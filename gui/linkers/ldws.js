let {PythonShell} = require('python-shell')
var path = require("path")

function Classify_Images() {
  let options = {
    scriptPath: path.join(__dirname, '/../engine/')
  };
  let pyshell = new PythonShell('ldws/project_hard.py', options);
  //const python = require("python-shell");
  //const path = require("path");
pyshell.on('message', function(message) {
    swal(message);
  })
  //path.join(__dirname, '/../engine/');
  //new python("Climate.py", options);
  //end(function () {
    //document.getElementById("detect").value = "Detect Images";

}