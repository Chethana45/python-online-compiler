// =============================
// RUN PYTHON CODE
// =============================

async function runCode(){

    const code = document.getElementById("editor").value
    const input = document.getElementById("programInput") ? 
                  document.getElementById("programInput").value : ""

    document.getElementById("output").innerText = "Running..."

    try{

        const response = await fetch("/run",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                code:code,
                input:input
            })
        })

        const data = await response.json()

        document.getElementById("output").innerText = data.output

    }
    catch(err){
        document.getElementById("output").innerText = "Error running program"
    }

}



// =============================
// SAVE FILE
// =============================

function saveFile(){

    let filename = prompt("Enter file name")

    if(!filename) return

    let code = document.getElementById("editor").value

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



// =============================
// LOAD FILE LIST
// =============================

function loadFiles(){

    fetch("/get_files")

    .then(res=>res.json())

    .then(files=>{

        let list = document.getElementById("fileList")

        if(!list) return

        list.innerHTML = ""

        files.forEach(file=>{

            let li = document.createElement("li")

            li.innerText = file.filename

            li.onclick = function(){
                document.getElementById("editor").value = file.code
            }

            list.appendChild(li)

        })

    })

}



// =============================
// NEW FILE
// =============================

function newFile(){
    document.getElementById("editor").value = ""
}



// =============================
// THEME TOGGLE
// =============================

function toggleTheme(){
    document.body.classList.toggle("light-theme")
}



// =============================
// LOAD FILES WHEN PAGE LOADS
// =============================

window.onload = function(){
    loadFiles()
}