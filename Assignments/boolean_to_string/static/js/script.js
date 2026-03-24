function convertBoolean() {
    let value = document.getElementById("inputValue").value;

    let result = Boolean(value);

    document.getElementById("output").innerHTML =
        "Original Value: " + value + "<br>" +
        "Converted to Boolean: " + result;
}

function convertString() {
    let value = document.getElementById("inputValue").value;

    let result = String(value);

    document.getElementById("output").innerHTML =
        "Original Type: " + typeof value + "<br>" +
        "Converted to String: " + result;
}