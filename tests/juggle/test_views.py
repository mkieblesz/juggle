# TODO: use django-any or similar
from collections import OrderedDict
from datetime import datetime

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from psycopg2.extras import NumericRange
from rest_framework.test import APIClient

from juggle.models import (
    AvailabilityChoices,
    Business,
    BusinessAdmin,
    Job,
    JobApplication,
    LocationChoices,
    Professional,
    Skill,
)

User = get_user_model()


def _create_professional(name):
    user = User.objects.create(
        username=name,
        first_name="Mr",
        last_name=name,
        password=name,
    )
    return Professional.objects.create(
        user=user,
        title="Professional",
        daily_rate_range=NumericRange(1, 100),
        availability=[AvailabilityChoices.ONE_OR_TWO_DAYS_PER_WEEK],
        location=[LocationChoices.ONSITE],
    )


@pytest.fixture
def professional(db):
    return _create_professional("Professional")


@pytest.fixture
def business(db):
    return Business.objects.create(
        company_name="Example Inc.", website="http://www.example.com"
    )


@pytest.fixture
def job(db, business):
    skill = Skill.objects.create(name="Finance")
    job = Job.objects.create(
        title="Example job title",
        business=business,
        daily_rate_range=NumericRange(1, 100),
        availability=[AvailabilityChoices.ONE_OR_TWO_DAYS_PER_WEEK],
        location=[LocationChoices.ONSITE],
    )
    job.skills.add(skill)
    return job


def test_list_all_entities_listed_on_the_website(client, professional, business):
    assert client.get(reverse("entity_search")).data == [
        {"type": "professional", "full_name": "Mr Professional"},
        {"type": "business", "company_name": "Example Inc."},
    ]


def test_search_for_entities(client, professional, business):
    assert client.get(reverse("entity_search"), data={"query": "Example"}).data == [
        {"type": "professional", "full_name": "Mr Professional"},
        {"type": "business", "company_name": "Example Inc."},
    ]
    assert client.get(reverse("entity_search"), data={"query": "a"}).data == [
        {"type": "professional", "full_name": "Mr Professional"},
        {"type": "business", "company_name": "Example Inc."},
    ]


@pytest.mark.freeze_time("2017-05-21")
def test_allow_to_list_all_applicants_for_any_job(client, professional, job):
    JobApplication.objects.create(job=job, professional=professional)

    response = client.get(reverse("job-applications-list"))

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["next"] == None
    assert response.data["previous"] == None
    assert dict(response.data["results"][0]["professional"]) == {
        "full_name": "Mr Professional"
    }
    assert response.data["results"][0]["job"] == 1
    assert response.data["results"][0]["date"] == "2017-05-21"


@pytest.mark.freeze_time("2017-05-21")
def test_allow_professional_to_apply_for_any_job(client, professional, job):
    response = client.post(
        reverse("job-applications-list"),
        {"job": job.id, "professional": professional.id, "date": "2017-05-21"},
    )
    print(response.status_code)
    print(response.data)


@pytest.mark.freeze_time("2017-05-21")
def _test_limit_to_5_applications_per_job_per_day(client, professional, job):
    for i in range(0, 5):
        p = _create_professional(f"{i} professional")
        JobApplication.objects.create(job=job, professional=p)

    assert JobApplication.objects.filter(job=job).count() == 5

    response = client.post(
        reverse("job-applications-list"),
        {"job": job.id, "professional": professional.id, "date": "2017-05-21"},
    )

    assert response.status_code == 400
    assert JobApplication.objects.filter(job=job).count() == 5

    date = datetime.strptime("25-05-2010", "%d-%m-%Y").date()
    response = client.post(
        reverse("job-applications-list"),
        {"job": job.id, "professional": professional.id, "date": "25-05-2010"},
    )

    assert response.status_code == 200
    assert JobApplication.objects.filter(job=job).count() == 6
