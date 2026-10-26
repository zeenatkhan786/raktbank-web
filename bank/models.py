from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

BLOOD_GROUPS = [
    ("A+", "A+"), ("A-", "A-"),
    ("B+", "B+"), ("B-", "B-"),
    ("AB+", "AB+"), ("AB-", "AB-"),
    ("O+", "O+"), ("O-", "O-"),
]

phone_validator = RegexValidator(
    regex=r"^\+?\d{10,13}$",
    message="Enter a valid phone number (10 to 13 digits).",
)


class Donor(models.Model):
    GENDERS = [("M", "Male"), ("F", "Female"), ("O", "Other")]

    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(18)],
        help_text="Donors must be at least 18 years old.",
    )
    gender = models.CharField(max_length=1, choices=GENDERS)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    phone = models.CharField(max_length=14, validators=[phone_validator])
    email = models.EmailField(blank=True)
    city = models.CharField(max_length=60)
    last_donation = models.DateField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    registered_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-registered_on"]

    def __str__(self):
        return f"{self.name} ({self.blood_group})"


class BloodStock(models.Model):
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS, unique=True)
    units = models.PositiveIntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["blood_group"]

    def __str__(self):
        return f"{self.blood_group}: {self.units} units"

    @property
    def level(self):
        if self.units == 0:
            return "out"
        if self.units <= 5:
            return "low"
        return "ok"


class BloodRequest(models.Model):
    STATUSES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("fulfilled", "Fulfilled"),
        ("rejected", "Rejected"),
    ]

    patient_name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    units_needed = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    hospital = models.CharField(max_length=120)
    city = models.CharField(max_length=60)
    contact = models.CharField(max_length=14, validators=[phone_validator])
    required_by = models.DateField()
    status = models.CharField(max_length=10, choices=STATUSES, default="pending")
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.patient_name} needs {self.blood_group}"

