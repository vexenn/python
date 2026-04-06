import 'package:flutter/material.dart';
import 'screens/todo_screen.dart';

// 1. Theme Definitions (Keep these outside the class for easy access)
final Map<String, ThemeData> appThemes = {
  'Classic Blue': ThemeData(
    useMaterial3: true,
    colorSchemeSeed: Colors.blue,
    brightness: Brightness.light,
  ),
  'Cyberpunk': ThemeData(
    useMaterial3: true,
    brightness: Brightness.dark,
    colorScheme: ColorScheme.fromSeed(
      seedColor: Colors.cyan,
      brightness: Brightness.dark,
      primary: Colors.cyanAccent,
      surface: Colors.black,
    ),
    scaffoldBackgroundColor: const Color(0xFF0D0208),
  ),
  'Pastel Garden': ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(
      seedColor: Colors.greenAccent,
      primary: Colors.pinkAccent,
      secondary: Colors.teal,
      surface: const Color(0xFFF1F8E9),
    ),
    scaffoldBackgroundColor: const Color(0xFFF1F8E9),
  ),
};

void main() {
  runApp(const TodoApp());
}

class TodoApp extends StatefulWidget {
  const TodoApp({super.key});

  @override
  State<TodoApp> createState() => _TodoAppState();
}

class _TodoAppState extends State<TodoApp> {
  String _currentThemeKey = 'Classic Blue';

  void _changeTheme(String themeKey) {
    setState(() {
      _currentThemeKey = themeKey;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Flutter To-Do',
      theme: appThemes[_currentThemeKey],
      // FIX: We are now passing the String key so TodoScreen knows which theme is active
      home: TodoScreen(
        onThemeChanged: _changeTheme,
        currentTheme: _currentThemeKey, 
      ),
    );
  }
}