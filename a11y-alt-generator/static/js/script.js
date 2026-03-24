document.getElementById('altTextForm').addEventListener('submit', async function(event) {
    // 1. Prevent the standard HTML form from reloading the page
    event.preventDefault(); 

    const form = event.target;
    const formData = new FormData(form);
    
    // Grab all the necessary elements from the DOM
    const resultContainer = document.getElementById('resultContainer');
    const altTextOutput = document.getElementById('altTextOutput');
    const htmlCodeOutput = document.getElementById('htmlCodeOutput');
    const submitButton = form.querySelector('button');
    const imagePreview = document.getElementById('imagePreview');

    // 2. Change button text and disable it to show it's working
    submitButton.textContent = 'Generating...';
    submitButton.disabled = true;

    try {
        // 3. Send the data to your Flask backend route
        const response = await fetch('/generate-alt-text', {
            method: 'POST',
            body: formData 
        });

        // 4. Wait for the Python backend to reply
        const data = await response.json();

        if (response.ok) {
            // 5. Inject the AI text into the page
            altTextOutput.textContent = data.alt_text;
            
            // Grab the original file to use its name and create the preview
            const fileInput = form.querySelector('#imageUpload');
            const file = fileInput.files[0];
            const fileName = file.name;
            
            // Write the ready-to-use HTML snippet
            htmlCodeOutput.textContent = `<img src="${fileName}" alt="${data.alt_text}">`;
            
            // 6. Create a temporary URL for the image and display it
            if (file) {
                const objectUrl = URL.createObjectURL(file);
                imagePreview.src = objectUrl;
                imagePreview.style.display = 'block'; 
            }

            // Reveal the hidden results div
            resultContainer.style.display = 'block';
        } else {
            // Handle errors returned by your Flask server
            altTextOutput.textContent = `Error: ${data.error}`;
            resultContainer.style.display = 'block';
        }
    } catch (error) {
        // Handle network errors (e.g., if your Flask server isn't running)
        console.error('Error:', error);
        altTextOutput.textContent = 'A network error occurred. Is your Python server running?';
        resultContainer.style.display = 'block';
    } finally {
        // 7. Reset the button state so the user can upload another image
        submitButton.textContent = 'Generate Alt Text';
        submitButton.disabled = false;
    }
});

// --- NEW: Copy to Clipboard Logic ---
document.getElementById('copyButton').addEventListener('click', async function() {
    const codeOutput = document.getElementById('htmlCodeOutput').textContent;
    const copyBtn = document.getElementById('copyButton');

    // Make sure there is actually text to copy
    if (!codeOutput) return;

    try {
        // Use the modern browser Clipboard API
        await navigator.clipboard.writeText(codeOutput);
        
        // Give the user visual feedback
        copyBtn.textContent = 'Copied!';
        copyBtn.style.backgroundColor = '#d4edda'; // Light green background
        copyBtn.style.color = '#155724'; // Dark green text
        
        // Reset the button after 2 seconds
        setTimeout(() => {
            copyBtn.textContent = 'Copy HTML';
            copyBtn.style.backgroundColor = ''; 
            copyBtn.style.color = '';
        }, 2000);

    } catch (err) {
        console.error('Failed to copy text: ', err);
        copyBtn.textContent = 'Error';
    }
});