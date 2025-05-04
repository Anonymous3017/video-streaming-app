import 'package:flutter/material.dart';
import 'package:video_stream_client/pages/auth/login_page.dart';
import 'package:video_stream_client/services/auth_service.dart';
import 'package:video_stream_client/utils/utils.dart';

class ConfirmSignupPage extends StatefulWidget {
  final String email;
  static route(String email) =>
      MaterialPageRoute(builder: (context) => ConfirmSignupPage(email: email));
  const ConfirmSignupPage({super.key, required this.email});

  @override
  State<ConfirmSignupPage> createState() => _ConfirmSignupPageState();
}

class _ConfirmSignupPageState extends State<ConfirmSignupPage> {
  final otpController = TextEditingController();
  late TextEditingController emailController;
  final formKey = GlobalKey<FormState>();
  final AuthService authService = AuthService();

  @override
  void initState() {
    super.initState();
    emailController = TextEditingController(text: widget.email);
  }

  @override
  void dispose() {
    otpController.dispose();
    emailController.dispose();
    super.dispose();
  }

  void confirmSignUp() async {
    if (formKey.currentState!.validate()) {
      try {
        final res = await authService.confirmSignUpUser(
          email: emailController.text.trim(),
          otp: otpController.text.trim(),
        );
        showSnackBar(res, context);
        Navigator.of(context).push(LoginPage.route());
      } catch (e) {
        showSnackBar(e.toString(), context);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(15.0),
        child: Form(
          key: formKey,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                'Confirm Sign Up',
                style: TextStyle(fontSize: 50, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 30),
              TextFormField(
                controller: emailController,
                decoration: InputDecoration(hintText: 'Email'),
                validator: (value) {
                  if (value != null && value.trim().isEmpty) {
                    return "Field cannot be empty!";
                  }
                  return null;
                },
              ),
              const SizedBox(height: 15),
              TextFormField(
                controller: otpController,
                decoration: InputDecoration(hintText: 'OTP'),
                obscureText: true,
                validator: (value) {
                  if (value != null && value.trim().isEmpty) {
                    return "Field cannot be empty!";
                  }
                  return null;
                },
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: () {},
                child: Text(
                  'CONFIRM',
                  style: TextStyle(fontSize: 16, color: Colors.white),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
