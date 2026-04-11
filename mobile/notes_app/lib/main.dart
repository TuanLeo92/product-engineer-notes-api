import 'package:flutter/material.dart';
import 'package:notes_app/core/network/dio_client.dart';
import 'package:notes_app/data/api/auth_api.dart';

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
      home: Scaffold(
        appBar: AppBar(title: const Text('Notes')),
        body: const Center(child: Text('App Started')),
      ),
    );
  }

  void testLogin() async {
  final client = DioClient(() async => null);
  final api = AuthApi(client.dio);

  final email = "tuan.le@gmail.com";

  final token = await api.login(email, "123456");
  print("Logged in: ${email}");
  print("Token: ${token}");
}
}