import 'package:flutter/material.dart';
import 'package:notes_app/core/network/dio_client.dart';
import 'package:notes_app/core/storage/token_storage.dart';
import 'package:notes_app/data/api/note_api.dart';

class NotesPage extends StatefulWidget {
  const NotesPage({super.key});

  @override
  State<NotesPage> createState() => _NotesPageState();
}

class _NotesPageState extends State<NotesPage> {
  List notes = [];

  @override
  void initState() {
    super.initState();
    loadNotes();
  }

  void loadNotes() async {
    final storage = TokenStorage();
    final client = DioClient(() => storage.getToken());
    final api = NoteApi(client.dio);

    final data = await api.getNotes();

    setState(() {
      notes = data;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Notes")),
      body: ListView.builder(
        itemCount: notes.length,
        itemBuilder: (_, index) {
          final note = notes[index];
          return ListTile(
            title: Text(note["title"]),
            subtitle: Text(note["content"]),
          );
        },
      ),
    );
  }
}