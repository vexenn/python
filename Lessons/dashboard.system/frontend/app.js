const API_BASE_URL = "http://localhost:3000";

// ====================================================================
// SYSTEM MANAGEMENT INITIALIZATION LAYER
// ====================================================================
document.addEventListener("DOMContentLoaded", () => {
    // Check if user has a persistent system theme preference saved in browser storage
    if (localStorage.getItem("dashboard-theme") === "dark") {
        document.body.classList.add("dark-theme");
        const themeBtn = document.getElementById("theme-toggle-btn");
        if (themeBtn) themeBtn.innerText = "☀️ Light Mode";
    }
});

function toggleTheme() {
    const body = document.body;
    body.classList.toggle("dark-theme");
    const themeBtn = document.getElementById("theme-toggle-btn");
    
    if (body.classList.contains("dark-theme")) {
        themeBtn.innerText = "☀️ Light Mode";
        localStorage.setItem("dashboard-theme", "dark");
    } else {
        themeBtn.innerText = "🌙 Dark Mode";
        localStorage.setItem("dashboard-theme", "light");
    }
}

// ====================================================================
// AUTHENTICATION FRAMEWORK MANAGEMENT SUBSYSTEM
// ====================================================================
async function handleRegister() {
    const user = document.getElementById("auth-username").value.trim();
    const pass = document.getElementById("auth-password").value.trim();
    const msg = document.getElementById("auth-message");

    if (!user || !pass) return showStatus(msg, "Username and password parameters required.", false);

    try {
        const res = await fetch(`${API_BASE_URL}/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: user, password: pass })
        });
        const data = await res.json();

        if (res.status === 201) {
            showStatus(msg, "Account registered successfully! You may now sign in.", true);
        } else {
            showStatus(msg, data.message || "Registration sequence failed.", false);
        }
    } catch (err) {
        showStatus(msg, "Network communication mismatch with authorization server.", false);
    }
}

async function handleLogin() {
    const user = document.getElementById("auth-username").value.trim();
    const pass = document.getElementById("auth-password").value.trim();
    const msg = document.getElementById("auth-message");

    try {
        const res = await fetch(`${API_BASE_URL}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: user, password: pass })
        });
        const data = await res.json();

        if (res.ok) {
            document.getElementById("auth-container").classList.add("hidden");
            document.getElementById("dashboard-workspace").classList.remove("hidden");
            synchronizeDashboardContext();
        } else {
            showStatus(msg, data.message || "Credential verification rejection.", false);
        }
    } catch (err) {
        showStatus(msg, "System connection fault during authentication clearance.", false);
    }
}

function handleLogout() {
    document.getElementById("auth-username").value = "";
    document.getElementById("auth-password").value = "";
    document.getElementById("auth-message").innerText = "";
    document.getElementById("dashboard-workspace").classList.add("hidden");
    document.getElementById("auth-container").classList.remove("hidden");
}

// ====================================================================
// CORE SYSTEM CONTEXT DATA SYNCHRONIZATION DATA LOOP
// ====================================================================
function synchronizeDashboardContext() {
    fetchStudentDirectory();
    fetchDashboardMetrics();
    fetchHonorsDirectory();
    fetchAttendanceRiskRegistry();
}

// ====================================================================
// CRUD & ANALYTICS FETCH MANAGEMENT OPERATIONS
// ====================================================================
async function fetchStudentDirectory() {
    try {
        const res = await fetch(`${API_BASE_URL}/students`);
        const students = await res.json();
        renderTableRows(students);
    } catch (err) {
        console.error("Critical error building student index view matrix:", err);
    }
}

async function fetchDashboardMetrics() {
    try {
        const res = await fetch(`${API_BASE_URL}/analytics`);
        const data = await res.json();
        document.getElementById("metric-total").innerText = data.totalStudents;
        document.getElementById("metric-pass").innerText = data.passCount;
        document.getElementById("metric-fail").innerText = data.failCount;
        document.getElementById("metric-avg").innerText = `${data.averageMarks}%`;
    } catch (err) {
        console.error("Metrics aggregation network cycle collision:", err);
    }
}

async function fetchHonorsDirectory() {
    try {
        const res = await fetch(`${API_BASE_URL}/toppers`);
        const toppers = await res.json();
        const container = document.getElementById("toppers-list");
        container.innerHTML = toppers.map(s => `<li><span class="badge badge-pass">A</span> <strong>${s.name}</strong> (${s.marks} Marks)</li>`).join("");
    } catch (err) {
        console.error("Honors compilation network exception:", err);
    }
}

