# Juggle

Welcome to Juggle 🙌🙌🙌

1. [Setup](#setup)
2. [Development](#development)
3. [Testing](#testing)
4. [Styleguide](#styleguide)
5. [Config Graph](#config-graph)
6. [Todo](#todo)

## Setup

It is assumed you are running Mac or Ubuntu and have python3.9, latest docker and docker compose installed. Following is recommended setup for development: db in docker, currently developed service on host (in this case it's only api). For demonstration all services in production are running nativiely.

```bash
python3.9 -m venv .venv
source .venv/bin/activate
pip install -U pip setuptools
pip install -r requirements.txt
```

## Development

```bash
docker-compose up -d db
source .venv/bin/activate
python manage.py migrate
python manage.py shell < juggle/fixtures/init.py
python manage.py runserver
```

## Testing

* verification - checks for correctness of type annotations, styling errors (autoformat mismatch and/or [pep8](https://www.python.org/dev/peps/pep-0008/#a-foolish-consistency-is-the-hobgoblin-of-little-minds), custom consistency checks), security patches etc.
* unit - tests for correctness of a small set of instructions which influence the state in the context of larger procedure/function with calls to other procedures/functions within same codebase or external services being mocked
* integration - tests multiple units of functionality as a whole with calls to external services being mocked
* smoke - post-deploy tests with test users (e.g. making requests to 3rd party credit card service with testing user which doesn't make actual transaction) - no mocks

```bash
# verification
# pip-check
mypy juggle tests
black -S -l 100 -t py39 --exclude migrations juggle tests
isort -rc -c juggle tests
flake8 juggle tests

# unit & integration
pytest --cov

# sanity, smoke, acceptance, performance, e2e
# TODO
```

## Styleguide

## Config Graph

Choose which elements of configuration layers of a build graph will be supported by the build system
- os: macos/linux/windows/...
- ide: vscode/sublime/vim/pycharm/emacs/...
- system components: db/cache/reverse proxy/web server/api/frontend/matching service/payment service/auth service/scheduling service/texting service/generation service/...
- virtualization strategy: all on host/mixed/all in docker/...
- stack runtime profile: prod/dev/test/local/...
- deployment orchestration: manual/scripts/docker-compose/terraform/kubernetes/cloudformation/...
- hardware provider: local/gcp/aws/scaleway/...
- ...

## TODO

* TODO: search should be done with custom query or better materialized union view in postgres or even better separate search engine
* TODO: add pagination to search view
* TODO: add to readme setup 3rd party dev env access/download dev backup script/etc.
* TODO: use django-any or similar
* TODO: add styleguide
* TODO: build and store release artifacts on github and just rsync to machine
* TODO: do blue/green deployments
* TODO: exit with non 0 on failure in actions
* TODO: make actions more verbose (make more steps)
* TODO: create build system able to generate configuration files
* TODO: make search version with union work using python orm - current there is probably a bug
    ```python
        professional_qs = (
            Professional.objects.annotate(type=Value("professional"))
            .annotate(full_name=Concat("user__first_name", Value(" "), "user__last_name"))
            .filter(user__last_name__icontains=query)
            .values("type", "full_name")
        )

        business_qs = (
            Business.objects.annotate(type=Value("business"))
            .filter(company_name__icontains=query)
            .values("type", "company_name")
        )

        job_qs = (
            Job.objects.annotate(type=Value("job"))
            .filter(title__icontains=query)
            .values("type", "title")
        )

        entities = professional_qs.union(business_qs, job_qs)
    ```
    Generated sql for this query looks very veird:

    ```sql
        (SELECT professional AS "type", CONCAT("auth_user"."first_name", CONCAT( , "auth_user"."last_name")) AS "full_name" FROM "juggle_professional" INNER JOIN "auth_user" ON ("juggle_professional"."user_id" = "auth_user"."id")) UNION (SELECT "juggle_business"."company_name", business AS "type" FROM "juggle_business") UNION (SELECT "juggle_job"."title", job AS "type" FROM "juggle_job")
    ```

    and result even weirder:

    ```json
        [
            { "type": "Example Inc.", "full_name": "business" },
            { "type": "professional", "full_name": "Mr Professional" },
            { "type": "Example job title", "full_name": "job" }
        ]
    ```
