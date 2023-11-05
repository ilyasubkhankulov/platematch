import 'package:bloc/bloc.dart';
import 'package:camera/camera.dart';
import 'package:dio/dio.dart';
import 'package:geolocator/geolocator.dart';
import 'package:meta/meta.dart';

part 'camera_event.dart';
part 'camera_state.dart';

Future<Position> _determinePosition() async {
  bool serviceEnabled;
  LocationPermission permission;

  // Test if location services are enabled.
  serviceEnabled = await Geolocator.isLocationServiceEnabled();
  if (!serviceEnabled) {
    // Location services are not enabled don't continue
    // accessing the position and request users of the
    // App to enable the location services.
    return Future.error('Location services are disabled.');
  }

  permission = await Geolocator.checkPermission();
  if (permission == LocationPermission.denied) {
    permission = await Geolocator.requestPermission();
    if (permission == LocationPermission.denied) {
      // Permissions are denied, next time you could try
      // requesting permissions again (this is also where
      // Android's shouldShowRequestPermissionRationale
      // returned true. According to Android guidelines
      // your App should show an explanatory UI now.
      return Future.error('Location permissions are denied');
    }
  }

  if (permission == LocationPermission.deniedForever) {
    // Permissions are denied forever, handle appropriately.
    return Future.error(
        'Location permissions are permanently denied, we cannot request permissions.');
  }

  // When we reach here, permissions are granted and we can
  // continue accessing the position of the device.
  return await Geolocator.getCurrentPosition();
}

class CameraBloc extends Bloc<CameraEvent, CameraState> {
  CameraBloc() : super(CameraInitial()) {
    on<PrepareCamera>(
      (event, emit) async {
        var cameras = await availableCameras();

        var controller = CameraController(cameras[0], ResolutionPreset.max);

        try {
          await controller.initialize();
        } catch (e) {
          if (e is CameraException) {
            switch (e.code) {
              case 'CameraAccessDenied':
                // Handle access errors here.
                break;
              default:
                // Handle other errors here.
                break;
            }
          }
          return;
        }
        emit(CameraReady(controller, true));
      },
    );

    on<TakePictureRequested>((event, emit) async {
      if (state is CameraReady) {
        if ((state as CameraReady).isLoading == false) return;

        emit(CameraReady((state as CameraReady).controller, false));
        var crState = state as CameraReady;
        var picture = await crState.controller.takePicture();

        var position = await _determinePosition();

        emit(PictureTaken(picture, position, crState.controller, false));
      }
    });

    on<SendPicture>(
      (event, emit) async {
        if (state is PictureTaken) {
          var ptState = state as PictureTaken;

          if (ptState.isLoading) return;

          var dio = Dio();

          emit(PictureTaken(
              ptState.picture, ptState.position, ptState.controller, true));

          final formData = FormData.fromMap({
            'long': ptState.position.longitude,
            'lat': ptState.position.latitude,
            'image': MultipartFile.fromBytes(
                await ptState.picture.readAsBytes(),
                filename: "test.heic"),
          });

          try {
            final response = await dio.post(
                'https://857f-204-11-230-50.ngrok-free.app/upload/',
                data: formData);

            emit(CameraResult(
                true, response.data.toString(), ptState.controller));
          } catch (e) {
            emit(CameraResult(false, "WE FAILED", ptState.controller));
          }
        }
      },
    );

    on<GoBackToCamera>((event, emit) {
      if (state is PictureTaken) {
        emit(CameraReady((state as PictureTaken).controller, true));
      }
      if (state is CameraResult) {
        emit(CameraReady((state as CameraResult).controller, true));
      }
    });
  }
}
