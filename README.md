# pendo-prom-emitter
A project to pull Pendo data into Prometheus metrics


## Prerequisites
You need:

- Python 3.8.x
- Pipenv

## Development
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
PENDO_INTEGRATION_KEY=PENDO_INT_KEY
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
