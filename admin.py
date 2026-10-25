from django.contrib import admin

from .models import BloodRequest, BloodStock, Donor


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ("name", "blood_group", "city", "phone", "is_available")
    list_filter = ("blood_group", "is_available")
    search_fields = ("name", "city", "phone")


@admin.register(BloodStock)
class BloodStockAdmin(admin.ModelAdmin):
    list_display = ("blood_group", "units", "updated_on")


@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ("patient_name", "blood_group", "units_needed", "hospital", "status")
    list_filter = ("status", "blood_group")
    search_fields = ("patient_name", "hospital", "city")
