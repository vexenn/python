document.getElementById('travel-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const destination = document.getElementById('destination').value;
    const duration = document.getElementById('duration').value;
    const preferences = document.getElementById('preferences').value;
    
    const loadingDiv = document.getElementById('loading');
    const itineraryContainer = document.getElementById('itinerary-container');
    const submitBtn = document.getElementById('submit-btn');

    // UI Updates
    loadingDiv.classList.remove('hidden');
    itineraryContainer.classList.add('hidden');
    submitBtn.disabled = true;

    try {
        const response = await fetch('/generate_itinerary', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ destination, duration, preferences }),
        });

        const data = await response.json();

        if (response.ok) {
            renderItinerary(data);
            itineraryContainer.classList.remove('hidden');
        } else {
            alert(data.error || "Something went wrong.");
        }
    } catch (error) {
        console.error("Error fetching itinerary:", error);
        alert("Failed to connect to the server.");
    } finally {
        loadingDiv.classList.add('hidden');
        submitBtn.disabled = false;
    }
});

function renderItinerary(data) {
    const content = document.getElementById('itinerary-content');
    let html = `<h2>Trip to ${data.destination}</h2>`;

    // Emergency Info
    html += `
        <div class="card emergency-card">
            <h3>🚨 Emergency Info</h3>
            <p><strong>Police:</strong> ${data.emergency_info.police}</p>
            <p><strong>Ambulance:</strong> ${data.emergency_info.ambulance}</p>
            <p><strong>Fire:</strong> ${data.emergency_info.fire}</p>
            <p><em>Tip:</em> ${data.emergency_info.embassy_tip}</p>
        </div>
    `;

    // Where to Stay
    html += `<h3>Suggested Neighborhoods</h3><div class="neighborhoods">`;
    data.suggested_areas_to_stay.forEach(area => {
        html += `
            <div class="card">
                <h4>${area.neighborhood} (${area.price_tier} Budget)</h4>
                <p>${area.vibe}</p>
            </div>
        `;
    });
    html += `</div>`;

    // Daily Itinerary
    data.itinerary.forEach(day => {
        html += `<div class="day-card">
                    <h3>Day ${day.day}: ${day.theme}</h3>`;
        
        // Activities
        html += `<h4>Activities</h4><ul>`;
        day.activities.forEach(act => {
            html += `
                <li>
                    <strong>${act.time_of_day}: ${act.name}</strong> (${act.type} - ${act.estimated_cost})<br>
                    ${act.description}
                </li>`;
        });
        html += `</ul>`;

        // Dining
        html += `<h4>Dining Suggestions</h4><ul>`;
        day.dining_suggestions.forEach(meal => {
            html += `
                <li>
                    <strong>${meal.meal}: ${meal.name}</strong> (${meal.cuisine})<br>
                    <em>${meal.type}</em> - ${meal.description}
                </li>`;
        });
        html += `</ul></div>`;
    });

    content.innerHTML = html;
}

// Enhanced PDF Export Logic
document.getElementById('export-btn').addEventListener('click', async function() {
    const btn = this;
    const originalText = btn.innerText;
    
    // 1. Give the user visual feedback so they know it's working
    btn.innerText = "Generating PDF (Please wait)...";
    btn.disabled = true;

    try {
        const element = document.getElementById('itinerary-content');
        const opt = {
            margin:       0.5,
            filename:     'My_Travel_Itinerary.pdf',
            image:        { type: 'jpeg', quality: 0.98 },
            html2canvas:  { scale: 2, useCORS: true },
            jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' },
            // Add this line to enforce clean page breaks!
            pagebreak:    { mode: ['avoid-all', 'css', 'legacy'] } 
        };
        
        // 2. Await the promise to catch any hidden errors
        await html2pdf().set(opt).from(element).save();
        
    } catch (error) {
        // 3. Log the exact error to the console if it fails
        console.error("PDF Export failed:", error);
        alert("Failed to generate PDF. Press F12 to check the console for details.");
    } finally {
        // 4. Reset the button
        btn.innerText = originalText;
        btn.disabled = false;
    }
});