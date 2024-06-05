// Frontend JavaScript logic to display browser notifications

// Fetch notifications for the current user
function fetchNotifications() {
    // Make an AJAX request to fetch notifications
    fetch('/account/notifications/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        // Process and display notifications
        data.notifications.forEach(notification => {
            displayBrowserNotification(notification);
        });
    })
    .catch(error => console.error('Error fetching notifications:', error));
}

// Display a browser notification
function displayBrowserNotification(notification) {
    // Check if the browser supports notifications
    if (Notification.permission === 'granted') {
        // Create a new notification
        var newNotification = new Notification('New Message', {
            body: notification.message,
            icon: notification.icon || '/static/images/default-icon.png'  // Optional: add an icon
        });
        
        // Handle notification click event
        newNotification.onclick = function(event) {
            
            event.preventDefault();  // Prevent the browser from focusing the Notification's tab
            markNotificationAsRead(notification.id, notification.link);
           
        };
    } else if (Notification.permission !== 'denied') {
        // Request permission to show notifications
        Notification.requestPermission().then(function(permission) {
            if (permission === 'granted') {
                // Call displayBrowserNotification again after permission is granted
                displayBrowserNotification(notification);
            }
        });
    }
}


// Mark a notification as read
function markNotificationAsRead(notificationId, link) {
    fetch(`/account/notifications/mark_as_read/${notificationId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // Ensure you send the CSRF token
        },
        body: JSON.stringify({ is_read: true })
    })
    .then(response => response.json())
    .then(data => {
        debugger;
         // Redirect to the appropriate URL when the notification is clicked
         window.location.href = link;  // Open link in a new tab
    })
    .catch(error => console.error('Error marking notification as read:', error));
}

// Helper function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Call fetchNotifications() to fetch and display notifications when the page loads
document.addEventListener('DOMContentLoaded', function() {
    fetchNotifications();

    // Optional: Set an interval to periodically fetch notifications
    setInterval(fetchNotifications, 60000);  // Fetch notifications every 60 seconds
});
