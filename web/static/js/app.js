const downloadIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-down-square" viewBox="0 0 16 16">\n' +
    '  <path fill-rule="evenodd" d="M15 2a1 1 0 0 0-1-1H2a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V2zM0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2zm8.5 2.5a.5.5 0 0 0-1 0v5.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V4.5z"/>\n' +
    '</svg>';


// create tables from object names.
function generateTable(data) {
    let responseDiv = document.getElementById("response-div");
    let mainTable = document.createElement("table");

    let nameHeader = document.createElement("th");
    nameHeader.innerText = "Object name";

    let linkHeader = document.createElement("th");
    linkHeader.innerText = "Object link";

    mainTable.appendChild(nameHeader);
    mainTable.appendChild(linkHeader);
    mainTable.appendChild(document.createElement("tr"));

    data.forEach((name) => {
        let nameField = document.createElement("td");
        nameField.innerText = name;
        nameField.style.textAlign = 'left';
        nameField.classList.add("border-right");

        let linkField = document.createElement("td");
        let linkButton = document.createElement("button");
        linkButton.onclick = function () {
            getObjectURL(name);
        };
        linkButton.classList.add("btn", "url-btn");
        linkButton.innerHTML = downloadIcon;

        let linkButtonText = document.createElement("span");
        linkButtonText.innerText = "Copy URL";
        linkButtonText.style.marginLeft = "10px";

        linkButton.appendChild(linkButtonText);
        linkField.appendChild(linkButton);

        let updateField = document.createElement("td");
        let updateLinkButton = document.createElement("button");
        updateLinkButton.onclick = function () {
            updateObject(0, 0);
        }
        updateLinkButton.classList.add("btn", "url-btn");
        updateLinkButton.innerText = "Update";

        updateField.appendChild(updateLinkButton);

        mainTable.appendChild(nameField);
        mainTable.appendChild(linkField);
        mainTable.appendChild(updateField);
        mainTable.appendChild(document.createElement("tr"));
    });

    responseDiv.innerHTML = "";
    responseDiv.appendChild(mainTable);
}

// get object of a bucket
function getObjects() {
    let bucket = document.getElementById("bucket").value;
    let prefix = document.getElementById("prefix").value;

    let responseDiv = document.getElementById("response-div");

    fetch(`/api/objects?bucket=${bucket}&prefix=${prefix}`)
        .then((response) => response.json())
        .then((data) => {
            generateTable(data);
        })
        .catch((e) => {
            console.error(e);
            responseDiv.innerText = "Error in reading objects!";

            alert("Failed to read objects!");
        });
}

// update object url.
function updateObject(bucket, key, status) {
    fetch(`/api/objects/${bucket}/${key}?status=${status}`)
        .then(() => {
            console.log("update");

            alert("Update successfully!")
        })
        .catch((e) => {
            console.error(e);

            alert("Failed to update!")
        })
}

// get url of an object
function getObjectURL(key) {
    let bucket = document.getElementById("bucket").value;

    fetch(`/api/objects/${bucket}/${key}`)
        .then((response) => response.json())
        .then((data) => {
            let text = data['address'];

            navigator.clipboard.writeText(text).then(function() {
                alert('URL copied to clipboard.')
            }, function(err) {
                console.error(`could not copy text error=${err}`);
            });
        })
        .catch((e) => {
            console.error(e);

            alert("Failed to get object link!");
        });
}
