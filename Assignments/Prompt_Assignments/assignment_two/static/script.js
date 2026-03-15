document.addEventListener('DOMContentLoaded', () => {
    // 1. Smooth Scrolling for Navigation
    const navLinks = document.querySelectorAll('nav a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // 2. Project Card Hover Effect / Simple Animation
    const projectCards = document.querySelectorAll('.project-card');
    projectCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-5px)';
            card.style.transition = 'transform 0.3s ease';
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
        });
    });

    // 3. Dynamic Project Management (Add/Remove)
    const addProjectBtn = document.getElementById('add-project-btn');
    const projectList = document.getElementById('project-list');

    if (addProjectBtn && projectList) {
        addProjectBtn.addEventListener('click', () => {
            const newProject = document.createElement('div');
            newProject.className = 'project-entry';
            // Styling matches the updated edit.html structure
            newProject.style.cssText = 'margin-bottom: 20px; border: 1px solid #e2e8f0; padding: 15px; border-radius: 8px;';
            
            newProject.innerHTML = `
                <label style="font-size: 0.8rem;">Project Title</label>
                <input type="text" name="project_title[]" placeholder="Project Title" style="margin-bottom: 10px;">
                
                <label style="font-size: 0.8rem;">Project Description</label>
                <textarea name="project_desc[]" placeholder="Project Description" rows="2"></textarea>
                
                <button type="button" class="btn-remove" onclick="this.parentElement.remove()" style="color: #ef4444; border: none; background: none; cursor: pointer; font-size: 0.85rem; padding: 5px 0; font-weight: 600;">× Remove Project</button>
            `;
            projectList.appendChild(newProject);
            isDirty = true; // Mark form as changed
        });
    }

    // 4. Edit Form Logic: Validation & UX
    const profileForm = document.querySelector('.profile-form');
    let isDirty = false; 

    if (profileForm) {
        profileForm.addEventListener('input', () => {
            isDirty = true;
        });

        window.addEventListener('beforeunload', (e) => {
            if (isDirty) {
                e.preventDefault();
                e.returnValue = ''; 
            }
        });

        profileForm.addEventListener('submit', (e) => {
            const nameInput = document.getElementById('name');
            const submitBtn = profileForm.querySelector('.btn-primary');

            if (nameInput && nameInput.value.trim() === "") {
                e.preventDefault();
                nameInput.style.borderColor = "#ef4444";
                alert("The Name field is required.");
                return;
            }

            isDirty = false; 
            submitBtn.innerText = 'Saving...';
            submitBtn.style.opacity = '0.7';
            submitBtn.disabled = true;
        });
    }

    // 5. Modern Recommendation: Dark Mode Toggle
    const toggleDarkMode = () => {
        document.body.classList.toggle('dark-mode');
        const isDark = document.body.classList.contains('dark-mode');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    };

    // Initialize theme from local storage
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark-mode');
    }
});