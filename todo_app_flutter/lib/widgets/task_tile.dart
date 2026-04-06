import 'package:flutter/material.dart';
import '../models/task.dart';

class TaskTile extends StatelessWidget {
  final Task task;
  final VoidCallback onComplete; // Renamed from onDelete for clarity

  const TaskTile({super.key, required this.task, required this.onComplete});

  // Helper to get the "Glow" color for each rarity
  Color _getRarityColor() {
    switch (task.rarity) {
      case TaskRarity.common: return Colors.grey;
      case TaskRarity.rare: return Colors.blueAccent;
      case TaskRarity.epic: return Colors.purpleAccent;
      case TaskRarity.legendary: return Colors.orangeAccent;
    }
  }

  @override
  Widget build(BuildContext context) {
    final rarityColor = _getRarityColor();

    return Card(
      elevation: 4,
      margin: const EdgeInsets.symmetric(vertical: 8),
      // UI Trick: Use a border side to show rarity
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: BorderSide(color: rarityColor, width: 2),
      ),
      child: ListTile(
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        leading: Icon(Icons.shield, color: rarityColor), // Icon based on rarity
        title: Text(
          task.title,
          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
        ),
        subtitle: Text(
          task.rarity.name.toUpperCase(),
          style: TextStyle(color: rarityColor, letterSpacing: 1.2, fontSize: 12),
        ),
        // The "Complete Quest" button
        trailing: IconButton(
          icon: const Icon(Icons.check_circle_outline, color: Colors.greenAccent, size: 30),
          onPressed: onComplete, 
          tooltip: 'Complete Quest',
        ),
      ),
    );
  }
}