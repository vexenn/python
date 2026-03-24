function showPrimitive() {

    let num = 10;
    let str = "Hello";
    let bool = true;
    let undef;
    let empty = null;

    let output =
        "Number: " + num + " | Type: " + typeof num + "\n" +
        "String: " + str + " | Type: " + typeof str + "\n" +
        "Boolean: " + bool + " | Type: " + typeof bool + "\n" +
        "Undefined: " + undef + " | Type: " + typeof undef + "\n" +
        "Null: " + empty + " | Type: " + typeof empty;

    document.getElementById("output").textContent = output;
}

function showNonPrimitive() {

    let array = [1, 2, 3];
    let obj = { name: "Somya", age: 25 };
    let func = function () { return "Hello"; };

    let output =
        "Array: " + JSON.stringify(array) + " | Type: " + typeof array + "\n" +
        "Object: " + JSON.stringify(obj) + " | Type: " + typeof obj + "\n" +
        "Function: " + func() + " | Type: " + typeof func;

    document.getElementById("output").textContent = output;
}