Quest Log: A Gamified Productivity HUD

Vision

Quest Log is a Flutter-based task management system that replaces the mundane "To-Do" list with an RPG-inspired progression system. Developed with a "Game-First" mindset, it utilizes standard mobile development patterns to create an engaging user loop of effort and reward.

Technical Stack
Framework: Flutter (Material 3)

Language: Dart

Persistence: shared_preferences (Local I/O)

Data Format: JSON Serialization

Key Logic Pillars

1. The RPG Progression System
The app utilizes a custom Rarity Engine. Each task is assigned a TaskRarity enum which determines its value within the game loop.

- Rarity Tiers: Common (+10 XP), Rare (+25 XP), Epic (+50 XP), Legendary (+100 XP).

- Leveling Formula: $XP_{required} = Level \times 100$.

- XP Carry-over: When a user levels up, leftover XP is subtracted from the next level's requirement to ensure no progress is lost.


2. State Management & Communication
The architecture follows a Decoupled Widget pattern:

The Controller (TodoScreen): Holds the master state, handles leveling logic, and coordinates data saving.

The Input (TaskInput): Uses a callback pattern (onAdd) to pass data from a stateless text field/dropdown up to the main state.

The Display (TaskTile): A modular component that renders itself dynamically based on the Task object's properties (rarity, title, etc.).

3. Persistence Layer
To ensure a seamless user experience, the app implements Local Data Persistence:

Serialization: Custom toJson() and fromJson() methods in the Task model convert complex Dart objects into strings.

Disk I/O: Utilizes the SharedPreferences API to store the JSON string, user level, and XP totals, ensuring progress survives an app restart.


4. Dynamic Theming HUD
The UI reacts to the user's progress. The XP Bar uses a custom _getXPBarColor() method that checks two conditions:

The Active Theme: (e.g., Cyberpunk Cyan vs. Pastel Green).

The User Rank: Once a user reaches Level 10, the bar undergoes a "Prestige" color shift (e.g., from Cyan to Pink) to provide visual prestige.

UI/UX Highlights
Visual Feedback: Cards use shadowColor and BorderSide to create a "Glow" effect that matches the item's rarity.

Non-Destructive Actions: Swiping left to "Abandon" a quest triggers an Undo SnackBar, protecting users from accidental data loss.

Success States: The LevelUpDialog provides immediate positive reinforcement, closing the dopamine loop and encouraging further productivity.


