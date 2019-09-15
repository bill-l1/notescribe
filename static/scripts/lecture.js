var socket = io.connect('http://127.0.0.1:5000/');

socket.on('connect', function() {
    console.log("connected");
});

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

let uploadFile = function(){
  let element = document.getElementById('fileupload');
  let formData = new FormData();
  let key = new Date().getTime().toString();
  let classroom = "CS135"
  let storageRef = firebase.storage().ref();
  let wavRef = storageRef.child(classroom + "/" + key + ".wav")

  console.log(element.files[0]);
  wavRef.put(element.files[0]).then(snapshot => {
    console.log('Uploaded.');
    socket.emit('createBlockData', {'key': key, 'classroom': classroom});
  });
  $("#submit").submit();

}

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

blockData = {};

fetch("https://firebasestorage.googleapis.com/v0/b/htn-aydan.appspot.com/o/CS135%2F1568536654383.json?alt=media&token=610dbc5b-92df-47c0-8e53-6502eaad8176")
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
  for(var i = 0; i < data.length; i++) {
    console.log(i)
    var div = document.createElement("div");
    div.className = "word-block"
    div.id = i.toString();
    div.setAttribute("ondblclick", "startEdit("+i.toString()+")");

    div.innerHTML = data[i].text;
    mainContainer.appendChild(div);
  }
}

function startEdit(id){

  let block = document.getElementById(id)
  let editContainer = document.createElement("div");
  editContainer.id = "edit-container-"+id;
  editContainer.className = "edit-container";
  block.appendChild(editContainer)

  block.style.backgroundColor = "red";
  block.setAttribute("contenteditable", "true");
  block.focus();
  console.log("bruh", id);

  let confirmButton = document.createElement("button");
  confirmButton.onclick = () => {stopEdit(id)};
  confirmButton.className = "edit-button-confirm";
  confirmButton.innerHTML = "√";
  editContainer.appendChild(confirmButton);
}

function stopEdit(id){
  document.getElementById("edit-container-"+id).remove();
  let block = document.getElementById(id)
  block.style.backgroundColor = "white";
  block.setAttribute("contenteditable", "false");
  block.blur();
  console.log("remove pls");
  valueOf(id)
}
