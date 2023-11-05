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

class Match {
  final bool matched;
  final String plateValue;
  final String carValue;

  Match(this.matched, this.plateValue, this.carValue);
}

class Matches {
  final bool overallMatched;

  final Match makeMatch;
  final Match modelMatch;
  final Match yearMatch;

  Matches(this.overallMatched, this.makeMatch, this.modelMatch, this.yearMatch);
}

final class CameraResult extends CameraState {
  final bool success;
  final String testResult;
  final Matches? match;
  final CameraController controller;

  CameraResult(this.success, this.testResult, this.match, this.controller);
}
