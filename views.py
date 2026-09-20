from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import (
    Property,
    WasteCollectionRequest,
    BulkPickupRequest,
    DumpingReport,
    FoodRedistributionRequest,
)

from .forms import (
    PropertyForm,
    WasteCollectionRequestForm,
    BulkPickupRequestForm,
    DumpingReportForm,
    FoodRedistributionRequestForm,
)


# =========================================================
# HOME
# =========================================================

def home(request):
    return render(request, 'index.html')


# =========================================================
# LOGIN
# =========================================================

def login(request):

    if request.method == 'POST':

        user_type = request.POST.get('user_type')

        # =================================================
        # CITIZEN LOGIN
        # =================================================

        if user_type == 'citizen':

            username_or_email = request.POST.get(
                'username',
                ''
            ).strip()

            password = request.POST.get(
                'password',
                ''
            )

            if not username_or_email or not password:

                messages.error(
                    request,
                    "Please enter your email and password."
                )

                return render(
                    request,
                    'login.html'
                )

            # Find user by email
            user = User.objects.filter(
                email__iexact=username_or_email
            ).first()

            # If not found, try username
            if user is None:

                user = User.objects.filter(
                    username__iexact=username_or_email
                ).first()

            # Check password
            if user is not None:

                authenticated_user = authenticate(
                    request,
                    username=user.username,
                    password=password
                )

                if authenticated_user is not None:

                    auth_login(
                        request,
                        authenticated_user
                    )

                    messages.success(
                        request,
                        f"Welcome back, "
                        f"{user.first_name or user.username}!"
                    )

                    return redirect(
                        'citizen_dashboard'
                    )

            messages.error(
                request,
                "Invalid email/username or password."
            )

        # =================================================
        # WORKER LOGIN
        # =================================================

        elif user_type == 'worker':

            worker_id = request.POST.get(
                'worker_id',
                ''
            ).strip()

            password = request.POST.get(
                'password',
                ''
            )

            if not worker_id or not password:

                messages.error(
                    request,
                    "Please enter Worker ID and password."
                )

                return render(
                    request,
                    'login.html'
                )

            user = authenticate(
                request,
                username=worker_id,
                password=password
            )

            if user is not None:

                auth_login(
                    request,
                    user
                )

                messages.success(
                    request,
                    f"Welcome Worker {worker_id}!"
                )

                return redirect(
                    'worker_dashboard'
                )

            messages.error(
                request,
                "Invalid Worker ID or password."
            )

        # =================================================
        # ADMIN LOGIN
        # =================================================

        elif user_type == 'admin':

            username = request.POST.get(
                'username',
                ''
            ).strip()

            password = request.POST.get(
                'password',
                ''
            )

            if not username or not password:

                messages.error(
                    request,
                    "Please enter admin username and password."
                )

                return render(
                    request,
                    'login.html'
                )

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None and user.is_staff:

                auth_login(
                    request,
                    user
                )

                messages.success(
                    request,
                    f"Welcome Admin {user.username}!"
                )

                return redirect(
                    'admin_dashboard'
                )

            messages.error(
                request,
                "Invalid admin credentials."
            )

    return render(
        request,
        'login.html'
    )


# =========================================================
# REGISTER
# =========================================================

def register(request):

    if request.method == 'POST':

        account_category = request.POST.get(
            'account_category'
        )

        full_name = request.POST.get(
            'full_name',
            ''
        ).strip()

        phone = request.POST.get(
            'phone',
            ''
        ).strip()

        email = request.POST.get(
            'email',
            ''
        ).strip().lower()

        password = request.POST.get(
            'password',
            ''
        )

        # Required fields
        if not full_name or not email or not password:

            messages.error(
                request,
                "Please fill in all required fields."
            )

            return render(
                request,
                'register.html'
            )

        # Check existing email
        existing_user = User.objects.filter(
            email__iexact=email
        ).first()

        if existing_user:

            messages.error(
                request,
                "This email is already registered. "
                "Please use the Login page."
            )

            return redirect('login')

        # Create username from email
        username = email

        # Create Django User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=full_name
        )

        user.save()

        messages.success(
            request,
            "Registration successful! "
            "Please login using the same email and password."
        )

        return redirect('login')

    return render(
        request,
        'register.html'
    )


# =========================================================
# CITIZEN DASHBOARD
# =========================================================

@login_required(login_url='login')
def citizen_dashboard(request):

    # -----------------------------------------------------
    # PROPERTY
    # -----------------------------------------------------

    properties = Property.objects.filter(
        owner=request.user
    ).order_by('-created_at')

    property_obj = properties.first()

    # -----------------------------------------------------
    # WASTE COLLECTION REQUESTS
    # -----------------------------------------------------

    waste_requests = WasteCollectionRequest.objects.filter(
        citizen=request.user
    ).select_related(
        'property'
    ).order_by('-created_at')

    # -----------------------------------------------------
    # BULK PICKUP REQUESTS
    # -----------------------------------------------------

    bulk_requests = BulkPickupRequest.objects.filter(
        citizen=request.user
    ).select_related(
        'property'
    ).order_by('-created_at')

    # -----------------------------------------------------
    # DUMPING REPORTS
    # -----------------------------------------------------

    dumping_reports = DumpingReport.objects.filter(
        citizen=request.user
    ).order_by('-created_at')

    # -----------------------------------------------------
    # FOOD REDISTRIBUTION REQUESTS
    # -----------------------------------------------------

    food_requests = FoodRedistributionRequest.objects.filter(
        citizen=request.user
    ).order_by('-created_at')

    # -----------------------------------------------------
    # CONTEXT
    # -----------------------------------------------------

    context = {
        'properties': properties,
        'property': property_obj,

        'waste_requests': waste_requests,

        'bulk_requests': bulk_requests,

        'dumping_reports': dumping_reports,

        'food_requests': food_requests,
    }

    return render(
        request,
        'citizen_dashboard.html',
        context
    )


