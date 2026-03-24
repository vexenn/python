document.addEventListener('DOMContentLoaded', () => {
    const calculateBtn = document.getElementById('calculateBtn');
    const resultDiv = document.getElementById('result');

    calculateBtn.addEventListener('click', () => {
        // Grab values from inputs
        const weight = parseFloat(document.getElementById('weight').value);
        const height = parseFloat(document.getElementById('height').value);

        // Validation: Ensure numbers are entered and height isn't zero
        if (isNaN(weight) || isNaN(height) || height <= 0) {
            resultDiv.innerHTML = "Please enter valid numbers for weight and height.";
            resultDiv.style.color = "red";
            return;
        }

        // Calculate BMI
        const bmi = (weight / (height * height)).toFixed(2);

        // Determine Category
        let category = "";
        if (bmi < 18.5) {
            category = "Underweight";
        } else if (bmi < 25) {
            category = "Normal weight";
        } else if (bmi < 30) {
            category = "Overweight";
        } else {
            category = "Obese";
        }

        // Display Result
        resultDiv.style.color = "blue";
        resultDiv.innerHTML = `<h3>Your BMI is: ${bmi}</h3><p>Category: <strong>${category}</strong></p>`;
    });
});