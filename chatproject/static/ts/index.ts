const roomNameElement = document.getElementById('room-name');
if (roomNameElement) {
    const roomName = JSON.parse(roomNameElement.textContent || '');

    const chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
    );

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const chatLogElement = document.querySelector('#chat-log') as HTMLElement;
        if (chatLogElement) {
            chatLogElement.innerHTML += (data.message + '\n');
        }
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    const messageInputDom = document.querySelector('#chat-message-input') as HTMLInputElement;
    const chatMessageSubmitButton = document.querySelector('#chat-message-submit') as HTMLElement;
    if (messageInputDom && chatMessageSubmitButton) {
        messageInputDom.focus();
        messageInputDom.onkeyup = function(e: KeyboardEvent) {
            if (e.keyCode === 13) {  // Enter key
                chatMessageSubmitButton.click();
            }
        };

        chatMessageSubmitButton.onclick = function(e: MouseEvent) {
            const message = messageInputDom.value;
            chatSocket.send(JSON.stringify({
                'message': message
            }));
            messageInputDom.value = '';
        };
    }
}
