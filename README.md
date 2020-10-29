# pendo-prom-emitter
A project to pull Pendo data into Prometheus metrics


## Prerequisites
You need:

- Python 3.8.x
- Pipenv
- Docker (Local Development Only)
- Docker Compose (Local Development Only)

## Development
This section covers the steps to get started and run the project.

### Getting Started
To get started developing you need to clone a local copy of the git repository.

0. Clone the repository
```bash
git clone https://github.com/RedHatInsights/pendo-prom-emitter.git
```

1. Change to the cloned directory:
```bash
cd pendo-prom-emitter
```
2. Copy .env.example into a .env:

```bash
cp .env.example .env
```

3. Update the environment variables:
```
PENDO_INTEGRATION_KEY=
PENDO_AGGREGATION_QUERY=
PENDO_AGGREGATION_FILTER=
PROMETHEUS_PUSH_GATEWAY=localhost:9091
PROMETHEUS_METRICS_MAP={}
NAMESPACE=NAMESPACE
EXECUTE_NAMESPACE=NAMESPACE
```

4. Install the requirements:

```bash
pipenv install --dev
```

5. Activate the virtual environment:
```bash
pipenv shell
```

6. Install pre-commit hooks for the repository:
```bash
pre-commit install
```

### Linting
You can execute linting using pre-commit with a make command:
```bash
make lint
```

### Developing with Docker Compose

1. Launch Prometheus, Prometheus Push Gateway, and Grafana monitoring stack components:
```bash
make docker-up
```

2. Execute pendo-prom-emittter:
```bash
make run-job
```

3. Review metrics using local containers:

 - Launch the Prometheus console at http://localhost:9090
 - Launch the Prometheus Push Gateway console at http://localhost:9091
 - Launch the Grafana console at http://localhost:3000
    - Login with `admin/password`
    - Create a Prometheus datasource using the address above

### Developing with OpenShift

The `pendo-prom-emitter` runs as a *CronJob* on OpenShift creating data daily. You can deploy it to OpenShift as follows:

1. Login to OpenShift
```
oc login
```
2. Select your project
```
oc project pendo
```
3. Copy `openshift/example.parameters.properties` into a `openshift/parameters.properties`
4. Update the values within `openshift/parameters.properties`
5. Create OpenShift resources
```
make oc-deploy
```

_Note:_ Delete OpenShift resources with the following command:
```
make oc-delete
```
