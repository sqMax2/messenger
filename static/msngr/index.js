import {getCookie} from "./common";
var roomList = [];

const csrftoken = getCookie('csrftoken');

window.onload = async function (e) {
    let roomListDatalist = document.querySelector('#room-list');
    await fetch('/room/')
    .then(response => response.json())
    .then(json => {
        for (let name of json['results']) {
            roomList.push(name['name']);
            roomListDatalist.insertAdjacentHTML('beforeend',
                `<option value="${name['name']}">users: ${name['get_online_count']}</option>`);
        }
    })
    if (typeof roomList == 'undefined') {
        roomList = [];
    }

};
document.querySelector('#room-name-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#room-name-submit').click();
    }
};

document.querySelector('#room-name-input').onkeypress = function(e) {
    const char = String.fromCharCode(e.charCode);
    console.log(e);
    if (e.target.value == '') {
        if (!(/[a-zA-Z\.$]/.test(char))) {  // enter, return
        console.log('prevent first')
        e.preventDefault();
        }
    }
    if (!(/[a-zA-Z0-9_\.$]/.test(char))) {  // enter, return
        console.log('prevent')
        e.preventDefault();
    }
};

document.querySelector('#room-name-submit').onclick = async function(e) {
    let roomName = document.querySelector('#room-name-input').value;
    if (roomList.indexOf(roomName) < 0) {
        await fetch('/room/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({name: roomName})
        })
            .then(response => response.json())
            .then(json => console.log('json: ', json));
    }
    window.location.pathname = '/chat/' + roomName + '/';
};