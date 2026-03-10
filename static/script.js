// RUN PYTHON CODE

function runCode(){

let code=document.getElementById("editor").value

fetch("/run",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
code:code
})

})

.then(res=>res.json())

.then(data=>{
document.getElementById("output").innerText=data.output
})

}



// SAVE FILE

function saveFile(){

let filename=prompt("Enter file name")

let code=document.getElementById("editor").value

fetch("/save_file",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
filename:filename,
code:code
})

})

.then(res=>res.json())

.then(data=>{
alert("File Saved!")
loadFiles()
})

}



// LOAD FILES

function loadFiles(){

fetch("/get_files")

.then(res=>res.json())

.then(files=>{

let list=document.getElementById("fileList")

list.innerHTML=""

files.forEach(file=>{

let li=document.createElement("li")

li.innerText=file.filename

li.onclick=function(){

document.getElementById("editor").value=file.code

}

list.appendChild(li)

})

})

}



// NEW FILE

function newFile(){

document.getElementById("editor").value=""

}



// THEME TOGGLE

function toggleTheme(){

document.body.classList.toggle("light-theme")

}



// LOAD FILES WHEN PAGE OPENS

window.onload=function(){

loadFiles()

}