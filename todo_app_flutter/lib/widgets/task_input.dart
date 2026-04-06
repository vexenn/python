import 'package:flutter/material.dart';
import '../models/task.dart'; // To access TaskRarity

class TaskInput extends StatefulWidget {
  final Function(String, TaskRarity) onAdd; 

  const TaskInput({super.key, required this.onAdd});

  @override
  State<TaskInput> createState() => _TaskInputState();
}

class _TaskInputState extends State<TaskInput> {
  final TextEditingController _controller = TextEditingController();
  TaskRarity _selectedRarity = TaskRarity.common;

  void _submitData() {
    final enteredText = _controller.text;
    if (enteredText.isEmpty) return;

    // Logic: Pass both values to the TodoScreen
    widget.onAdd(enteredText, _selectedRarity); 
    
    _controller.clear();
    setState(() {
      _selectedRarity = TaskRarity.common; // Reset rarity after adding
    });
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 0,
      color: Colors.transparent,
      child: Row(
        children: [
          Expanded(
            child: TextField(
              controller: _controller,
              decoration: const InputDecoration(
                labelText: 'New Quest Name...',
                border: OutlineInputBorder(),
              ),
              onSubmitted: (_) => _submitData(),
            ),
          ),
          const SizedBox(width: 10),
          // Rarity Selector Dropdown
          DropdownButton<TaskRarity>(
            value: _selectedRarity,
            items: TaskRarity.values.map((rarity) {
              return DropdownMenuItem(
                value: rarity,
                child: Text(
                  rarity.name.toUpperCase(),
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                    color: _getRarityColor(rarity),
                  ),
                ),
              );
            }).toList(),
            onChanged: (value) {
              setState(() {
                _selectedRarity = value!;
              });
            },
          ),
          const SizedBox(width: 10),
          ElevatedButton(
            onPressed: _submitData,
            style: ElevatedButton.styleFrom(
              padding: const EdgeInsets.all(16),
            ),
            child: const Icon(Icons.add),
          ),
        ],
      ),
    );
  }

  // UI Hint: Helper to show rarity colors in the dropdown
  Color _getRarityColor(TaskRarity rarity) {
    switch (rarity) {
      case TaskRarity.common: return Colors.grey;
      case TaskRarity.rare: return Colors.blue;
      case TaskRarity.epic: return Colors.purple;
      case TaskRarity.legendary: return Colors.orange;
    }
  }
}