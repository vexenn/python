import os
import json
from datetime import datetime

class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.priority_map = {1: "🔴 HIGH", 2: "🟡 MED", 3: "🟢 LOW"}
        self.current_filter = None
        self.search_query = None  # New: search state
        self.load_from_file()

    def save_to_file(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.tasks, f, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

    def load_from_file(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    self.tasks = json.load(f)
            except Exception as e:
                print(f"Error loading: {e}. Starting fresh.")
                self.tasks = []

    def get_processed_tasks(self):
        """Applies filters, then search queries, then sorts the list."""
        processed = self.tasks
        
        # 1. Apply Search
        if self.search_query:
            processed = [t for t in processed if self.search_query.lower() in t['title'].lower()]
        
        # 2. Apply Filters
        if self.current_filter:
            f_type, f_val = self.current_filter
            if f_type == "priority":
                processed = [t for t in processed if t['priority'] == int(f_val)]
            elif f_type == "status":
                processed = [t for t in processed if t['status'] == f_val.upper()]
        
        return sorted(processed, key=lambda x: (x['priority'], x['due_date']))

    def set_filter(self, filter_type, value):
        self.current_filter = None if filter_type == "none" else (filter_type, value)

    def set_search(self, query):
        self.search_query = query if query else None

    def add_task(self, title, priority, due_date):
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
            task = {"title": title, "priority": int(priority), "due_date": due_date, "status": "PENDING"}
            self.tasks.append(task)
            self.save_to_file()
            print(f"\n✅ Task '{title}' added!")
        except ValueError:
            print("\n❌ Error: Invalid format.")

    def update_status(self, display_id, new_status):
        visible_tasks = self.get_processed_tasks()
        if 0 <= display_id < len(visible_tasks):
            target = visible_tasks[display_id]
            for task in self.tasks:
                if task == target:
                    task["status"] = new_status.upper()
                    break
            self.save_to_file()
            print("\n✅ Status updated.")
        else:
            print("\n❌ ID not found.")

    def delete_task(self, display_id):
        visible_tasks = self.get_processed_tasks()
        if 0 <= display_id < len(visible_tasks):
            target = visible_tasks[display_id]
            self.tasks.remove(target)
            self.save_to_file()
            print(f"\n🗑️ Deleted: {target['title']}")
        else:
            print("\n❌ ID not found.")

    def export_agenda(self):
        visible_tasks = self.get_processed_tasks()
        filename = f"agenda_{datetime.now().strftime('%Y-%m-%d')}.txt"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"📅 DAILY AGENDA - {datetime.now().strftime('%B %d, %Y')}\n")
                f.write("="*60 + "\n")
                for t in visible_tasks:
                    p = self.priority_map.get(t['priority'], "LOW")
                    f.write(f"[{t['status']}] {p} | {t['title']} (Due: {t['due_date']})\n")
                f.write("="*60 + "\n")
            print(f"\n📄 Agenda exported to {filename}!")
        except Exception as e:
            print(f"Export failed: {e}")

    def display_dashboard(self):
        visible_tasks = self.get_processed_tasks()
        status_info = []
        if self.current_filter: status_info.append(f"FILTER: {self.current_filter}")
        if self.search_query: status_info.append(f"SEARCH: '{self.search_query}'")
        
        header = f"📋 TASK DASHBOARD {' | '.join(status_info)}" if status_info else "📋 TASK DASHBOARD"
        
        print("\n" + "="*75)
        print(header)
        print("-" * 75)
        if not visible_tasks:
            print("No tasks matching this view.")
        else:
            print(f"{'ID':<4} | {'TASK TITLE':<25} | {'PRIORITY':<10} | {'DUE DATE':<12} | {'STATUS':<12}")
            print("-" * 75)
            for i, task in enumerate(visible_tasks):
                p_label = self.priority_map.get(task['priority'], "???")
                print(f"{i:<4} | {task['title']:<25} | {p_label:<10} | {task['due_date']:<12} | {task['status']:<12}")
        print("="*75 + "\n")

def main():
    tm = TaskManager()
    while True:
        tm.display_dashboard()
        print("CMDS: [1] Add [2] Update [3] Del [4] Filter [5] Search [6] Export [7] Exit")
        choice = input("Select: ")

        if choice == "1":
            tm.add_task(input("Title: "), input("Priority (1-3): "), input("Date (YYYY-MM-DD): "))
        elif choice == "2":
            try: tm.update_status(int(input("ID: ")), input("New Status: "))
            except: print("Invalid ID.")
        elif choice == "3":
            try: tm.delete_task(int(input("ID: ")))
            except: print("Invalid ID.")
        elif choice == "4":
            f_choice = input("\nFILTER: [P] Priority [S] Status [C] Clear: ").lower()
            if f_choice == 'p': tm.set_filter("priority", input("Enter 1, 2, or 3: "))
            elif f_choice == 's': tm.set_filter("status", input("Enter Status: "))
            else: tm.set_filter("none", None)
        elif choice == "5":
            query = input("Enter search keyword (or leave blank to clear): ")
            tm.set_search(query)
        elif choice == "6":
            tm.export_agenda()
        elif choice == "7":
            print("Session saved. Goodbye!")
            break

if __name__ == "__main__":
    main()