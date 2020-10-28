help:
	@echo "Please use \`make <target>' where <target> is one of:"
	@echo ""
	@echo "--- General Commands ---"
	@echo "  help                                  show this message"
	@echo "  lint                                  run pre-commit against the project"
	@echo "  docker-up							   start docker containers"
	@echo "  docker-down						   stop docker containers"
	@echo "  docker-logs						   view docker container logs"
	@echo "  oc-deploy							   deploy cronjob to openshift"
	@echo "  oc-delete							   delete cronjob from openshift"
	@echo "  run-job							   locally run pendo emitter job"
	@echo ""

lint:
	pre-commit run --all-files


docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs

oc-deloy:
	oc process --param-file openshift/parameters.properties  -f openshift/ |  oc apply -f -

oc-delete:
	oc process --param-file openshift/parameters.properties  -f openshift/ |  oc delete -f -

run-job:
	python job.py
