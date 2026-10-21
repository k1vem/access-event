function showNotification(message, type = 'info') {
    const container = document.getElementById('notifications');
    if (!container) return;
    const notice = document.createElement('div');
    notice.className = 'notification notification-' + type;
    notice.textContent = message;
    container.appendChild(notice);
    setTimeout(() => notice.remove(), 4000);
}