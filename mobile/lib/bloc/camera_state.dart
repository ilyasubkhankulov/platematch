part of 'camera_bloc.dart';

@immutable
sealed class CameraState {}

final class CameraInitial extends CameraState {}

final class CameraReady extends CameraState {
  final CameraController controller;
  final bool isLoading;

  CameraReady(this.controller, this.isLoading);
}

final class PictureTaken extends CameraState {
  final XFile picture;
  final Position position;
  final CameraController controller;
  final bool isLoading;

  PictureTaken(this.picture, this.position, this.controller, this.isLoading);
}

final class CameraResult extends CameraState {
  final bool success;
  final String result;
  final CameraController controller;

  CameraResult(this.success, this.result, this.controller);
}
