download-swagger-ui:
	wget --no-clobber https://files.pythonhosted.org/packages/0e/bb/d00f72e512784af20e368d2ecd5868c51a5aa3688d26ace5f4391651a3ce/swagger_ui_bundle-0.0.3-py3-none-any.whl

installation:
	make download-swagger-ui
	python -m pip install swagger_ui_bundle-0.0.3-py3-none-any.whl
	cd server && python -m pip install -r requirements.txt

.PHONY: tests

tests:
	cd server && python -m pip install -r test-requirements.txt && nosetests

run:
	cd server && python -m ara_server

validation:
	./generate.sh validate

code-generation:
	./generate.sh server
	./generate.sh client

build: download-swagger-ui
	docker build --file Dockerfile_Workflow_ARA -t ncats:workflow-ara-server .

start:
	docker run -d --rm -p 8080:8080 --name workflow_ara_server ncats:workflow-ara-server

ssh:
	docker exec -it workflow_ara_server /bin/bash

stop:
	docker stop workflow_ara_server

log:
	docker logs workflow_ara_server
