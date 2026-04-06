import 'package:flutter_test/flutter_test.dart';
import 'package:todo_app_flutter/main.dart'; // Ensure this matches your project name

void main() {
  testWidgets('Quest Log smoke test', (WidgetTester tester) async {
    // 1. Build our app and trigger a frame.
    // We use TodoApp() because that is the class name in your main.dart
    await tester.pumpWidget(const TodoApp());

    // 2. Verify that our app starts with the correct title.
    expect(find.text('Quest Log'), findsOneWidget);

    // 3. Verify that the initial empty state message is shown.
    expect(find.text('No active quests.'), findsOneWidget);
  });
}