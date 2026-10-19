const API="/api";
function showNotification(message,kind="info"){const region=document.getElementById("notifications");if(!region)return;const node=document.createElement("div");node.className="notification";node.setAttribute("role",kind==="error"?"alert":"status");node.textContent=message;region.appendChild(node);setTimeout(()=>node.remove(),5000)}
function token(){return sessionStorage.getItem("accessEventToken")}
async function api(path,options={}){const headers={"Content-Type":"application/json",...(options.headers||{})};if(token())headers.Authorization="Bearer "+token();const response=await fetch(API+path,{...options,headers});const data=await response.json().catch(()=>({}));if(!response.ok)throw new Error(data.error||"Ошибка запроса");return data}
function esc(v){return String(v??"").replace(/[&<>\"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'\"':"&quot;","'":"&#39;"}[c]))}
async function loadEvents(){const list=document.getElementById("events-list");if(!list)return;const params=new URLSearchParams(new FormData(document.getElementById("event-search")));try{const events=await api("/events?"+params);if(!events.length){list.innerHTML='<p class="empty-state">Подходящих мероприятий пока нет.</p>';return}list.innerHTML=events.map(e=>`<article class="event-card"><h2>${esc(e.title)}</h2><p>${esc(e.description)}</p><p><b>Место:</b> ${esc(e.location||"Уточняется")}</p><p><b>Дата:</b> ${esc(new Date(e.event_date).toLocaleString("ru-RU"))}</p><p><b>Доступность:</b> ${esc(e.accessibility||"Уточняется")}</p><button class="button register-event" data-id="${Number(e.id)}">Записаться</button></article>`).join("");list.querySelectorAll(".register-event").forEach(b=>b.addEventListener("click",async()=>{if(!token()){showNotification("Сначала войдите в аккаунт.","error");return}try{await api("/events/"+b.dataset.id+"/register",{method:"POST",body:"{}"});showNotification("Вы записались на мероприятие")}catch(err){showNotification(err.message,"error")}}))}catch(err){list.textContent="Не удалось загрузить каталог.";showNotification(err.message,"error")}}
document.addEventListener("DOMContentLoaded",()=>{const search=document.getElementById("event-search");if(search){search.addEventListener("submit",e=>{e.preventDefault();loadEvents()});loadEvents()}const login=document.getElementById("login-form");if(login)login.addEventListener("submit",async e=>{e.preventDefault();try{const r=await api("/auth/login",{method:"POST",body:JSON.stringify(Object.fromEntries(new FormData(login)))});sessionStorage.setItem("accessEventToken",r.token);location.href="/profile"}catch(err){showNotification(err.message,"error")}});const reg=document.getElementById("register-form");if(reg)reg.addEventListener("submit",async e=>{e.preventDefault();const f=new FormData(reg),d=Object.fromEntries(f);d.is_deaf=f.has("is_deaf");try{const r=await api("/auth/register",{method:"POST",body:JSON.stringify(d)});sessionStorage.setItem("accessEventToken",r.token);location.href="/profile"}catch(err){showNotification(err.message,"error")}});const logout=document.getElementById("logout-button");if(logout)logout.addEventListener("click",()=>{sessionStorage.removeItem("accessEventToken");location.href="/"});const profile=document.getElementById("profile-status");if(profile&&token()){profile.textContent="Вы вошли. Ваши регистрации:";api("/me/registrations").then(items=>{document.getElementById("my-registrations").innerHTML=items.length?items.map(x=>`<li>Мероприятие №${Number(x.event_id)}</li>`).join(""):"<li>Регистраций пока нет.</li>"}).catch(e=>showNotification(e.message,"error"))}});

/* Event detail: visual status, text chat and reviews. */
async function loadEventDetail() {
  const root = document.getElementById("event-detail");
  if (!root) return;
  const id = root.dataset.eventId;
  try {
    const event = await api("/events/" + id);
    root.innerHTML = '<h1>' + esc(event.title) + '</h1><p>' + esc(event.description || "") +
      '</p><p><b>Дата:</b> ' + esc(new Date(event.event_date).toLocaleString("ru-RU")) +
      '</p><p><b>Место:</b> ' + esc(event.location || "Уточняется") +
      '</p><p><b>Доступность:</b> ' + esc(event.accessibility || "Уточняется") + '</p>';
  } catch (error) { root.textContent = "Не удалось загрузить мероприятие."; showNotification(error.message, "error"); }
}
async function loadChat() {
  const root = document.getElementById("chat-messages");
  const detail = document.getElementById("event-detail");
  if (!root || !detail) return;
  try {
    const rows = await api("/events/" + detail.dataset.eventId + "/messages");
    root.innerHTML = rows.map(row => '<p class="chat-message">' + esc(row.message) + '</p>').join("") || "<p>Сообщений пока нет.</p>";
  } catch (error) { root.textContent = "Войдите, чтобы открыть чат."; }
}
async function loadReviews() {
  const root = document.getElementById("reviews");
  const detail = document.getElementById("event-detail");
  if (!root || !detail) return;
  try {
    const rows = await api("/events/" + detail.dataset.eventId + "/reviews");
    root.innerHTML = rows.map(row => '<article class="event-card"><b>Оценка ' + Number(row.rating) + '/5</b><p>' + esc(row.comment) + '</p></article>').join("") || "<p>Отзывов пока нет.</p>";
  } catch (error) { root.textContent = "Не удалось загрузить отзывы."; }
}
document.addEventListener("DOMContentLoaded", () => {
  const detail = document.getElementById("event-detail");
  if (detail) {
    loadEventDetail(); loadChat(); loadReviews();
    const id = detail.dataset.eventId;
    const registerButton = document.getElementById("register-btn");
    if (registerButton) registerButton.addEventListener("click", async () => {
      try {
        const result = await api("/events/" + id + "/register", {method:"POST", body:"{}"});
        const banner = document.getElementById("status-banner");
        banner.className = "status-banner status-" + result.status;
        banner.textContent = result.status === "pending" ? "Заявка на рассмотрении" : result.status;
      } catch (error) { document.getElementById("reg-result").textContent = error.message; }
    });
    const chatForm = document.getElementById("chat-form");
    if (chatForm) chatForm.addEventListener("submit", async event => {
      event.preventDefault();
      try {
        await api("/events/" + id + "/messages", {method:"POST", body:JSON.stringify({message:chatForm.message.value})});
        chatForm.reset(); await loadChat();
      } catch (error) { document.getElementById("reg-result").textContent = error.message; }
    });
    const reviewForm = document.getElementById("review-form");
    if (reviewForm) reviewForm.addEventListener("submit", async event => {
      event.preventDefault();
      try {
        await api("/events/" + id + "/reviews", {method:"POST", body:JSON.stringify({rating:reviewForm.rating.value, comment:reviewForm.comment.value})});
        reviewForm.reset(); await loadReviews(); showNotification("Отзыв сохранён.");
      } catch (error) { document.getElementById("reg-result").textContent = error.message; }
    });
  }
  const dashboard = document.getElementById("dashboard-status");
  if (dashboard && token()) {
    dashboard.textContent = "Ваши регистрации и уведомления";
    api("/my/registrations").then(items => {
      const list = document.getElementById("my-registrations");
      list.innerHTML = items.map(x => '<li>Мероприятие №' + Number(x.event_id) + ' — ' + esc(x.status) + '</li>').join("") || "<li>Регистраций пока нет.</li>";
    }).catch(error => showNotification(error.message, "error"));
    api("/notifications").then(items => {
      const list = document.getElementById("my-notifications");
      list.innerHTML = items.map(x => '<p class="status-banner status-' + (x.type.endsWith("confirmed") ? "confirmed" : x.type.endsWith("cancelled") ? "cancelled" : "pending") + '">' + esc(x.type.replaceAll("_", " ")) + '</p>').join("") || "<p>Новых уведомлений нет.</p>";
    }).catch(error => showNotification(error.message, "error"));
  }
});
