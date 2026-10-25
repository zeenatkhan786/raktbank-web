from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BloodRequestForm, DonorForm, RequestStatusForm, StockForm
from .models import BLOOD_GROUPS, BloodRequest, BloodStock, Donor


def ensure_stock():
    """Make sure one stock row exists for each of the 8 blood groups."""
    for code, _ in BLOOD_GROUPS:
        BloodStock.objects.get_or_create(blood_group=code)
    return BloodStock.objects.all()


# ---------- Home ----------
def home(request):
    stock = ensure_stock()
    context = {
        "stock": stock,
        "donor_count": Donor.objects.count(),
        "available_donors": Donor.objects.filter(is_available=True).count(),
        "total_units": sum(s.units for s in stock),
        "pending_requests": BloodRequest.objects.filter(status="pending").count(),
        "recent_requests": BloodRequest.objects.all()[:5],
    }
    return render(request, "bank/home.html", context)


# ---------- Donors ----------
def donor_list(request):
    donors = Donor.objects.all()
    q = request.GET.get("q", "").strip()
    group = request.GET.get("group", "")
    if q:
        donors = donors.filter(
            Q(name__icontains=q) | Q(city__icontains=q) | Q(phone__icontains=q)
        )
    if group:
        donors = donors.filter(blood_group=group)
    return render(request, "bank/donor_list.html", {
        "donors": donors, "q": q, "group": group, "groups": BLOOD_GROUPS,
    })


def donor_add(request):
    form = DonorForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Donor registered successfully.")
        return redirect("bank:donor_list")
    return render(request, "bank/form.html", {
        "form": form, "title": "Register Donor", "back": "bank:donor_list",
    })


def donor_edit(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    form = DonorForm(request.POST or None, instance=donor)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Donor details updated.")
        return redirect("bank:donor_list")
    return render(request, "bank/form.html", {
        "form": form, "title": f"Edit Donor: {donor.name}", "back": "bank:donor_list",
    })


def donor_delete(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    if request.method == "POST":
        donor.delete()
        messages.success(request, "Donor record deleted.")
        return redirect("bank:donor_list")
    return render(request, "bank/confirm_delete.html", {
        "object": donor, "back": "bank:donor_list",
    })


# ---------- Blood availability ----------
def availability(request):
    return render(request, "bank/availability.html", {"stock": ensure_stock()})


def stock_edit(request, pk):
    item = get_object_or_404(BloodStock, pk=pk)
    form = StockForm(request.POST or None, instance=item)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"Stock for {item.blood_group} updated.")
        return redirect("bank:availability")
    return render(request, "bank/form.html", {
        "form": form, "title": f"Update Stock: {item.blood_group}",
        "back": "bank:availability",
    })


# ---------- Blood requests ----------
def request_list(request):
    requests_qs = BloodRequest.objects.all()
    status = request.GET.get("status", "")
    group = request.GET.get("group", "")
    if status:
        requests_qs = requests_qs.filter(status=status)
    if group:
        requests_qs = requests_qs.filter(blood_group=group)
    return render(request, "bank/request_list.html", {
        "requests": requests_qs, "status": status, "group": group,
        "groups": BLOOD_GROUPS, "statuses": BloodRequest.STATUSES,
    })


def request_add(request):
    form = BloodRequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Blood request submitted.")
        return redirect("bank:request_list")
    return render(request, "bank/form.html", {
        "form": form, "title": "Request Blood", "back": "bank:request_list",
    })


def request_edit(request, pk):
    obj = get_object_or_404(BloodRequest, pk=pk)
    form = BloodRequestForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Request updated.")
        return redirect("bank:request_list")
    return render(request, "bank/form.html", {
        "form": form, "title": "Edit Request", "back": "bank:request_list",
    })


def request_status(request, pk):
    obj = get_object_or_404(BloodRequest, pk=pk)
    form = RequestStatusForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        new_status = form.cleaned_data["status"]
        # Taking stock out only when a request moves to "fulfilled".
        if new_status == "fulfilled" and obj.status != "fulfilled":
            stock, _ = BloodStock.objects.get_or_create(blood_group=obj.blood_group)
            if stock.units < obj.units_needed:
                messages.error(
                    request,
                    f"Only {stock.units} unit(s) of {obj.blood_group} in stock; "
                    f"{obj.units_needed} needed.",
                )
                return redirect("bank:request_list")
            stock.units -= obj.units_needed
            stock.save()
        form.save()
        messages.success(request, f"Request marked as {obj.get_status_display()}.")
        return redirect("bank:request_list")
    return render(request, "bank/form.html", {
        "form": form, "title": f"Update Status: {obj.patient_name}",
        "back": "bank:request_list",
    })


def request_delete(request, pk):
    obj = get_object_or_404(BloodRequest, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Request deleted.")
        return redirect("bank:request_list")
    return render(request, "bank/confirm_delete.html", {
        "object": obj, "back": "bank:request_list",
    })
