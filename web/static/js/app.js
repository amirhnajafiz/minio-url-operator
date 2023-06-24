// create tables from object names.
function generateTable(data) {
    let mainTable = document.createElement("table");

    let nameHeader = document.createElement("th");
    nameHeader.innerText = "name";

    let linkHeader = document.createElement("th");
    linkHeader.innerText = "link";

    mainTable.appendChild(nameHeader);
    mainTable.appendChild(linkHeader);
    mainTable.appendChild(document.createElement("tr"));

    data.forEach((name) => {
        let nameField = document.createElement("td");
        nameField.innerText = name;

        let linkField = document.createElement("td");
        let linkButton = document.createElement("button");
        linkButton.onclick = function () {
            getObjectURL(name);
        };
        linkButton.innerText = "Get URL";

        linkField.appendChild(linkButton);

        mainTable.appendChild(nameField);
        mainTable.appendChild(linkButton);
        mainTable.appendChild(document.createElement("tr"));
    })

    document.getElementById("response-div").appendChild(mainTable);
}

// get object of a bucket
function getObjects() {
    let bucket = document.getElementById("bucket").value;
    let prefix = document.getElementById("prefix").value;

    let responseDiv = document.getElementById("response-div");

    fetch(`/api/objects?bucket=${bucket}&prefix=${prefix}`)
        .then((response) => response.json())
        .then((data) => {
            console.log(data);

            generateTable(data);
        })
        .catch((e) => {
            console.error(e);
            responseDiv.innerText = "Error in reading objects!";

            alert("Failed to read objects!");
        });
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
