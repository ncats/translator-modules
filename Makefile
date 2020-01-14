download-swagger-ui:
	wget --no-clobber https://files.pythonhosted.org/packages/0e/bb/d00f72e512784af20e368d2ecd5868c51a5aa3688d26ace5f4391651a3ce/swagger_ui_bundle-0.0.3-py3-none-any.whl

client-installation:
	cd client && python -m pip install -r requirements.txt . --no-cache-dir

server-installation: download-swagger-ui
	python -m pip install swagger_ui_bundle-0.0.3-py3-none-any.whl
	python -m pip install -r requirements.txt -e . --no-cache-dir
	cd server && python -m pip install -r requirements.txt . --no-cache-dir

.PHONY: server-tests

client-tests:
	cd client && python -m pip install -r test-requirements.txt && nosetests

server-tests:
	cd server && python -m pip install -r test-requirements.txt && nosetests

server-run:
	cd server && python -m ara_server

api-validation:
	./generate.sh validate

code-generation:
	./generate.sh server
	./generate.sh client

build: download-swagger-ui
	docker build --file Dockerfile_Workflow_ARA -t ncats:workflow-ara-server .

server-start:
	docker run -d --rm -p 8080:8080 --name workflow_ara_server ncats:workflow-ara-server

server-ssh:
	docker exec -it workflow_ara_server /bin/bash

server-stop:
	docker stop workflow_ara_server

server-log:
	docker logs workflow_ara_server
