document.addEventListener('DOMContentLoaded', () => {
    const taskList = document.getElementById('taskList');
    const addBtn = document.getElementById('addBtn');

    // 1. Load existing tasks from the Database
    fetch('/tasks')
        .then(res => res.json())
        .then(tasks => tasks.forEach(task => renderTask(task)));

    // 2. Function to Add a Task
    addBtn.addEventListener('click', async () => {
        const title = document.getElementById('taskTitle').value;
        const comment = document.getElementById('taskComment').value;

        if (!title) return alert("Task title is required!");

        const response = await fetch('/tasks', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, comment })
        });

        const newTask = await response.json();
        renderTask(newTask);

        // Clear inputs
        document.getElementById('taskTitle').value = '';
        document.getElementById('taskComment').value = '';
    });

    // 3. Function to Render a Task in the UI
    function renderTask(task) {
        const li = document.createElement('li');
        li.className = 'task-item';
        li.id = `task-${task.id}`;

        li.innerHTML = `
            <div class="task-content">
                <span class="title">${task.title}</span>
                <span class="comment">${task.comment || 'No comment'}</span>
            </div>
            <div class="actions">
                <button class="remove-btn" id="rm-${task.id}">Remove</button>
                <button class="confirm-btn" id="cf-${task.id}">Are you sure?</button>
            </div>
        `;

        taskList.appendChild(li);

        // Confirmation Logic
        const removeBtn = li.querySelector('.remove-btn');
        const confirmBtn = li.querySelector('.confirm-btn');

        removeBtn.addEventListener('click', () => {
            confirmBtn.style.display = 'inline-block';
            removeBtn.style.display = 'none';
        });

        confirmBtn.addEventListener('click', async () => {
            // Trigger Fade Out Animation
            li.style.animation = 'fadeOut 0.3s forwards';
            
            // Delete from Database
            await fetch(`/tasks/${task.id}`, { method: 'DELETE' });
            
            // Remove from HTML after animation
            setTimeout(() => li.remove(), 300);
        });
    }
});