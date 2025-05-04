import 'dart:convert';

import 'package:http/http.dart' as http;

class AuthService {
  final backendUrl = "https://video-streaming-app-3xxr.onrender.com/auth";

  Future<String> signUpUser({
    required String name,
    required String password,
    required String email,
  }) async {
    final res = await http.post(
      Uri.parse("$backendUrl/signup"),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({"name": name, "email": email, "password": password}),
    );

    if (res.statusCode != 200) {
      print(res.body);
      throw jsonDecode(res.body)['detail'] ?? 'An error occurred!';
    }

    print(res.headers);

    return jsonDecode(res.body)['message'] ??
        'Signup successful, please verify your email';
  }
}