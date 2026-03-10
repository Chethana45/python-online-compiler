// RUN CODE

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

if(!filename) return

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
alert("File Saved")
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

li.style.display="flex"
li.style.justifyContent="space-between"
li.style.alignItems="center"

let name=document.createElement("span")

name.innerText=file.filename

name.onclick=function(){
document.getElementById("editor").value=file.code
}

let controls=document.createElement("div")

let renameBtn=document.createElement("button")
renameBtn.innerText="✏"
renameBtn.onclick=function(){
renameFile(file.filename)
}

let deleteBtn=document.createElement("button")
deleteBtn.innerText="🗑"
deleteBtn.onclick=function(){
deleteFile(file.filename)
}

controls.appendChild(renameBtn)
controls.appendChild(deleteBtn)

li.appendChild(name)
li.appendChild(controls)

list.appendChild(li)

})

})

}



// DELETE FILE

function deleteFile(filename){

if(!confirm("Delete this file?")) return

fetch("/delete_file",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
filename:filename
})

})

.then(res=>res.json())

.then(data=>{
loadFiles()
})

}



// RENAME FILE

function renameFile(oldname){

let newname=prompt("Enter new file name")

if(!newname) return

fetch("/rename_file",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
old_name:oldname,
new_name:newname
})

})

.then(res=>res.json())

.then(data=>{
loadFiles()
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



// LOAD FILES WHEN PAGE LOADS

window.onload=function(){
loadFiles()
}