var socket = io.connect('http://127.0.0.1:5000/');

socket.on('connect', function() {
    console.log("connected");
    socket.on('disconnect', function(){
      console.log('user disconnected');
    });
    socket.on('processing_done', function(data){
        console.log("processing finished");
        window.location.href = '/lecture?classroom='+data.classroom+"&key="+data.key;
    });
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
  let uploadElement = document.getElementById('fileupload');
  let formData = new FormData();
  let key = new Date().getTime().toString();
  let classroom = "CS135"
  let storageRef = firebase.storage().ref();
  let wavRef = storageRef.child(classroom + "/" + key + ".wav")

  let uploadBanner = document.getElementById('uploadbanner');
  let loading = document.createElement("h1");
  uploadBanner.appendChild(loading);

  console.log(uploadElement.files[0]);
  let file = uploadElement.files[0];

  if(!file){
    alert("No file specified!");
    uploadElement.files.shift();
  }else if(file.type != "audio/wav"){
    alert("Audio must be a .wav file");
    uploadElement.files.shift();
  }else if(file.size >= 100000000){
    alert("Audio file too large");
    uploadElement.files.shift();
  }else{
    loading.innerHTML = "Loading..."
    wavRef.put(uploadElement.files[0]).then(snapshot => {
      console.log('Uploaded.');
      socket.emit('createBlockData', {'key': key, 'classroom': classroom});
      loading.innerHTML = "Processing..."
    });
    $("#submit").submit();
  }


}
