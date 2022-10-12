import {getCookie} from "./common.js";

const csrftoken = getCookie('csrftoken');

function gotoLogin(){
    window.location.href = '/';
}

const roomName = JSON.parse(document.getElementById('room-name').textContent);
const username = JSON.parse(document.getElementById('username').textContent);
const onlineUsersSelector = document.querySelector("#onlineUsersSelector");

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onmessage = async function(e) {
    const data = JSON.parse(e.data);
    // check auth permissions
    if (data.auth) {
        if (data.auth === 'anon') gotoLogin();
        // join room through REST
        else await fetch(`/room/${roomName}/join/`, {
            method: 'PATCH',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({})
        }).then(response => response.json())
          .then(json => {console.log('json: ', json)
          // sends control message to backend
          chatSocket.send(JSON.stringify({
                'type': 'join',
                'message': '',
                'username': data.username,
                }));
          });
    }
    // updates user list if someone join/leave the room
    else {
        switch(data.type) {
            case 'join':
            case 'leave':
                await fetch(`/room/${roomName}/`, {
                    method: 'GET',
                    headers: {
                      'Content-Type': 'application/json',
                      'X-CSRFToken': csrftoken
                    }
                }).then(response => response.json())
                  .then(json => {
                      let usr_lib = {};
                      for (let usr of json.online) {
                          console.log(usr)
                           fetch(`/user/${usr}/`, {
                                method: 'GET',
                                headers: {
                                  'Content-Type': 'application/json',
                                  'X-CSRFToken': csrftoken
                                }
                          }).then(response => response.json())
                               .then(json => {
                                   console.log(json.member)
                                   fetch(`${json.member}`, {
                                        method: 'GET',
                                        headers: {
                                          'Content-Type': 'application/json',
                                          'X-CSRFToken': csrftoken
                                        }
                                   }).then(response => response.json())
                                       .then(json => {
                                           usr_lib[`${usr}`] = json.avatar;
                                       })
                               })
                      }
                      onlineUsersSelectorUpdate(usr_lib);
                  });
                break;
            case 'deletion':
                // handles room deletion message and sends respond
                chatSocket.send(JSON.stringify({
                'type': 'disconnect',
                'message': 'Has left room',
                'username': data.username,
                }));
                gotoLogin();
                break;
            case "private_message":
                document.querySelector('#chat-log').value += "PM from " + data.user + ": " + data.message + "\n";
                break;
            case "private_message_delivered":
                document.querySelector('#chat-log').value += "PM to " + data.target + ": " + data.message + "\n";
                break;
            default:
                // updates output field with received message
                document.querySelector('#chat-log').value += (data.username +': ' + data.message + '\n');

        }
    }
};

// handles socket error
chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

// input field interaction
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
        'type': 'message',
        'message': message,
        'username': username,
    }));
    messageInputDom.value = '';
    this.blur();
    document.querySelector('#chat-message-input').focus();
};

// leave button
document.querySelector('#chat-leave').onclick = async function (e) {
    chatSocket.send(JSON.stringify({
        'type': 'disconnect',
        'message': 'Has left room',
        'username': username,
    }));
    await fetch(`/room/${roomName}/leave/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({})
    }).then(response => response.json())
      .then(json => console.log('json: ', json));
    gotoLogin();
};

// delete button
document.querySelector('#chat-delete').onclick = async function (e) {
    // sends control message to backend
    await chatSocket.send(JSON.stringify({
        'type': 'delete.room',
        'message': 'Has deleted room',
        'username': username,
    }));
    //deletes room through REST
    await fetch(`/room/${roomName}/`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({name: roomName})
    }).then(response => response.status)
      .then(json => console.log('json: ', json));
    gotoLogin();
};

// adds/removes a new option to 'onlineUsersSelector'
function onlineUsersSelectorUpdate(userArray) {
    console.log('ua: ', userArray)
    // if (document.querySelector("option[value='" + value + "']")) return;
    onlineUsersSelector.innerHTML = '';
    for (let item in userArray) {
        console.log('item: ', item, userArray[item])
        let newOption = document.createElement("option");
        newOption.value = item;
        newOption.innerHTML = `<img src="${userArray[item]}">${item}</img>`;
        onlineUsersSelector.appendChild(newOption);
    }

}

onlineUsersSelector.onchange = function() {
    document.querySelector('#chat-message-input').value = "/pm " + onlineUsersSelector.value + " ";
    onlineUsersSelector.value = null;
    document.querySelector('#chat-message-input').focus();
};
