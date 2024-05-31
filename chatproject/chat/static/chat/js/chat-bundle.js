const room_idElement = document.getElementById('chat-log');
if (room_idElement) {
    const room_id = room_idElement.getAttribute('data-room-id');

    const chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/chat/' + room_id + '/'
    );

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const chatLog = document.querySelector('#chat-log');
        if (chatLog) {
           // debugger;
            console.log('connected');
            chatLog.innerHTML += data.message + '<br>';
        }
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    const messageInputDom = document.querySelector('#chat-message-input');
    const chatMessageSubmitButton = document.querySelector('#chat-message-submit');
    if (messageInputDom && chatMessageSubmitButton) {
        messageInputDom.focus();
        messageInputDom.onkeyup = function(e) {
            if (e.keyCode === 13) {  // Enter key
                chatMessageSubmitButton.click();
            }
        };

        chatMessageSubmitButton.onclick = function(e) {
            const message = messageInputDom.value;
            chatSocket.send(JSON.stringify({
                'message': message
            }));
            messageInputDom.value = '';
        };
    }
}