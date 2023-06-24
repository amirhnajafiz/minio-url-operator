// get object of a bucket
function getObjects() {
    let bucket = "";
    let prefix = "";

    fetch(`/api/objects?bucket=${bucket}&prefix=${prefix}`)
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
        })
        .catch((e) => {
            console.error(e);
        })
}

// get url of an object
function getObjectURL() {
    let bucket = "";
    let object = "";

    fetch(`/api/objects/${bucket}/${object}`)
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
        })
        .catch((e) => {
            console.error(e);
        })
}
