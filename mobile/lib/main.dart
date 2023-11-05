import 'dart:io';

import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:mobile/bloc/camera_bloc.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  runApp(const CameraApp());
}

/// CameraApp is the Main Application.
class CameraApp extends StatefulWidget {
  /// Default Constructor
  const CameraApp({super.key});

  @override
  State<CameraApp> createState() => _CameraAppState();
}

class _CameraAppState extends State<CameraApp> {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
            leadingWidth: 300,
            leading: const Padding(
              padding: const EdgeInsets.all(8.0),
              child: const Row(
                children: [
                  Icon(
                    Icons.translate,
                    color: Colors.black,
                  ),
                  SizedBox(
                    width: 10,
                  ),
                  Text(
                    "Eng",
                    style: TextStyle(color: Colors.black, fontSize: 20),
                  )
                ],
              ),
            ),
            backgroundColor: Colors.grey[200],
            actions: [
              IconButton(
                  onPressed: () {},
                  icon: Icon(
                    Icons.accessible,
                    color: Colors.black,
                  )),
            ]),
        body: SafeArea(
          child: BlocProvider(
            create: (context) => CameraBloc()..add(PrepareCamera()),
            child: BlocBuilder<CameraBloc, CameraState>(
              builder: (context, state) {
                switch (state) {
                  case CameraInitial():
                    return const Center(
                      child: CircularProgressIndicator(),
                    );
                  case CameraReady():
                    return Column(
                      crossAxisAlignment: CrossAxisAlignment.center,
                      children: [
                        const Padding(
                          padding: EdgeInsets.all(8.0),
                          child: Column(
                            children: [
                              Text(
                                "Capture a car",
                                style: TextStyle(fontSize: 20),
                              ),
                              Text("Make sure license plate and car is visible")
                            ],
                          ),
                        ),
                        Expanded(
                            child: FractionallySizedBox(
                          heightFactor: 1,
                          child: Center(
                            child: ClipRRect(
                                borderRadius: BorderRadius.circular(10),
                                child: CameraPreview((state).controller)),
                          ),
                        )),
                        ElevatedButton(
                            style: ButtonStyle(
                                backgroundColor:
                                    MaterialStateProperty.all(Colors.purple)),
                            onPressed: () async {
                              context
                                  .read<CameraBloc>()
                                  .add(TakePictureRequested());
                            },
                            child: const Text("Check Car"))
                      ],
                    );
                  case PictureTaken():
                    return state.isLoading
                        ? Center(child: CircularProgressIndicator())
                        : Column(
                            children: [
                              const Padding(
                                padding: EdgeInsets.all(8.0),
                                child: Column(
                                  children: [
                                    Text(
                                      "Picture taken",
                                      style: TextStyle(fontSize: 20),
                                    ),
                                    Text(
                                        "Make sure that license plate and car is visible")
                                  ],
                                ),
                              ),
                              Expanded(
                                child: Center(
                                  child: ClipRRect(
                                      borderRadius: BorderRadius.circular(10),
                                      child:
                                          Image.file(File(state.picture.path))),
                                ),
                              ),
                              Row(
                                mainAxisAlignment:
                                    MainAxisAlignment.spaceEvenly,
                                children: [
                                  ElevatedButton(
                                      style: ButtonStyle(
                                          backgroundColor:
                                              MaterialStateProperty.all(
                                                  Colors.red)),
                                      onPressed: () {
                                        context
                                            .read<CameraBloc>()
                                            .add(GoBackToCamera());
                                      },
                                      child: Text("Try again")),
                                  ElevatedButton(
                                      style: ButtonStyle(
                                          backgroundColor:
                                              MaterialStateProperty.all(
                                                  Colors.green)),
                                      onPressed: () {
                                        context
                                            .read<CameraBloc>()
                                            .add(SendPicture());
                                      },
                                      child: const Text("Send picture"))
                                ],
                              ),
                            ],
                          );
                  case CameraResult():
                    return Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text(state.result),
                        TextButton(
                            onPressed: () {
                              context.read<CameraBloc>().add(GoBackToCamera());
                            },
                            child: Text("try again"))
                      ],
                    );
                }
              },
            ),
          ),
        ),
      ),
    );
  }
}
