import 'package:dio/dio.dart';
import 'package:notes_app/domain/entities/note.dart';

class NoteApi {
  final Dio dio;

  NoteApi(this.dio);

  Future<List<Note>> getNotes() async {
    // Use trailing slash to avoid 307 redirect that can drop Authorization.
    final response = await dio.get("/notes/");

    final data = response.data["data"] as List;

    return data.map((e) {
      return Note(
        id: e["id"],
        title: e["title"],
        content: e["content"],
      );
    }).toList();
  }
}