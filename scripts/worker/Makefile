image = yolov8-worker
version = latest

build:
	docker build -t $(image):$(version) .

run-image:
	docker run -it $(image):$(version)

push-image:
	docker tag $(image):$(version) registry.ilya.cloud/$(image):$(version)
	docker push registry.ilya.cloud/$(image):$(version)
