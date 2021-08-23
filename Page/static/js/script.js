//selecting all required elements
const dropArea = document.querySelector(".drag-area");
const mainArea = document.querySelector(".main-area");

dragText = dropArea.querySelector("header");
fileInput = document.querySelector(".input-file")
submitInput = document.querySelector(".input-submit")

let files;


//If user Drag File Over DropArea
dropArea.addEventListener("dragover", (event)=>{
    event.preventDefault(); //preventing from default behaviour
    dropArea.classList.add("active");
    dragText.textContent = "Release to Upload File";
});

//If user leave dragged File from DropArea
dropArea.addEventListener("dragleave", ()=>{
    dropArea.classList.remove("active");
    dragText.textContent = "Drag & Drop to Upload File";
});

//If user drop File on DropArea
dropArea.addEventListener("drop", (event)=>{
    event.preventDefault(); //preventing from default behaviour
    files = event.dataTransfer.files;
    fileDropEvent();
});



function fileDropEvent()
{
    if(!isValid())
    {
        notValidCall();
    }
    else
    {
        validCall();
    }
}

function isValid()
{
    let validExtensions = ["image/jpeg", "image/jpg", "image/png"];
    for(var i = 0; i < files.length; i++)
    {
        console.log(files[i].type);
        if(!validExtensions.includes(files[i].type))
        {
            return false;
        }
    };
    return true
}


function notValidCall()
{
    alert("This is not an Image File!");
    dropArea.classList.remove("active");
    dragText.textContent = "Drag & Drop to Upload File";
}

function validCall()
{
    fileInput.files = files;
    submitInput.classList.add("active");
    submitInput.disabled = false;

    showFile(files[0]);
}

function receiveFile(data)
{
    let resultImage = jsonToBlob(data);
    showFile(resultImage);
}

function jsonToBlob(json)
{
    const str = JSON.stringify(json);
    const bytes = new TextEncoder().encode(str);
    const blob = new Blob([bytes], {
        type: "application/json;charset=urf-8"
    });
    return blob;
}

function showFile(file)
{
    console.log("show");
    //if user selected file is an image file
    let fileReader = new FileReader(); //creating new FileReader object
    fileReader.onload = ()=>{
        console.log("loader");
        let fileURL = fileReader.result; //passing user file source in fileURL variable
            // UNCOMMENT THIS BELOW LINE. I GOT AN ERROR WHILE UPLOADING THIS POST SO I COMMENTED IT
        let imgTag = `<img src="${fileURL}" alt="image">`; //creating an img tag and passing user selected file source inside src attribute
        dropArea.innerHTML = imgTag; //adding that created img tag inside dropArea container
    }
    fileReader.readAsDataURL(file);
}