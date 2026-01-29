// Dark mode
document.getElementById('dark-mode-toggle')?.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
});
if (localStorage.getItem('darkMode') === 'true') document.body.classList.add('dark-mode');

// Geolocation
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((pos) => {
            document.getElementById('location').value = `${pos.coords.latitude}, ${pos.coords.longitude}`;
        });
    } else alert('Geolocation not supported.');
}

// Notifications
function checkNotifications() {
    fetch('/api/alerts').then(r => r.json()).then(d => {
        const div = document.getElementById('notifications');
        if (div) div.innerHTML = d.length ? `New alerts: ${d.length}` : 'No alerts';
    });
}
setInterval(checkNotifications, 10000);

// Comments
function addComment(id) {
    const comment = document.getElementById(`comment-${id}`).value;
    if (comment) {
        const div = document.getElementById(`comments-${id}`);
        div.innerHTML += `<p>${comment}</p>`;
        document.getElementById(`comment-${id}`).value = '';
    }
}