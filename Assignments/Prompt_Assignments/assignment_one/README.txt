🌟 Overview
The Task Orchestrator is a high-performance, terminal-based productivity system. It is designed to manage complex workloads by prioritizing tasks through a Priority-First Scheduling (PFS) algorithm, ensuring that high-impact items never get buried under minor chores.

🚀 Key Features
Persistent Storage: All tasks are saved to tasks.json. You can close the program and your data remains safe.

Intelligent Sorting: Tasks are automatically ranked by Priority (High to Low) and then by Due Date (Earliest to Latest).

Dynamic ID Mapping: The ID numbers you see on screen always refer to the current view, making updates and deletions intuitive even after filtering.

Search & Filter: Find specific tasks using keywords or drill down into categories like "Done" or "High Priority."

Agenda Export: Generate a clean .txt file for your daily stand-ups or personal logs.


Option,Command,Description
[1],Add,"Create a new task. Requires a Title, Priority (1, 2, or 3), and Date (YYYY-MM-DD)."
[2],Update,"Change the status of a task (e.g., to ""In Progress"" or ""Done"")."
[3],Delete,Permanently remove a task from the system. Includes a safety confirmation.
[4],Filter,Toggle views based on specific Priority levels or Status keywords.
[5],Search,Instantly find tasks containing a specific word or phrase.
[6],Export,Save your current dashboard view to a timestamped text file.
[7],Exit,Safely close the application.


🛠️ Quick Start Guide
Installation: Ensure you have Python installed. Place task_manager.py in its own folder.

First Run: Open your terminal, navigate to the folder, and run:

Bash
python task_manager.py
Adding Tasks: Start by adding 3 tasks with different priorities. Notice how the system automatically re-orders them to put the most urgent item at the top (ID: 0).

The "Morning Routine": Use the Export feature every morning to create a "Focus List" for your day.