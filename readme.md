# Juggle

Welcome to Juggle 🙌🙌🙌

1. [Setup](#setup)
2. [Development](#development)
3. [Testing](#testing)
4. [Styleguide](#styleguide)
5. [Config Graph](#config-graph)

## Setup

It is assumed you are running Mac or Ubuntu and have python3.9, latest docker and docker compose installed. Following is recommended setup for development: db in docker, currently developed service on host (in this case it's only api). For demonstration all services in production are running nativiely.

```bash
python3.9 -m venv .venv
source .venv/bin/activate
pip install -U pip setuptools
pip install -r requirements.txt
```

TODO: setup 3rd party dev env access/download dev backup script/etc.

## Development

```bash
docker-compose up -d db
source .venv/bin/activate
python manage.py migrate
python manage.py shell < juggle/fixtures/init.py
python manage.py runserver
```

## Testing

* verification - checks for correctness of type annotations and styling errors (autoformat mismatch and/or [pep8](https://www.python.org/dev/peps/pep-0008/#a-foolish-consistency-is-the-hobgoblin-of-little-minds), custom consistency checks)
* unit - tests for correctness of a small set of instructions which influence the state in the context of larger procedure/function with calls to other procedures/functions within same codebase or external services being mocked
* integration - tests multiple units of functionality as a whole with calls to external services being mocked
* smoke - post-deploy tests with test users (e.g. making requests to 3rd party credit card service with testing user which doesn't make actual transaction) - no mocks

```bash
# verification
mypy juggle
black -S -l 100 -t py39 juggle
isort -rc -c juggle
flake8 juggle

# unit & integration
pytest --cov

# sanity, smoke, acceptance, performance, e2e
# TODO
```

## Styleguide

TODO

## Config Graph

TODO

Choose which elements of configuration layers of a build graph will be supported by the build system
- os: macos/linux/windows/...
- ide: vscode/sublime/vim/pycharm/emacs/...
- system components: db/cache/reverse proxy/web server/api/frontend/matching service/payment service/auth service/scheduling service/texting service/generation service/...
- virtualization strategy: all on host/mixed/all in docker/...
- stack runtime profile: prod/dev/test/local/...
- deployment orchestration: manual/scripts/docker-compose/terraform/kubernetes/cloudformation/...
- hardware provider: local/gcp/aws/scaleway/...
- ...
