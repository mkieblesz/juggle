# TODO: use django-any or similar
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from psycopg2.extras import NumericRange
from rest_framework.test import APIClient
from datetime import datetime
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


# TODO: add more tests


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
def job(db):
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


def test_allow_to_list_all_applicants_for_any_job(client, professional, business, job):
    job_application = JobApplication.objects.create(job=job, professional=professional)

    assert client.get(reverse("job-applications")).data == [
        {"type": "business", "company_name": "Example Inc."},
    ]


def test_allow_professional_to_apply_for_any_job(client, professional, business, job):
    assert client.post(reverse("job-applications")).data == []


def test_limit_to_5_applications_per_job_per_day(client, business, job):
    date = datetime.strptime("24-05-2010", "%d-%m-%Y").date()

    for i in range(0, 5):
        p = _create_professional(f"{i} professional")
        JobApplication.objects.create(job=job, professional=p, date=date)

    assert JobApplication.filter(job=job).count() == 5

    response = client.post(
        reverse("job-applications"), {"job": job, "professional": p, "date": date}
    )

    assert response.status_code == 400
    assert JobApplication.filter(job=job).count() == 5

    date = datetime.strptime("25-05-2010", "%d-%m-%Y").date()
    response = client.post(
        reverse("job-applications"), {"job": job, "professional": p, "date": date}
    )

    assert response.status_code == 200
    assert JobApplication.filter(job=job).count() == 6
