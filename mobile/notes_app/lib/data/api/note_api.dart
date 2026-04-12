import 'package:dio/dio.dart';

class NoteApi {
  final Dio dio;

  NoteApi(this.dio);

  Future<List<dynamic>> getNotes() async {
    final response = await dio.get("/notes/");
    return response.data["data"];
  }
}