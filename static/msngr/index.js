import {getCookie} from "./common.js";
var roomList = [];

const csrftoken = getCookie('csrftoken');
async function updateList(e) {
    let roomListDatalist = document.querySelector('#room-list');
    await fetch('/room/')
    .then(response => response.json())
    .then(json => {
        roomList = [];
        roomListDatalist.innerHTML = '';
        for (let name of json['results']) {
            roomList.push(name['name']);
            roomListDatalist.insertAdjacentHTML('beforeend',
                `<option value="${name['name']}">users: ${name['get_online_count']}</option>`);
        }
    })
    if (typeof roomList == 'undefined') {
        roomList = [];
    }
}


window.onload = async function (e) {
    await updateList(e);
};

document.querySelector('#room-name-input').onmousedown = async function (e) {
    await updateList(e);
};

document.querySelector('#room-name-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#room-name-submit').click();
    }
};

document.querySelector('#room-name-input').focus();
document.querySelector('#room-name-input').onkeydown = function(e) {
    const char = e.key
    const btn = document.querySelector('#room-name-submit');
    if ((char === 'Backspace' || char === 'Delete') && (e.target.value.length === 1)) {
    }
    if (e.target.value === '') {
        if (!(/[a-zA-Z\.$]/.test(char))) {
            e.preventDefault();
        }
    }
    if (!(/[a-zA-Z0-9_\.$]/.test(char))) {
        e.preventDefault();
    }

};

document.querySelector('#room-name-input').oninput = function(e) {
    document.querySelector('#room-name-submit').disabled = !e.target.checkValidity();
}

document.querySelector('#room-name-submit').onclick = async function(e) {
    let roomName = document.querySelector('#room-name-input').value;
    e.target.disabled = !document.querySelector('#room-name-input').checkValidity();
    if (e.target.disabled) return '';
    if (roomList.indexOf(roomName) < 0) {
        await fetch('/room/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({name: roomName, online: []})
        })
            .then(response => response.json())
            .then(json => console.log('json: ', json));
    }
    window.location.pathname = '/chat/' + roomName + '/';
};