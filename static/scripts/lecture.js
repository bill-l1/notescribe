var socket = io.connect('http://127.0.0.1:5000/');

socket.on('connect', function() {
    console.log("connected");
});

let url = new URL(window.location.href);
let CLASSROOM = url.searchParams.get("classroom");
let KEY = url.searchParams.get("key");

const firebaseConfig = {
  apiKey: "AIzaSyAn2bI9-r1lQrRdao7QQ6GUXu2ZK-f9Hvc",
  authDomain: "htn-aydan.firebaseapp.com",
  databaseURL: "https://htn-aydan.firebaseio.com",
  projectId: "htn-aydan",
  storageBucket: "htn-aydan.appspot.com",
  messagingSenderId: "150429804004",
  appId: "1:150429804004:web:c24ffbf4cbce1a144c93f1"
};

firebase.initializeApp(firebaseConfig);

Element.prototype.remove = function() {
    this.parentElement.removeChild(this);
}
NodeList.prototype.remove = HTMLCollection.prototype.remove = function() {
    for(var i = this.length - 1; i >= 0; i--) {
        if(this[i] && this[i].parentElement) {
            this[i].parentElement.removeChild(this[i]);
        }
    }
}

let blockData = {};

fetch("https://firebasestorage.googleapis.com/v0/b/htn-aydan.appspot.com/o/"+CLASSROOM+"%2F"+KEY+".json?alt=media&token=6d1bc873-d336-412a-88c1-49ecdc8c9ef5")
    .then(function (response) {
      blockData = response.json();
      return blockData
    })
    .then(function(data) {
      appendData(data);
    })
    .catch(function(err) {
      console.log("owo " + err);
    });

function appendData(data) {
  var mainContainer = document.getElementById("transcription-box");
  blockData = data;
  for(var i = 0; i < data.blockArray.length; i++) {
    console.log(i)
    var div = document.createElement("div");
    div.className = "word-block"
    div.id = i.toString();
    div.setAttribute("ondblclick", "startEdit("+i.toString()+")");

    div.innerHTML = data.blockArray[i].text;
    mainContainer.appendChild(div);
  }
}

function startEdit(id){

  let block = document.getElementById(id)
  if(block.getElementsByClassName("edit-container").length == 0){
    let editContainer = document.createElement("div");
    editContainer.id = "edit-container-"+id;
    editContainer.className = "edit-container";
    block.appendChild(editContainer)

    block.style.backgroundColor = "yellow";
    block.setAttribute("contenteditable", "true");
    block.focus();
    console.log("bruh", id);

    let confirmButton = document.createElement("button");
    confirmButton.onclick = () => {stopEdit(id, 1)};
    confirmButton.className = "edit-button-confirm";
    confirmButton.setAttribute("contenteditable", "false");
    confirmButton.innerHTML = "√";
    editContainer.appendChild(confirmButton);

    let cancelButton = document.createElement("button");
    cancelButton.onclick = () => {stopEdit(id, 0)};
    cancelButton.className = "edit-button-confirm";
    cancelButton.setAttribute("contenteditable", "false");
    cancelButton.innerHTML = "X";
    editContainer.appendChild(cancelButton);
  }
}

$(document).keypress(
  function(event){
    if (event.which == '13') {
      event.preventDefault();
    }
});

function stopEdit(id, val=0){
  //0 - cancel, 1 - confirm
  document.getElementById("edit-container-"+id).remove();
  let block = document.getElementById(id)
  block.style.backgroundColor = "white";
  block.setAttribute("contenteditable", "false");
  block.blur();
  if(blockData.blockArray[id].text != block.innerHTML && val == 1){
    blockData.blockArray[id].text = block.innerHTML;
    let storageRef = firebase.storage().ref();
    let jsonRef = storageRef.child(blockData.classroom + "/" + blockData.key + ".json")
    let json = new File([JSON.stringify(blockData)], blockData.key + ".json")
    console.log(json)
    jsonRef.put(json).then(snapshot => {
      console.log('Uploaded', blockData.key+".json");
    });
  }else{
     block.innerHTML = blockData.blockArray[id].text;
  }
}
