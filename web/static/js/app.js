// get object of a bucket
function getObjects() {
    let bucket = document.getElementById("bucket").value;
    let prefix = document.getElementById("prefix").value;

    let responseDiv = document.getElementById("response-div");

    fetch(`/api/objects?bucket=${bucket}&prefix=${prefix}`)
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
        })
        .catch((e) => {
            console.error(e);
            responseDiv.innerText = "Error in reading objects!";

            alert("Failed to read objects!");
        });
}

// get url of an object
function getObjectURL() {
    let bucket = document.getElementById("bucket").value;
    let object = document.getElementById("object").value;

    fetch(`/api/objects/${bucket}/${object}`)
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
        })
        .catch((e) => {
            console.error(e);

            alert("Failed to get object link!");
        });
}
