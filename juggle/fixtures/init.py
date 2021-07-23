from django.contrib.auth import get_user_model
from psycopg2.extras import NumericRange

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

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="admin",
        first_name="Mr",
        last_name="Super Admin",
    )

user_1, _ = User.objects.get_or_create(
    username="professional",
    first_name="Mr",
    last_name="Professional",
    password="test",
    email="john_smith@example.com",
)

user_2, _ = User.objects.get_or_create(
    username="business_admin",
    first_name="Mr",
    last_name="Business Admin",
    password="test",
)


professional, _ = Professional.objects.get_or_create(
    user=user_1,
    title="Boss",
    daily_rate_range=NumericRange(1, 100),
    availability=[AvailabilityChoices.ONE_OR_TWO_DAYS_PER_WEEK],
    location=[LocationChoices.ONSITE],
)

business, _ = Business.objects.get_or_create(
    company_name="Example Inc.", website="http://www.example.com"
)
business_admin, _ = BusinessAdmin.objects.get_or_create(business=business, user=user_2)

skill, _ = Skill.objects.get_or_create(name="Finance")
job, _ = Job.objects.get_or_create(
    title="Example job title",
    business=business,
    daily_rate_range=NumericRange(1, 100),
    availability=[AvailabilityChoices.ONE_OR_TWO_DAYS_PER_WEEK],
    location=[LocationChoices.ONSITE],
)
job.skills.add(skill)

JobApplication.objects.get_or_create(job=job, professional=professional)