async function fetchAttendanceRiskRegistry() {
    try {
        const res = await fetch(`${API_BASE_URL}/low-attendance`);
        const riskList = await res.json();
        const container = document.getElementById("low-attendance-list");
        container.innerHTML = riskList.map(s => `<li><span class="badge badge-fail">${s.grade}</span> <strong>${s.name}</strong> (${s.attendance}% Attendance)</li>`).join("");
    } catch (err) {
        console.error("Risk registry compilation network exception:", err);
    }
}

async function searchStudentDirectory() {
    const query = document.getElementById("search-input").value.trim();
    if (!query) return fetchStudentDirectory();

    try {
        const res = await fetch(`${API_BASE_URL}/search?name=${encodeURIComponent(query)}`);
        const matches = await res.json();
        renderTableRows(matches);
    } catch (err) {
        console.error("Search string serialization transmission failure:", err);
    }
}

async function saveStudent() {
    const id = document.getElementById("student-id-tracker").value;
    const name = document.getElementById("name").value.trim();
    const marks = Number(document.getElementById("marks").value);
    const attendance = Number(document.getElementById("attendance").value);
    const formStatus = document.getElementById("form-status");

    if (!name || isNaN(marks) || isNaN(attendance)) {
        return showStatus(formStatus, "All tracking parameter fields are strictly mandatory.", false);
    }

    const payload = { name, marks, attendance };
    const url = id ? `${API_BASE_URL}/student/${id}` : `${API_BASE_URL}/student`;
    const method = id ? "PUT" : "POST";

    try {
        const res = await fetch(url, {
            method: method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const data = await res.json();

        if (res.ok) {
            showStatus(formStatus, data.message, true);
            clearStudentForm();
            synchronizeDashboardContext();
        } else {
            showStatus(formStatus, data.message || "Record compilation rejection execution status.", false);
        }
    } catch (err) {
        showStatus(formStatus, "Network timeout connecting to transaction endpoint configuration.", false);
    }
}

async function deleteStudent(id) {
    if (!confirm("Are you certain you want to permanently scrub this tracking record from index files?")) return;

    try {
        const res = await fetch(`${API_BASE_URL}/student/${id}`, { method: "DELETE" });
        if (res.ok) {
            synchronizeDashboardContext();
        } else {
            alert("Administrative row deletion target operation was blocked by core.");
        }
    } catch (err) {
        console.error("Deletion lifecycle networking transmission exception:", err);
    }
}

// ====================================================================
// PRESENTATION RENDERING CORE MUTATION INTERACTION LAYERS
// ====================================================================
function renderTableRows(studentArray) {
    const tbody = document.getElementById("directory-table-body");
    if (studentArray.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" class="empty-placeholder">No active records match the current database view window filters.</td></tr>`;
        return;
    }

    tbody.innerHTML = studentArray.map(student => {
        const resultClass = student.result.includes("Pass") ? "status-pass" : "status-fail";
        return `
            <tr>
                <td><strong>#${student.id}</strong></td>
                <td>${student.name}</td>
                <td>${student.marks} / 100</td>
                <td>${student.attendance}%</td>
                <td><span class="table-grade">${student.grade}</span></td>
                <td><span class="status-indicator ${resultClass}">${student.result}</span></td>
                <td>
                    <div class="row-actions">
                        <button onclick="prepareUpdateStudent(${student.id}, '${student.name}', ${student.marks}, ${student.attendance})" class="btn-edit-tool">Modify</button>
                        <button onclick="deleteStudent(${student.id})" class="btn-delete-tool">Scrub</button>
                    </div>
                </td>
            </tr>
        `;
    }).join("");
}

function prepareUpdateStudent(id, name, marks, attendance) {
    document.getElementById("student-id-tracker").value = id;
    document.getElementById("name").value = name;
    document.getElementById("marks").value = marks;
    document.getElementById("attendance").value = attendance;

    document.getElementById("form-heading").innerText = `Modify Student Profile #${id}`;
    document.getElementById("form-submit-btn").innerText = "Apply Record Changes";
    document.getElementById("form-cancel-btn").classList.remove("hidden");
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function clearStudentForm() {
    document.getElementById("student-id-tracker").value = "";
    document.getElementById("name").value = "";
    document.getElementById("marks").value = "";
    document.getElementById("attendance").value = "";

    document.getElementById("form-heading").innerText = "Add New Student Profile";
    document.getElementById("form-submit-btn").innerText = "Save Profile Record";
    document.getElementById("form-cancel-btn").classList.add("hidden");
    document.getElementById("form-status").innerText = "";
}

function showStatus(element, text, isSuccess) {
    element.innerText = text;
    element.className = `status-msg ${isSuccess ? "success-text" : "error-text"}`;
}