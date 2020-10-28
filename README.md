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
git clone https://github.com/chambridge/pendo-prom-emitter.git
```

1. Change to the cloned directory:
```bash
cd pendo-prom-emitter
```
2. Copy .env.example into a .env:

```bash
cp .env.example .evn
```

3. Update the environment variables:
```
PENDO_INTEGRATION_KEY=
PENDO_AGGREGATION_QUERY=
PENDO_AGGREGATION_FILTER=
PROMETHEUS_PUSH_GATEWAY=localhost:9091
PROMETHEUS_METRICS_MAP={}
NAMESPACE=NAMESPACE
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

### Local Development

1. Launch Prometheus, Prometheus Push Gateway, and Grafana monitoring stack components:
```bash
docker-compose up -d
```

2. Execute pendo-prom-emittter:
```bash
python job.py
```

3. Review metrics using local containers:

 - Launch the Prometheus console at http://localhost:9090
 - Launch the Prometheus Push Gateway console at http://localhost:9091
 - Launch the Grafana console at http://localhost:3000
    - Login with `admin/password`
    - Create a Prometheus datasource using the address above
