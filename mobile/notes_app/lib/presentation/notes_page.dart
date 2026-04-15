import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:notes_app/core/network/dio_client.dart';
import 'package:notes_app/core/storage/token_storage.dart';
import 'package:notes_app/data/api/note_api.dart';
import 'package:notes_app/data/repositories/note_repository.dart';
import 'package:notes_app/domain/usecases/get_notes_use_case.dart';
import 'package:notes_app/presentation/bloc/note_bloc.dart';

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
      body: BlocProvider(
  create: (_) {
    final storage = TokenStorage();
    final client = DioClient(() => storage.getToken());
    final api = NoteApi(client.dio);
    final repo = NoteRepository(api);
    final usecase = GetNotesUseCase(repo);

    return NoteBloc(usecase)..add(LoadNotes());
  },
  child: BlocBuilder<NoteBloc, NoteState>(
    builder: (context, state) {
      if (state is NoteLoading) {
        return const Center(child: CircularProgressIndicator());
      }

      if (state is NoteLoaded) {
        return ListView.builder(
          itemCount: state.notes.length,
          itemBuilder: (_, index) {
            final note = state.notes[index];
            return ListTile(
              title: Text(note.title),
              subtitle: Text(note.content),
            );
          },
        );
      }

      return const SizedBox();
    },
  ),
)
    );
  }
}