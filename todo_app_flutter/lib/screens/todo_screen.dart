import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/task.dart';
import '../widgets/task_tile.dart';
import '../widgets/task_input.dart';

class TodoScreen extends StatefulWidget {
  final String currentTheme; 
  final Function(String) onThemeChanged;

  const TodoScreen({
    super.key,
    required this.onThemeChanged,
    required this.currentTheme,
  });

  @override
  State<TodoScreen> createState() => _TodoScreenState();
}

class _TodoScreenState extends State<TodoScreen> {
  List<Task> _tasks = [];
  int _userXP = 0;
  int _userLevel = 1;

  @override
  void initState() {
    super.initState();
    _loadTasks();
    _loadUserStats();
  }

  // --- GAMIFICATION LOGIC ---

  void _completeTask(int index, Task task) {
    int xpGain = 0;
    switch (task.rarity) {
      case TaskRarity.common: xpGain = 10; break;
      case TaskRarity.rare: xpGain = 25; break;
      case TaskRarity.epic: xpGain = 50; break;
      case TaskRarity.legendary: xpGain = 100; break;
    }

    setState(() {
      _userXP += xpGain;
      _tasks.removeAt(index);
      if (_userXP >= _userLevel * 100) {
        _userXP -= (_userLevel * 100);
        _userLevel++;
        _showLevelUpDialog();
      }
    });
    _saveTasks();
    _saveUserStats();
  }

  void _showLevelUpDialog() {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text("LEVEL UP! 🎊", textAlign: TextAlign.center),
        content: Text("You reached Level $_userLevel!\nYour efficiency is legendary."),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(),
            child: const Text("Keep Grinding"),
          ),
        ],
      ),
    );
  }

  // --- PERSISTENCE LOGIC ---

  Future<void> _saveUserStats() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt('user_xp', _userXP);
    await prefs.setInt('user_level', _userLevel);
  }

  Future<void> _loadUserStats() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      _userXP = prefs.getInt('user_xp') ?? 0;
      _userLevel = prefs.getInt('user_level') ?? 1;
    });
  }

  Future<void> _saveTasks() async {
    final prefs = await SharedPreferences.getInstance();
    final String encodedData = jsonEncode(_tasks.map((t) => t.toJson()).toList());
    await prefs.setString('user_tasks', encodedData);
  }

  Future<void> _loadTasks() async {
    final prefs = await SharedPreferences.getInstance();
    final String? tasksString = prefs.getString('user_tasks');
    if (tasksString != null) {
      final List<dynamic> decodedData = jsonDecode(tasksString);
      setState(() {
        _tasks = decodedData.map((item) => Task.fromJson(item)).toList();
      });
    }
  }

  void _addTask(String title, TaskRarity rarity) {
    setState(() {
      _tasks.add(Task(
        id: DateTime.now().toString(),
        title: title,
        rarity: rarity,
      ));
    });
    _saveTasks();
  }

  void _deleteTaskWithUndo(int index, Task task) {
    final deletedTask = task;
    setState(() { _tasks.removeAt(index); });
    _saveTasks();

    ScaffoldMessenger.of(context).clearSnackBars();
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('Abandoned "${deletedTask.title}"'),
        action: SnackBarAction(
          label: 'UNDO',
          onPressed: () {
            setState(() { _tasks.insert(index, deletedTask); });
            _saveTasks();
          },
        ),
      ),
    );
  }

  // --- UI BUILDING BLOCKS ---

  Color _getXPBarColor() {
    bool isHighLevel = _userLevel >= 10;
    switch (widget.currentTheme) {
      case 'Cyberpunk':
        // Standardized to pinkAccent for Cyberpunk theme
        return isHighLevel ? Colors.pinkAccent : Colors.cyanAccent;
      case 'Pastel Garden':
        return isHighLevel ? Colors.orange[200]! : Colors.lightGreen[300]!;
      case 'Classic Blue':
      default:
        return isHighLevel ? Colors.amber : Colors.lightBlueAccent;
    }
  }

  Widget _buildXPBar() {
    double progress = _userXP / (_userLevel * 100);
    Color barColor = _getXPBarColor();

    return Card(
      elevation: 8,
      // Using .withValues to stay up-to-date with Flutter 3.27+ standards
      shadowColor: barColor.withValues(alpha: 0.5), 
      color: barColor.withValues(alpha: 0.1),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  "LVL $_userLevel", 
                  style: TextStyle(fontWeight: FontWeight.bold, color: barColor, fontSize: 18)
                ),
                Text("$_userXP / ${_userLevel * 100} XP"),
              ],
            ),
            const SizedBox(height: 12),
            ClipRRect(
              borderRadius: BorderRadius.circular(10),
              child: LinearProgressIndicator(
                value: progress,
                minHeight: 12,
                backgroundColor: barColor.withValues(alpha: 0.1),
                valueColor: AlwaysStoppedAnimation<Color>(barColor),
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Quest Log'),
        centerTitle: true,
        actions: [
          PopupMenuButton<String>(
            icon: const Icon(Icons.palette),
            onSelected: widget.onThemeChanged,
            itemBuilder: (ctx) => ['Classic Blue', 'Cyberpunk', 'Pastel Garden']
                .map((c) => PopupMenuItem(value: c, child: Text(c)))
                .toList(),
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            _buildXPBar(), 
            const SizedBox(height: 20),
            TaskInput(onAdd: _addTask),
            const SizedBox(height: 20),
            Expanded(
              child: _tasks.isEmpty
                  ? const Center(child: Text('No active quests.'))
                  : ListView.builder(
                      itemCount: _tasks.length,
                      itemBuilder: (ctx, index) {
                        final task = _tasks[index];
                        return Dismissible(
                          key: Key(task.id),
                          direction: DismissDirection.endToStart,
                          onDismissed: (_) => _deleteTaskWithUndo(index, task),
                          background: Container(
                            color: Colors.redAccent, 
                            alignment: Alignment.centerRight, 
                            padding: const EdgeInsets.only(right: 20),
                            child: const Icon(Icons.delete_forever, color: Colors.white)
                          ),
                          child: TaskTile(
                            task: task,
                            onComplete: () => _completeTask(index, task), 
                          ),
                        );
                      },
                    ),
            ),
          ],
        ),
      ),
    );
  }
}