import {getCookie} from "./common";

const csrftoken = getCookie('csrftoken');

function gotoLogin(){
    window.location.href = '/';
}

const roomName = JSON.parse(document.getElementById('room-name').textContent);
const username = JSON.parse(document.getElementById('username').textContent);

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if (data.auth) {
        if (data.auth === 'anon') gotoLogin()
    }
    else {
        switch (data.type){
            case 'delete':
                chatSocket.send(JSON.stringify({
                    'type': 'disconnect',
                    'message': 'Has left room',
                    'username': username,
                    }));
                gotoLogin();
                break;
        }
        document.querySelector('#chat-log').value += (data.username +': ' + data.message + '\n');
    }
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message,
        'username': username,
    }));
    messageInputDom.value = '';
};

document.querySelector('#chat-leave').onclick = function (e) {
    chatSocket.send(JSON.stringify({
        'type': 'disconnect',
        'message': 'Has left room',
        'username': username,
    }));
    gotoLogin();
};

document.querySelector('#chat-delete').onclick = async function (e) {
    await chatSocket.send(JSON.stringify({
        'type': 'delete_room',
        'message': 'Has deleted room',
        'username': username,
    }));
    await fetch('/room/', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({name: roomName})
    })
        .then(response => response.json())
        .then(json => console.log('json: ', json));
    gotoLogin();
}

