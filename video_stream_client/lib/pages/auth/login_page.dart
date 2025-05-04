import 'package:flutter/material.dart';
import 'package:video_stream_client/pages/auth/signup_page.dart';
class LoginPage extends StatefulWidget {
  static route() => MaterialPageRoute(builder: (context) => LoginPage());
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final emailController = TextEditingController();
  final passwordController = TextEditingController();
  final formKey = GlobalKey<FormState>();
  // final AuthService authService = AuthService();

  @override
  void dispose() {
    passwordController.dispose();
    emailController.dispose();
    super.dispose();
  }

  // void login() async {
  //   if (formKey.currentState!.validate()) {
  //     context.read<AuthCubit>().loginUser(
  //       email: emailController.text.trim(),
  //       password: passwordController.text.trim(),
  //     );
  //   }
  // }

  //login log controler details
  void login() async {
    if (formKey.currentState!.validate()) {
      //print controler data
      print(emailController.text);
      print(passwordController.text);
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
              'Sign in.',
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
              controller: passwordController,
              decoration: InputDecoration(hintText: 'Password'),
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
              onPressed: login,
              child: Text(
                'SIGN IN',
                style: TextStyle(fontSize: 16, color: Colors.white),
              ),
            ),
            const SizedBox(height: 20),
            GestureDetector(
              onTap: () {
                Navigator.of(context).push(SignupPage.route());
              },
              child: RichText(
                text: TextSpan(
                  text: 'Don\'t have an account? ',
                  style: Theme.of(context).textTheme.titleMedium,
                  children: [
                    TextSpan(
                      text: 'Sign up',
                      style: Theme.of(context)
                          .textTheme
                          .titleMedium
                          ?.copyWith(fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    ));
  }
}
