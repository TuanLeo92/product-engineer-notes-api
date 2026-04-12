import 'package:flutter/material.dart';
import 'package:notes_app/core/network/dio_client.dart';
import 'package:notes_app/core/storage/token_storage.dart';
import 'package:notes_app/data/api/auth_api.dart';
import 'package:notes_app/data/api/note_api.dart';
import 'package:notes_app/presentation/notes_page.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {

  @override
  void initState() {
    super.initState();
    testLogin();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Notes App',
      home: Builder(
        builder: (navContext) => Scaffold(
          appBar: AppBar(title: const Text('Notes')),
          body: Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Text('App Started'),
                TextButton(
                  onPressed: () => Navigator.of(navContext).push(
                    MaterialPageRoute<void>(
                      builder: (context) => const NotesPage(),
                    ),
                  ),
                  child: const Text('Notes'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  void testLogin() async {
    final storage = TokenStorage();
    final client = DioClient(() async => await storage.getToken());

    final noteApi = NoteApi(client.dio);
    final api = AuthApi(client.dio);
    final email = "tuan.le@gmail.com";
    final token = await api.login(email, "123456");

    print("Logged in: ${email}");
    print("Token: ${token}");
    await storage.setToken(token);

    final notes = await noteApi.getNotes();
    print("Notes: ${notes}");
 }
}