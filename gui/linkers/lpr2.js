let {PythonShell} = require('python-shell')
function Classify_Image() {
var options = {
    pythonPath: "C:\\Python\\Python39\\python.exe",
    //scriptPath: "Main.py",
    //pythonOptions: ['-u']
};
PythonShell.run('engine/lpr/Main.py', options, function (err, results) {
  if (err) throw err;
  // results is an array consisting of messages collected during execution
  console.log('results: %j', results)
  //else
      //swal(message);
});
    //const spawn = require('child_process').spawn;
    //const scriptExecution = spawn(pythonExecutable, [myPythonScript]);

    //scriptExecution.on('message', function (message) {
        //console.log('Pipe data from python script ...');

//console.log(message)
    //});
}