var socket = io.connect('http://127.0.0.1:5000/');

socket.on('connect', function() {
    console.log("connected");
});

let url = new URL(window.location.href);
let CLASSROOM = url.searchParams.get("classroom");
let KEY = url.searchParams.get("key");

const firebaseConfig = {
  apiKey: "-"",
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

let lectureRef = firebase.database().ref("Transcripts/"+CLASSROOM+"/"+KEY);
let blockData = [];
let mainContainer = document.getElementById("transcription-box");

lectureRef.once('value').then(snapshot => {
  let blockData = snapshot.val();
  createBlockDiv(blockData);
});

function createBlockDiv(blockArray){
  for(i in blockArray){

    let block = blockArray[i];
    console.log(block.text);
    blockData.push(block);

    let div = document.createElement("div");
    div.className = "my-4 mx-auto text-center word-block";
    div.id = i.toString();
    div.setAttribute("ondblclick", "startEdit("+i.toString()+")");
    div.innerHTML = block.text;
    mainContainer.appendChild(div);
  }
}

function startEdit(id){
  let block = document.getElementById(id);
  if(block.getElementsByClassName("edit-container").length == 0){
    let editContainer = document.createElement("div");
    editContainer.id = "edit-container-"+id;
    editContainer.className = "edit-container";
    block.appendChild(editContainer);

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
  let blockElement = document.getElementById(id)
  blockElement.style.backgroundColor = "white";
  blockElement.setAttribute("contenteditable", "false");
  blockElement.blur();

  if(blockData[id].text != block.innerHTML && val == 1){
    blockData[id].text = block.innerHTML;
    lectureRef.set(blockData);
  }else{
     block.innerHTML = blockData.blockArray[id].text;
  }
}
