image = yolov8
version = latest

build:
	docker build -t $(image):$(version) .

run-image:
	docker run -it $(image):$(version)

push-image:
	docker tag $(image):$(version) ilyasubkhankulov/$(image):$(version)
	docker push ilyasubkhankulov/$(image):$(version)
