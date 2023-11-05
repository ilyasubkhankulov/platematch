part of 'camera_bloc.dart';

@immutable
sealed class CameraEvent {}

class PrepareCamera extends CameraEvent {}

class TakePictureRequested extends CameraEvent {}

class SendPicture extends CameraEvent {}

class GoBackToCamera extends CameraEvent {}
