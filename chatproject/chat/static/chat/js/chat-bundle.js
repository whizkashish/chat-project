document.addEventListener("DOMContentLoaded", function() {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const currentUserElement = document.getElementById('current-user');
    const currentUser = currentUserElement.dataset.userId; // Get the username from the data attribute
    const token = getCookie('auth_token');
    const room_id = document.getElementById('chat-log').getAttribute('data-room-id');
    const chatLog = document.getElementById('chat-log');
    const chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/chat/' + room_id + '/?token='+token
    );
    chatLog.scrollTop = chatLog.scrollHeight;
    
    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const messagedivElement = document.createElement('div');
        const messageElement = document.createElement('p');
        messageElement.classList.add('chat-message');
        
        if (data.user == currentUser) { // Assuming currentUser is the logged-in user ID
            messagedivElement.classList.add('text-right');
            messageElement.classList.add('chat-message-right');
            messageElement.appendChild(document.createTextNode(data.message.content));
        } else {
            const usernameLink = document.createElement('a');
            usernameLink.setAttribute('href', '/account/profile/' + data.user); // Assuming user_id is passed with the data
            usernameLink.innerHTML = '<strong>' + data.user + '</strong>';
            messagedivElement.classList.add('text-left');
            messageElement.classList.add('chat-message-left');
            messageElement.appendChild(usernameLink);
            messageElement.appendChild(document.createTextNode(': ' + data.message.content));
        }
        
        messagedivElement.appendChild(messageElement);
        chatLog.appendChild(messagedivElement);
        chatLog.scrollTop = chatLog.scrollHeight;
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    const messageInputDom = document.getElementById('chat-message-input');
    const chatMessageSubmitButton = document.getElementById('chat-message-submit');

    messageInputDom.focus();
    messageInputDom.addEventListener('keyup', function(e) {
        if (e.keyCode === 13) {  // Enter key
            chatMessageSubmitButton.click();
        }
    });

    chatMessageSubmitButton.addEventListener('click', function() {
        const message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'message': message
        }));
        messageInputDom.value = '';
    });

});
