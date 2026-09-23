import 'package:dio/dio.dart';

class ApiClient {
  final Dio dio;

  // Use 10.0.2.2 for Android Emulator, or 127.0.0.1 for Windows Desktop / Web
  ApiClient({String baseUrl = 'http://127.0.0.1:8000/api/v1/'})
    : dio = Dio(
        BaseOptions(
          baseUrl: baseUrl,
          connectTimeout: const Duration(seconds: 5),
          receiveTimeout: const Duration(seconds: 3),
          headers: {'Content-Type': 'application/json'},
        ),
      );

  Future<Response> commitDelivery(
    String matchId,
    Map<String, dynamic> data,
  ) async {
    return await dio.post('matches/$matchId/deliveries/', data: data);
  }
}
