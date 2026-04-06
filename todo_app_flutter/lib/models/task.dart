enum TaskRarity { common, rare, epic, legendary }

class Task {
  final String id;
  final String title;
  final TaskRarity rarity;
  bool isCompleted;

  Task({
    required this.id, 
    required this.title, 
    this.rarity = TaskRarity.common,
    this.isCompleted = false,
  });

  Map<String, dynamic> toJson() => {
        'id': id,
        'title': title,
        'rarity': rarity.index, // Store as integer
        'isCompleted': isCompleted,
      };

  factory Task.fromJson(Map<String, dynamic> json) => Task(
        id: json['id'],
        title: json['title'],
        rarity: TaskRarity.values[json['rarity'] ?? 0],
        isCompleted: json['isCompleted'] ?? false,
      );
}