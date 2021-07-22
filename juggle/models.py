from django.conf import settings
from django.contrib.postgres.fields import ArrayField, IntegerRangeField
from django.db import models


class AvailabilityChoices(models.TextChoices):
    ONE_OR_TWO_DAYS_PER_WEEK = "1/2 days/wk", "1/2 days/wk"
    THREE_OR_FOUR_DAYS_PER_WEEK = "3/4 days/wk", "3/4 days/wk"
    FULL_TIME = "full time", "full time"


class LocationChoices(models.TextChoices):
    ONSITE = "onsite", "onsite"
    REMOTE = "remote", "remote"
    MIXED = "mixed", "mixed"


class Professional(models.Model):
    # user can have only one professional profile
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    daily_rate_range = IntegerRangeField()
    availability = ArrayField(
        models.CharField(max_length=32, blank=True, choices=AvailabilityChoices.choices)
    )
    location = ArrayField(
        models.CharField(max_length=32, blank=True, choices=LocationChoices.choices)
    )

    @property
    def email(self):
        return self.user.email

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"


class BusinessAdmin(models.Model):
    # business admin user can be potentially attached to multiple businesses
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    business = models.ForeignKey("juggle.Business", on_delete=models.CASCADE)

    class Meta:
        unique_together = [['user', 'business']]


class Business(models.Model):
    company_name = models.CharField(max_length=100)
    website = models.URLField()


class Job(models.Model):
    title = models.CharField(max_length=64)
    business = models.ForeignKey("juggle.Business", on_delete=models.CASCADE)
    daily_rate_range = IntegerRangeField()
    availability = ArrayField(
        models.CharField(max_length=32, blank=True, choices=AvailabilityChoices.choices)
    )
    location = ArrayField(
        models.CharField(max_length=32, blank=True, choices=LocationChoices.choices)
    )
    skills = models.ManyToManyField("juggle.Skill")


class JobApplication(models.Model):
    professional = models.ForeignKey("juggle.Professional", on_delete=models.CASCADE)
    job = models.ForeignKey("juggle.Job", on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = [['job', 'professional']]


class Skill(models.Model):
    name = models.CharField(max_length=100)
