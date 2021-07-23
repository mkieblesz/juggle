from datetime import date
from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from psycopg2.extras import NumericRange
from rest_framework import status

from juggle.models import (
    AvailabilityChoices,
    Business,
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


def _create_job(title):
    skill, _ = Skill.objects.get_or_create(name="Finance")
    business, _ = Business.objects.get_or_create(
        company_name="Example Inc.", website="http://www.example.com"
    )
    job = Job.objects.create(
        title=title,
        business=business,
        daily_rate_range=NumericRange(1, 100),
        availability=[AvailabilityChoices.ONE_OR_TWO_DAYS_PER_WEEK],
        location=[LocationChoices.ONSITE],
    )
    job.skills.add(skill)
    return job


@pytest.fixture
def professional(db):
    return _create_professional("Professional")


@pytest.fixture
def business(db):
    return Business.objects.create(company_name="Example Inc.", website="http://www.example.com")


@pytest.fixture
def job(db, business):
    return _create_job("Example job title")


class TestEntitySearchAPIView:
    @pytest.mark.parametrize(
        "query,expected",
        [
            (
                "",
                [
                    {"type": "professional", "full_name": "Mr Professional"},
                    {"type": "business", "company_name": "Example Inc."},
                    {"type": "job", "title": "Example job title"},
                ],
            ),
            (
                "Example",
                [
                    {"type": "business", "company_name": "Example Inc."},
                    {"type": "job", "title": "Example job title"},
                ],
            ),
            (
                "a",
                [
                    {"type": "professional", "full_name": "Mr Professional"},
                    {"type": "business", "company_name": "Example Inc."},
                    {"type": "job", "title": "Example job title"},
                ],
            ),
            (
                "query_which_doesnt_return_anything",
                [],
            ),
        ],
    )
    def test_view(self, query, expected, client, professional, business, job):
        assert client.get(reverse("entity_search"), data={"query": query}).data == expected


class TestJobApplicationViewSet:
    @pytest.mark.freeze_time("2017-05-21")
    def test_list(self, client, professional, job):
        JobApplication.objects.create(job=job, professional=professional)

        response = client.get(reverse("job-applications-list"))

        assert response.status_code == 200
        assert response.data["count"] == 1
        assert dict(response.data["results"][0]["professional"]) == {
            "full_name": professional.full_name
        }
        assert response.data["results"][0]["job"] == job.id
        assert response.data["results"][0]["date"] == "2017-05-21"

    @pytest.mark.freeze_time("2017-05-21")
    def test_list_filtered_by_job_id(self, client):
        p1 = _create_professional("1st professional")
        p2 = _create_professional("2st professional")
        p3 = _create_professional("3rd professional")
        j1 = _create_job("1st job")
        j2 = _create_job("2nd job")
        JobApplication.objects.create(job=j1, professional=p1)
        JobApplication.objects.create(job=j1, professional=p2)
        JobApplication.objects.create(job=j2, professional=p3)

        response = client.get(reverse("job-applications-list"), data={"job": j1.id})

        assert response.status_code == 200
        assert response.data["count"] == 2
        assert response.data["results"][0]["professional"]["full_name"] == p1.full_name
        assert response.data["results"][0]["job"] == j1.id
        assert response.data["results"][1]["professional"]["full_name"] == p2.full_name
        assert response.data["results"][1]["job"] == j1.id

    @pytest.mark.freeze_time("2017-05-21")
    def test_create(self, client, professional, job):
        response = client.post(
            reverse("job-applications-list"),
            {"job": job.id, "professional": professional.id},
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert JobApplication.objects.count() == 1

    @pytest.mark.freeze_time("2017-05-21")
    def test_create_limit_for_the_day_exceeded(self, client, professional, job):
        p1 = _create_professional(f"1 professional")
        p2 = _create_professional(f"2 professional")
        p3 = _create_professional(f"3 professional")
        JobApplication.objects.create(job=job, professional=p1)
        JobApplication.objects.create(job=job, professional=p2)
        JobApplication.objects.create(job=job, professional=p3)

        with patch("juggle.views.MAX_NUMBER_OF_APPLICATIONS_PER_JOB_PER_DAY", 3):
            response = client.post(
                reverse("job-applications-list"),
                {"job": job.id, "professional": professional.id},
            )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"message": "You can't apply for this job today. Try tomorrow"}

        assert JobApplication.objects.filter(job=job).count() == 3

    @pytest.mark.freeze_time("2017-05-22")
    def test_create_limit_for_today_didnt_exceed(self, client, professional, job):
        yesterday = date(2017, 5, 21)
        p1 = _create_professional(f"1 professional")
        p2 = _create_professional(f"2 professional")
        p3 = _create_professional(f"3 professional")
        JobApplication.objects.create(job=job, professional=p1, date=yesterday)
        JobApplication.objects.create(job=job, professional=p2, date=yesterday)
        JobApplication.objects.create(job=job, professional=p3, date=yesterday)

        with patch("juggle.views.MAX_NUMBER_OF_APPLICATIONS_PER_JOB_PER_DAY", 3):
            response = client.post(
                reverse("job-applications-list"),
                {"job": job.id, "professional": professional.id},
            )

        assert response.status_code == status.HTTP_201_CREATED
        assert JobApplication.objects.filter(job=job).count() == 4
