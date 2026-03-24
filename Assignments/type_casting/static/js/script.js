function implicitDemo() {
    let value = document.getElementById("inputValue").value;

    // Implicit conversion
    let result1 = value + 5;   // string + number
    let result2 = value - 5;   // string - number

    document.getElementById("output").innerHTML =
        "Input Type: " + typeof value + "<br>" +
        "value + 5 = " + result1 + "<br>" +
        "value - 5 = " + result2;
}

function explicitDemo() {
    let value = document.getElementById("inputValue").value;

    let numberValue = Number(value);
    console.log(numberValue);

    document.getElementById("output").innerHTML =
        "Converted Type: " + typeof numberValue + "<br>" +
        "Number(value) + 5 = " + (numberValue + 5) + "<br>" +
        "Boolean(value) = " + Boolean(numberValue);
}