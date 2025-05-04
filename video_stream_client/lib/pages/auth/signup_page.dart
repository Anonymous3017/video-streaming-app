import 'package:flutter/material.dart';
import 'package:video_stream_client/pages/auth/login_page.dart';
import 'package:video_stream_client/services/auth_service.dart';
import 'package:video_stream_client/utils/utils.dart';

class SignupPage extends StatefulWidget {
  static route() => MaterialPageRoute(builder: (context) => SignupPage());
  const SignupPage({super.key});

  @override
  State<SignupPage> createState() => _SignupPageState();
}

class _SignupPageState extends State<SignupPage> {
  final nameController = TextEditingController();
  final emailController = TextEditingController();
  final passwordController = TextEditingController();
  final formKey = GlobalKey<FormState>();
  final AuthService authService = AuthService();

  @override
  void dispose() {
    nameController.dispose();
    passwordController.dispose();
    emailController.dispose();
    super.dispose();
  }

  // void signUp() async {
  //   if (formKey.currentState!.validate()) {
  //     context.read<AuthCubit>().signUpUser(
  //       name: nameController.text.trim(),
  //       email: emailController.text.trim(),
  //       password: passwordController.text.trim(),
  //     );
  //   }
  // }

  void signUp() async {
    if (formKey.currentState!.validate()) {
      try{
        final res = await authService.signUpUser(
          name: nameController.text.trim(),
          email: emailController.text.trim(),
          password: passwordController.text.trim(),
        );
        showSnackBar(res, context);
      } catch(e){
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
              'Sign Up',
              style: TextStyle(fontSize: 50, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 30),
            TextFormField(
              controller: nameController,
              decoration: InputDecoration(hintText: 'Name'),
              validator: (value) {
                if (value != null && value.trim().isEmpty) {
                  return "Field cannot be empty!";
                }

                return null;
              },
            ),
            const SizedBox(height: 15),
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
              onPressed: signUp,
              child: Text(
                'SIGN UP',
                style: TextStyle(fontSize: 16, color: Colors.white),
              ),
            ),
            const SizedBox(height: 20),
            GestureDetector(
              onTap: () {
                Navigator.of(context).push(LoginPage.route());
              },
              child: RichText(
                text: TextSpan(
                  text: 'Already have an account? ',
                  style: Theme.of(context).textTheme.titleMedium,
                  children: [
                    TextSpan(
                      text: 'Sign In',
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
