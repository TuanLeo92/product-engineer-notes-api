import '../../domain/entities/note.dart';
import '../api/note_api.dart';

class NoteRepository {
  final NoteApi api;

  NoteRepository(this.api);

  Future<List<Note>> getNotes() {
    return api.getNotes();
  }
}