# =========================================================
# WORKER DASHBOARD
# =========================================================

@login_required(login_url='login')
def worker_dashboard(request):

    return render(
        request,
        'worker_dashboard.html'
    )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@login_required(login_url='login')
def admin_dashboard(request):

    return render(
        request,
        'admin_dashboard.html'
    )


# =========================================================
# LOGOUT
# =========================================================

@login_required(login_url='login')
def logout_view(request):

    auth_logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect('login')


# =========================================================
# MY PROPERTY
# =========================================================

@login_required(login_url='login')
def my_property(request):

    print("========== MY PROPERTY DEBUG ==========")
    print("USER:", request.user)
    print("USER ID:", request.user.id)
    print("AUTHENTICATED:", request.user.is_authenticated)

    properties = Property.objects.filter(
        owner=request.user
    ).order_by('-created_at')

    print("PROPERTY COUNT:", properties.count())

    for p in properties:

        print(
            "PROPERTY:",
            p.property_id,
            "| OWNER:",
            p.owner,
            "| OWNER ID:",
            p.owner_id
        )

    print("=======================================")

    return render(
        request,
        'my_property.html',
        {
            'properties': properties
        }
    )


# =========================================================
# ADD PROPERTY
# =========================================================

@login_required(login_url='login')
def add_property(request):

    if request.method == 'POST':

        form = PropertyForm(request.POST)

        if form.is_valid():

            property_obj = form.save(commit=False)

            # Connect property to logged-in user
            property_obj.owner = request.user

            # Save user's name
            property_obj.owner_name = (
                request.user.first_name
                or request.user.username
            )

            property_obj.save()

            messages.success(
                request,
                "Property registered successfully!"
            )

            return redirect('my_property')

    else:

        form = PropertyForm()

    return render(
        request,
        'add_property.html',
        {
            'form': form
        }
    )


# =========================================================
# PROPERTY LIST
# =========================================================

@login_required(login_url='login')
def property_list(request):

    if request.user.is_staff:

        properties = Property.objects.all().order_by(
            '-created_at'
        )

    else:

        properties = Property.objects.filter(
            owner=request.user
        ).order_by('-created_at')

    return render(
        request,
        'property_list.html',
        {
            'properties': properties
        }
    )


# =========================================================
# WASTE COLLECTION
# =========================================================

@login_required(login_url='login')
def waste_collection(request):

    property_obj = Property.objects.filter(
        owner=request.user
    ).order_by('-created_at').first()

    if not property_obj:

        messages.warning(
            request,
            "Please register your property before requesting waste collection."
        )

        return redirect('add_property')

    if request.method == 'POST':

        form = WasteCollectionRequestForm(
            request.POST
        )

        if form.is_valid():

            waste_request = form.save(
                commit=False
            )

            waste_request.citizen = request.user
            waste_request.property = property_obj

            waste_request.save()

            messages.success(
                request,
                "Waste collection request submitted successfully!"
            )

            return redirect(
                'citizen_dashboard'
            )

    else:

        form = WasteCollectionRequestForm()

    return render(
        request,
        'waste_collection.html',
        {
            'form': form,
            'property': property_obj,
        }
    )


# =========================================================
# BULK PICKUP
# =========================================================

@login_required(login_url='login')
def bulk_pickup(request):

    property_obj = Property.objects.filter(
        owner=request.user
    ).order_by('-created_at').first()

    if not property_obj:

        messages.warning(
            request,
            "Please register your property before requesting bulk pickup."
        )

        return redirect(
            'add_property'
        )

    if request.method == 'POST':

        form = BulkPickupRequestForm(
            request.POST
        )

        if form.is_valid():

            bulk_request = form.save(
                commit=False
            )

            bulk_request.citizen = request.user
            bulk_request.property = property_obj

            bulk_request.save()

            messages.success(
                request,
                "Bulk pickup request submitted successfully!"
            )

            return redirect(
                'citizen_dashboard'
            )

    else:

        form = BulkPickupRequestForm()

    return render(
        request,
        'bulk_pickup.html',
        {
            'form': form,
            'property': property_obj,
        }
    )


# =========================================================
# REPORT DUMPING
# =========================================================

@login_required(login_url='login')
def report_dumping(request):

    if request.method == 'POST':

        form = DumpingReportForm(
            request.POST
        )

        if form.is_valid():

            report = form.save(
                commit=False
            )

            report.citizen = request.user

            report.save()

            messages.success(
                request,
                "Dumping report submitted successfully!"
            )

            return redirect(
                'citizen_dashboard'
            )

    else:

        form = DumpingReportForm()

    return render(
        request,
        'report_dumping.html',
        {
            'form': form
        }
    )


# =========================================================
# FOOD REDISTRIBUTION
# =========================================================

@login_required(login_url='login')
def food_redistribution(request):

    if request.method == 'POST':

        form = FoodRedistributionRequestForm(
            request.POST
        )

        if form.is_valid():

            food_request = form.save(
                commit=False
            )

            food_request.citizen = request.user

            food_request.save()

            messages.success(
                request,
                "Food redistribution request submitted successfully!"
            )

            return redirect(
                'citizen_dashboard'
            )

    else:

        form = FoodRedistributionRequestForm()

    return render(
        request,
        'food_redistribution.html',
        {
            'form': form
        }
    )