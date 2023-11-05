import 'dart:io';
import 'dart:math';

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
                      crossAxisAlignment: CrossAxisAlignment.center,
                      children: [
                        CameraResultWidget(state),
                        ElevatedButton(
                            style: ButtonStyle(
                                backgroundColor:
                                    MaterialStateProperty.all(Colors.purple)),
                            onPressed: () {
                              context.read<CameraBloc>().add(GoBackToCamera());
                            },
                            child: const Text("try again"))
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

class CameraResultWidget extends StatefulWidget {
  final CameraResult cameraResult;

  const CameraResultWidget(this.cameraResult, {super.key});

  @override
  State<CameraResultWidget> createState() => _CameraResultWidgetState();
}

class _CameraResultWidgetState extends State<CameraResultWidget> {
  late final int reportNumber;
  late final DateTime dateTime;

  @override
  void initState() {
    reportNumber = Random().nextInt(1000000);
    dateTime = DateTime.now();
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(8.0),
      child: AspectRatio(
        aspectRatio: 1,
        child: Container(
            decoration: BoxDecoration(
              border: Border.all(
                color: Colors.purple,
                width: 3,
              ),
              borderRadius: BorderRadius.circular(12),
            ),
            alignment: Alignment.center,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.center,
              mainAxisSize: MainAxisSize.min,
              children: [
                Spacer(),
                Text(
                  "Thank you\nfor your submission!",
                  textAlign: TextAlign.center,
                  style: TextStyle(fontSize: 24),
                ),
                Spacer(),
                Text(
                  "Report: $reportNumber",
                  style: TextStyle(fontSize: 12),
                ),
                SizedBox(
                  height: 10,
                ),
                Text(
                  "Your report was submitted on: ${dateTime.day}/${dateTime.month}/${dateTime.year} at ${dateTime.hour}:${dateTime.minute}",
                  style: TextStyle(fontSize: 12, color: Colors.grey[800]),
                ),
                Spacer(),
                Text(
                  "Check result:",
                  style: TextStyle(fontSize: 16),
                ),
                Text(
                  widget.cameraResult.testResult,
                  style: TextStyle(fontSize: 32),
                ),
                Spacer()
              ],
            )),
      ),
    );
  }
}
