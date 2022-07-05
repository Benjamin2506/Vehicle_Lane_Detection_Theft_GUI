let {PythonShell} = require('python-shell')
const path = require("path");

function Classify_Image() {
  let options = {
    scriptPath: path.join(__dirname, '/../engine/lpr/')
  };
  let pyshell = new PythonShell('Main.py', options);
  //const python = require("python-shell");
  //const path = require("path");
pyshell.on('message', function(message) {
    swal(message);
    console.log(message)
  })
  //path.join(__dirname, '/../engine/');
  //new python("Climate.py", options);
  //end(function () {
    //document.getElementById("detect").value = "Detect Images";

}