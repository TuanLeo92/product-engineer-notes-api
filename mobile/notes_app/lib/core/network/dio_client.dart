import 'package:dio/dio.dart';
import 'package:notes_app/core/network/auth_interceptor.dart';
import 'api_config.dart';

class DioClient {
  late final Dio dio;

  DioClient(Future<String?> Function() getToken) {
    dio = Dio(
      BaseOptions(
        baseUrl: ApiConfig.baseUrl,
        headers: {
          "Content-Type": "application/json",
        },
      ),
    );

    dio.interceptors.add(AuthInterceptor(getToken));
  }
}