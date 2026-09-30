from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum

from .models import (
    Property,
    WasteCollectionRequest,
    BulkPickupRequest,
    DumpingReport,
    FoodRedistributionRequest,
    WasteCollectionRecord,
    DailyWorkUpdate,
    Notification,
    WorkerProfile,
    WasteStorageRecord,
    DumpingFine,

)

from .forms import (
    PropertyForm,
    WasteCollectionRequestForm,
    BulkPickupRequestForm,
    DumpingReportForm,
    FoodRedistributionRequestForm,
    WasteCollectionRecordForm,
    DailyWorkUpdateForm,
)


# =========================================================
# HOME
# =========================================================

def home(request):

    return render(
        request,
        'index.html'
    )


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


            # Find user using email
            user = User.objects.filter(
                email__iexact=username_or_email
            ).first()


            # If email not found, try username
            if user is None:

                user = User.objects.filter(
                    username__iexact=username_or_email
                ).first()


            # Authenticate
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

        # -----------------------------------------
        # GET FORM DATA
        # -----------------------------------------

        account_category = request.POST.get(
            'account_category',
            ''
        ).strip().lower()

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

        worker_id = request.POST.get(
            'worker_id',
            ''
        ).strip().upper()

        assigned_area = request.POST.get(
            'assigned_area',
            ''
        ).strip()

        confirm_password = request.POST.get(
            'confirm_password',
            ''
        )

        # -----------------------------------------
        # REQUIRED FIELDS
        # -----------------------------------------

        if not full_name or not email or not password:

            messages.error(
                request,
                "Please fill in all required fields."
            )

            return render(
                request,
                'register.html'
            )

        # -----------------------------------------
        # WORKER VALIDATION
        # -----------------------------------------

        if account_category == 'worker':

            if not worker_id:

                messages.error(
                    request,
                    "Please enter Worker ID."
                )

                return render(
                    request,
                    'register.html'
                )

            if not assigned_area:

                messages.error(
                    request,
                    "Please enter Assigned Area."
                )

                return render(
                    request,
                    'register.html'
                )

            if password != confirm_password:

                messages.error(
                    request,
                    "Password and Confirm Password do not match."
                )

                return render(
                    request,
                    'register.html'
                )

            # Check Worker ID in User table
            if User.objects.filter(
                username__iexact=worker_id
            ).exists():

                messages.error(
                    request,
                    "This Worker ID is already registered."
                )

                return render(
                    request,
                    'register.html'
                )

            # Check Worker ID in WorkerProfile table
            if WorkerProfile.objects.filter(
                worker_id__iexact=worker_id
            ).exists():

                messages.error(
                    request,
                    "This Worker ID already has a worker profile."
                )

                return render(
                    request,
                    'register.html'
                )

        # -----------------------------------------
        # EMAIL CHECK
        # -----------------------------------------

        if User.objects.filter(
            email__iexact=email
        ).exists():

            messages.error(
                request,
                "This email is already registered. "
                "Please use the Login page."
            )

            return redirect('login')

        # -----------------------------------------
        # SELECT USERNAME
        # -----------------------------------------

        if account_category == 'worker':

            username = worker_id

        else:

            username = email

        # -----------------------------------------
        # CREATE USER
        # -----------------------------------------

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=full_name
        )

        # -----------------------------------------
        # CREATE WORKER PROFILE
        # -----------------------------------------

        if account_category == 'worker':

            WorkerProfile.objects.create(
                user=user,
                worker_id=worker_id,
                phone=phone,
                assigned_area=assigned_area,
                status='ACTIVE'
            )

        # -----------------------------------------
        # SUCCESS MESSAGE
        # -----------------------------------------

        if account_category == 'worker':

            messages.success(
                request,
                f"Worker registration successful! "
                f"Worker ID: {worker_id}. "
                f"Please login using your Worker ID and password."
            )

        else:

            messages.success(
                request,
                "Registration successful! "
                "Please login using the same email and password."
            )

        return redirect('login')

    # -----------------------------------------
    # GET REQUEST
    # -----------------------------------------

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
    ).order_by(
        '-created_at'
    )

    property_obj = properties.first()


    # -----------------------------------------------------
    # WASTE COLLECTION REQUESTS
    # -----------------------------------------------------

    waste_requests = WasteCollectionRequest.objects.filter(
        citizen=request.user
    ).select_related(
        'property'
    ).order_by(
        '-created_at'
    )


    # -----------------------------------------------------
    # BULK PICKUP REQUESTS
    # -----------------------------------------------------

    bulk_requests = BulkPickupRequest.objects.filter(
        citizen=request.user
    ).select_related(
        'property'
    ).order_by(
        '-created_at'
    )


    # -----------------------------------------------------
    # DUMPING REPORTS
    # -----------------------------------------------------

    dumping_reports = DumpingReport.objects.filter(
        citizen=request.user
    ).order_by(
        '-created_at'
    )


    # -----------------------------------------------------
    # FOOD REDISTRIBUTION REQUESTS
    # -----------------------------------------------------

    food_requests = FoodRedistributionRequest.objects.filter(
        citizen=request.user
    ).order_by(
        '-created_at'
    )


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

# =========================================================
# ADMIN DASHBOARD
# =========================================================

@login_required(login_url='login')
def admin_dashboard(request):

    if not request.user.is_staff:

        messages.error(
            request,
            "Admin access required."
        )

        return redirect('login')


    today = timezone.localdate()


    # =====================================================
    # USERS
    # =====================================================

    total_citizens = User.objects.filter(
        is_staff=False,
        is_superuser=False
    ).exclude(
        worker_profile__isnull=False
    ).count()


    total_workers = WorkerProfile.objects.filter(
        status='ACTIVE'
    ).count()


    # =====================================================
    # PROPERTIES
    # =====================================================

    total_properties = Property.objects.count()


    # =====================================================
    # TODAY'S COLLECTIONS
    # =====================================================

    todays_collections = WasteCollectionRecord.objects.filter(
        collection_date=today
    ).count()


    # =====================================================
    # BULK PICKUP
    # =====================================================

    pending_pickups = BulkPickupRequest.objects.filter(
        status='PENDING'
    ).count()


    # =====================================================
    # FOOD REDISTRIBUTION
    # =====================================================

    food_donations = FoodRedistributionRequest.objects.filter(
        request_type='DONATE'
    ).count()


    food_requests = FoodRedistributionRequest.objects.filter(
        request_type='REQUEST'
    ).count()


    # =====================================================
    # DUMPING REPORTS
    # =====================================================

    dumping_reports = DumpingReport.objects.count()


    # =====================================================
    # RECENT COLLECTIONS
    # =====================================================

    recent_collections = WasteCollectionRecord.objects.select_related(
        'property',
        'worker'
    ).order_by(
        '-collection_date',
        '-created_at'
    )[:6]


    # =====================================================
    # WORKER PROFILES
    # =====================================================

    worker_profiles = WorkerProfile.objects.select_related(
        'user'
    ).order_by(
        '-created_at'
    )[:10]


    # =====================================================
    # RECENT PROPERTIES
    # =====================================================

    recent_properties = Property.objects.select_related(
        'owner'
    ).order_by(
        '-created_at'
    )[:10]


    # =====================================================
    # WASTE CATEGORY TOTALS
    # =====================================================

    waste_totals = WasteCollectionRecord.objects.aggregate(

        biodegradable=Sum('biodegradable'),

        non_biodegradable=Sum(
            'non_biodegradable'
        ),

        plastic=Sum('plastic'),

        paper=Sum('paper'),

        glass=Sum('glass'),

        metal=Sum('metal'),

        electronic=Sum('electronic'),

        hazardous=Sum('hazardous'),

    )


    biodegradable_total = (
        waste_totals['biodegradable'] or 0
    )

    non_biodegradable_total = (
        waste_totals['non_biodegradable'] or 0
    )

    plastic_total = (
        waste_totals['plastic'] or 0
    )

    paper_total = (
        waste_totals['paper'] or 0
    )

    glass_total = (
        waste_totals['glass'] or 0
    )

    metal_total = (
        waste_totals['metal'] or 0
    )

    electronic_total = (
        waste_totals['electronic'] or 0
    )

    hazardous_total = (
        waste_totals['hazardous'] or 0
    )


    # =====================================================
    # CONTEXT
    # =====================================================

    context = {

        'total_properties':
            total_properties,

        'total_citizens':
            total_citizens,

        'total_workers':
            total_workers,

        'todays_collections':
            todays_collections,

        'pending_pickups':
            pending_pickups,

        'food_donations':
            food_donations,

        'food_requests':
            food_requests,

        'dumping_reports':
            dumping_reports,

        'recent_collections':
            recent_collections,

        'worker_profiles':
            worker_profiles,

        'recent_properties':
            recent_properties,

        'today':
            today,


        # Waste categories

        'biodegradable_total':
            biodegradable_total,

        'non_biodegradable_total':
            non_biodegradable_total,

        'plastic_total':
            plastic_total,

        'paper_total':
            paper_total,

        'glass_total':
            glass_total,

        'metal_total':
            metal_total,

        'electronic_total':
            electronic_total,

        'hazardous_total':
            hazardous_total,

    }


    return render(
        request,
        'admin_dashboard.html',
        context
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

    return redirect(
        'login'
    )


# =========================================================
# MY PROPERTY
# =========================================================

@login_required(login_url='login')
def my_property(request):

    print(
        "========== MY PROPERTY DEBUG =========="
    )

    print(
        "USER:",
        request.user
    )

    print(
        "USER ID:",
        request.user.id
    )

    print(
        "AUTHENTICATED:",
        request.user.is_authenticated
    )


    properties = Property.objects.filter(
        owner=request.user
    ).order_by(
        '-created_at'
    )


    print(
        "PROPERTY COUNT:",
        properties.count()
    )


    for p in properties:

        print(
            "PROPERTY:",
            p.property_id,
            "| OWNER:",
            p.owner,
            "| OWNER ID:",
            p.owner_id
        )


    print(
        "======================================="
    )


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

        form = PropertyForm(
            request.POST
        )


        if form.is_valid():

            property_obj = form.save(
                commit=False
            )


            # Connect property to logged-in user
            property_obj.owner = request.user


            # Save owner name
            property_obj.owner_name = (
                request.user.first_name
                or request.user.username
            )


            property_obj.save()


            messages.success(
                request,
                "Property registered successfully!"
            )


            return redirect(
                'my_property'
            )


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
        ).order_by(
            '-created_at'
        )


    return render(
        request,
        'property_list.html',
        {
            'properties': properties
        }
    )

@login_required(login_url='login')
def property_detail(request, property_id):

    property_obj = Property.objects.select_related(
         'owner'
        ).get(
         id=property_id
        )

    return render(
        request,
        'property_detail.html',
        {
            'property': property_obj
        }
    )

@login_required(login_url='login')
def edit_property(request, property_id):

    property_obj = Property.objects.get(
        id=property_id
    )

    if request.method == 'POST':

        owner_name = request.POST.get(
            'owner_name',
            ''
        ).strip()

        property_type = request.POST.get(
            'property_type',
            ''
        ).strip()

        address = request.POST.get(
            'address',
            ''
        ).strip()

        phone = request.POST.get(
            'phone',
            ''
        ).strip()


        # Validation

        if not owner_name:
            messages.error(
                request,
                "Owner name is required."
            )

            return render(
                request,
                'edit_property.html',
                {
                    'property': property_obj
                }
            )


        if not property_type:
            messages.error(
                request,
                "Please select a property type."
            )

            return render(
                request,
                'edit_property.html',
                {
                    'property': property_obj
                }
            )


        if not address:
            messages.error(
                request,
                "Address is required."
            )

            return render(
                request,
                'edit_property.html',
                {
                    'property': property_obj
                }
            )


        # Update property

        property_obj.owner_name = owner_name
        property_obj.property_type = property_type
        property_obj.address = address
        property_obj.phone = phone

        property_obj.save()


        messages.success(
            request,
            f"Property {property_obj.property_id} updated successfully."
        )


        return redirect(
            'property_detail',
            property_id=property_obj.id
        )


    return render(
        request,
        'edit_property.html',
        {
            'property': property_obj
        }
    )

@login_required(login_url='login')
def delete_property(request, property_id):

    property_obj = Property.objects.get(
        id=property_id
    )

    # Check whether this property has related records
    has_collection_records = WasteCollectionRecord.objects.filter(
        property=property_obj
    ).exists()

    has_waste_requests = WasteCollectionRequest.objects.filter(
        property=property_obj
    ).exists()

    has_bulk_requests = BulkPickupRequest.objects.filter(
        property=property_obj
    ).exists()

    has_related_records = (
        has_collection_records
        or has_waste_requests
        or has_bulk_requests
    )

    if request.method == 'POST':

        if has_related_records:
            messages.error(
                request,
                "This property cannot be deleted because it has related collection or service records."
            )

            return redirect(
                'property_detail',
                property_id=property_obj.id
            )

        property_id_display = property_obj.property_id

        property_obj.delete()

        messages.success(
            request,
            f"Property {property_id_display} deleted successfully."
        )

        return redirect('property_list')

    return render(
        request,
        'delete_property.html',
        {
            'property': property_obj,
            'has_related_records': has_related_records,
        }
    )

@login_required(login_url='login')
def collection_records(request):

    records = WasteCollectionRecord.objects.select_related(
        'worker',
        'property'
    ).order_by(
        '-collection_date',
        '-created_at'
    )

    return render(
        request,
        'collection_records.html',
        {
            'records': records
        }
    )


# =========================================================
# WASTE COLLECTION - CITIZEN
# =========================================================

@login_required(login_url='login')
def waste_collection(request):

    property_obj = Property.objects.filter(
        owner=request.user
    ).order_by(
        '-created_at'
    ).first()


    if not property_obj:

        messages.warning(
            request,
            "Please register your property before requesting waste collection."
        )

        return redirect(
            'add_property'
        )


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
# BULK PICKUP - CITIZEN
# =========================================================

@login_required(login_url='login')
def bulk_pickup(request):

    property_obj = Property.objects.filter(
        owner=request.user
    ).order_by(
        '-created_at'
    ).first()


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
            request.POST,
            request.FILES
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


# =========================================================
# WORKER - VERIFY PROPERTY
# =========================================================

@login_required(login_url='login')
def verify_property(request):

    if request.method == 'POST':

        property_id = request.POST.get(
            'property_id',
            ''
        ).strip().upper()

        worker_id = request.POST.get(
            'worker_id',
            ''
        ).strip()

        property_obj = Property.objects.filter(
            property_id=property_id
        ).first()

        if not property_obj:
            messages.error(
                request,
                "Property not found. Please check the Property ID."
            )

        else:
            messages.success(
                request,
                f"Property {property_obj.property_id} verified successfully."
            )

        return render(
            request,
            'verify_property.html',
            {
                'property': property_obj,
                'searched_id': property_id,
                'workers': WorkerProfile.objects.select_related(
                    'user'
                ).filter(
                    status='ACTIVE'
                ).order_by('worker_id'),
                'selected_worker_id': worker_id,
            }
        )

    workers = WorkerProfile.objects.select_related(
        'user'
    ).filter(
        status='ACTIVE'
    ).order_by('worker_id')

    return render(
        request,
        'verify_property.html',
        {
            'workers': workers,
            'selected_worker_id': request.user.username,
        }
    )


# =========================================================
# WORKER - RECORD COLLECTION
# =========================================================

@login_required(login_url='login')
def record_collection(request, property_id):

    property_obj = Property.objects.filter(
        property_id=property_id
    ).first()


    if not property_obj:

        messages.error(
            request,
            "Property not found."
        )

        return redirect(
            'verify_property'
        )


    if request.method == 'POST':

        form = WasteCollectionRecordForm(
            request.POST
        )


        if form.is_valid():

            today = timezone.localdate()


            # Check duplicate collection
            existing_record = WasteCollectionRecord.objects.filter(
                property=property_obj,
                collection_date=today
            ).first()


            if existing_record:

                messages.warning(
                    request,
                    "Collection has already been recorded for this property today."
                )

                return redirect(
                    'my_collection_areas'
                )


            collection = form.save(
                commit=False
            )


            collection.worker = request.user

            collection.property = property_obj

            collection.collection_date = today

            collection.save()


            messages.success(
                request,
                f"Waste collection recorded successfully for "
                f"{property_obj.property_id}!"
            )


            return redirect(
                'my_collection_areas'
            )


    else:

        form = WasteCollectionRecordForm()


    return render(
        request,
        'record_collection.html',
        {
            'property': property_obj,
            'form': form,
            'today': timezone.localdate(),
        }
    )


# =========================================================
# WORKER - MY COLLECTION AREAS
# =========================================================

@login_required(login_url='login')
def my_collection_areas(request):

    properties = Property.objects.all().order_by(
        '-created_at'
    )


    today = timezone.localdate()


    today_records = WasteCollectionRecord.objects.filter(
        collection_date=today
    )


    collected_property_ids = set(
        today_records.values_list(
            'property_id',
            flat=True
        )
    )


    for property_obj in properties:

        if property_obj.id in collected_property_ids:

            property_obj.collection_status = 'COMPLETED'

        else:

            property_obj.collection_status = 'PENDING'


    total_properties = properties.count()


    today_collection = today_records.count()


    completed_count = sum(
        1
        for property_obj in properties
        if property_obj.collection_status == 'COMPLETED'
    )


    pending_count = (
        total_properties
        - completed_count
    )


    context = {

        'properties': properties,

        'total_properties': total_properties,

        'today_collection': today_collection,

        'completed_count': completed_count,

        'pending_count': pending_count,

        'today': today,

    }


    return render(
        request,
        'my_collection_areas.html',
        context
    )


# =========================================================
# WORKER - BULK PICKUP
# =========================================================

@login_required(login_url='login')
def worker_bulk_pickup(request):

    bulk_requests = BulkPickupRequest.objects.select_related(
        'citizen',
        'property'
    ).order_by(
        '-created_at'
    )


    # -----------------------------------------------------
    # STATISTICS
    # -----------------------------------------------------

    total_requests = bulk_requests.count()


    pending_count = bulk_requests.filter(
        status='PENDING'
    ).count()


    approved_count = bulk_requests.filter(
        status='APPROVED'
    ).count()


    collected_count = bulk_requests.filter(
        status='COLLECTED'
    ).count()


    rejected_count = bulk_requests.filter(
        status='REJECTED'
    ).count()


    # -----------------------------------------------------
    # CONTEXT
    # -----------------------------------------------------

    context = {

        'bulk_requests': bulk_requests,

        'total_requests': total_requests,

        'pending_count': pending_count,

        'approved_count': approved_count,

        'collected_count': collected_count,

        'rejected_count': rejected_count,

    }


    return render(
        request,
        'worker_bulk_pickup.html',
        context
    )


# =========================================================
# WORKER - APPROVE BULK PICKUP
# =========================================================

@login_required(login_url='login')
def approve_bulk_pickup(request, request_id):

    if request.method == 'POST':

        bulk_request = BulkPickupRequest.objects.filter(
            id=request_id
        ).first()


        if not bulk_request:

            messages.error(
                request,
                "Bulk pickup request not found."
            )

            return redirect(
                'worker_bulk_pickup'
            )


        # Only pending requests can be approved
        if bulk_request.status != 'PENDING':

            messages.warning(
                request,
                "This bulk pickup request has already been processed."
            )

            return redirect(
                'worker_bulk_pickup'
            )


        bulk_request.status = 'APPROVED'


        bulk_request.save(
            update_fields=['status']
        )


        messages.success(
            request,
            f"Bulk pickup request for "
            f"{bulk_request.property.property_id} "
            f"approved successfully."
        )


    return redirect(
        'worker_bulk_pickup'
    )


# =========================================================
# WORKER - REJECT BULK PICKUP
# =========================================================

@login_required(login_url='login')
def reject_bulk_pickup(request, request_id):

    if request.method == 'POST':

        bulk_request = BulkPickupRequest.objects.filter(
            id=request_id
        ).first()


        if not bulk_request:

            messages.error(
                request,
                "Bulk pickup request not found."
            )

            return redirect(
                'worker_bulk_pickup'
            )


        # Only pending requests can be rejected
        if bulk_request.status != 'PENDING':

            messages.warning(
                request,
                "This bulk pickup request has already been processed."
            )

            return redirect(
                'worker_bulk_pickup'
            )


        bulk_request.status = 'REJECTED'


        bulk_request.save(
            update_fields=['status']
        )


        messages.success(
            request,
            f"Bulk pickup request for "
            f"{bulk_request.property.property_id} "
            f"rejected."
        )


    return redirect(
        'worker_bulk_pickup'
    )


# =========================================================
# WORKER - COMPLETE BULK PICKUP
# =========================================================

@login_required(login_url='login')
def complete_bulk_pickup(request, request_id):

    if request.method == 'POST':

        bulk_request = BulkPickupRequest.objects.filter(
            id=request_id
        ).first()


        if not bulk_request:

            messages.error(
                request,
                "Bulk pickup request not found."
            )

            return redirect(
                'worker_bulk_pickup'
            )


        # Only approved requests can be completed
        if bulk_request.status != 'APPROVED':

            messages.warning(
                request,
                "Only approved bulk pickup requests can be marked as collected."
            )

            return redirect(
                'worker_bulk_pickup'
            )


        bulk_request.status = 'COLLECTED'


        bulk_request.save(
            update_fields=['status']
        )


        messages.success(
            request,
            f"Bulk pickup for "
            f"{bulk_request.property.property_id} "
            f"marked as collected."
        )


    return redirect(
        'worker_bulk_pickup'
    )

# =========================================================
# WORKER - COLLECTION HISTORY
# =========================================================

@login_required(login_url='login')
def collection_history(request):

    # -----------------------------------------------------
    # GET ALL COLLECTION RECORDS
    # -----------------------------------------------------

    records = WasteCollectionRecord.objects.select_related(
        'worker',
        'property'
    ).order_by(
        '-collection_date',
        '-created_at'
    )


    # -----------------------------------------------------
    # STATISTICS
    # -----------------------------------------------------

    total_records = records.count()


    # Today's records
    today = timezone.localdate()

    today_records = records.filter(
        collection_date=today
    )

    today_count = today_records.count()


    # -----------------------------------------------------
    # TOTAL WASTE
    # -----------------------------------------------------

    total_biodegradable = sum(
        record.biodegradable or 0
        for record in records
    )


    total_non_biodegradable = sum(
        record.non_biodegradable or 0
        for record in records
    )


    total_plastic = sum(
        record.plastic or 0
        for record in records
    )


    total_paper = sum(
        record.paper or 0
        for record in records
    )


    total_glass = sum(
        record.glass or 0
        for record in records
    )


    total_metal = sum(
        record.metal or 0
        for record in records
    )


    total_electronic = sum(
        record.electronic or 0
        for record in records
    )


    total_hazardous = sum(
        record.hazardous or 0
        for record in records
    )


    # -----------------------------------------------------
    # GRAND TOTAL
    # -----------------------------------------------------

    total_waste = (
        total_biodegradable
        + total_non_biodegradable
        + total_plastic
        + total_paper
        + total_glass
        + total_metal
        + total_electronic
        + total_hazardous
    )


    # -----------------------------------------------------
    # UNIQUE PROPERTIES
    # -----------------------------------------------------

    properties_count = records.values(
        'property'
    ).distinct().count()


    # -----------------------------------------------------
    # CONTEXT
    # -----------------------------------------------------

    context = {

        'records': records,

        'total_records': total_records,

        'today_count': today_count,

        'properties_count': properties_count,

        'total_waste': total_waste,

        'total_biodegradable': total_biodegradable,

        'total_non_biodegradable': total_non_biodegradable,

        'total_plastic': total_plastic,

        'total_paper': total_paper,

        'total_glass': total_glass,

        'total_metal': total_metal,

        'total_electronic': total_electronic,

        'total_hazardous': total_hazardous,

        'today': today,

    }


    return render(
        request,
        'collection_history.html',
        context
    )

# =========================================================
# WORKER - DAILY WORK UPDATE
# =========================================================

@login_required(login_url='login')
def daily_work_update(request):

    today = timezone.localdate()

    # -----------------------------------------------------
    # CHECK IF UPDATE ALREADY EXISTS FOR TODAY
    # -----------------------------------------------------

    existing_update = DailyWorkUpdate.objects.filter(
        worker=request.user,
        update_date=today
    ).first()


    # -----------------------------------------------------
    # POST
    # -----------------------------------------------------

    if request.method == 'POST':

        # Prevent duplicate daily update
        if existing_update:

            messages.warning(
                request,
                "You have already submitted today's work update."
            )

            return redirect(
                'daily_work_update'
            )


        form = DailyWorkUpdateForm(
            request.POST
        )


        if form.is_valid():

            update = form.save(
                commit=False
            )

            update.worker = request.user

            update.update_date = today

            update.save()


            messages.success(
                request,
                "Today's work update submitted successfully!"
            )


            return redirect(
                'daily_work_update'
            )


    # -----------------------------------------------------
    # GET
    # -----------------------------------------------------

    else:

        if existing_update:

            form = DailyWorkUpdateForm(
                instance=existing_update
            )

        else:

            form = DailyWorkUpdateForm()


    # -----------------------------------------------------
    # RECENT UPDATES
    # -----------------------------------------------------

    recent_updates = DailyWorkUpdate.objects.filter(
        worker=request.user
    ).order_by(
        '-update_date',
        '-created_at'
    )[:10]


    # -----------------------------------------------------
    # CONTEXT
    # -----------------------------------------------------

    context = {

        'form': form,

        'today': today,

        'existing_update': existing_update,

        'recent_updates': recent_updates,

    }


    return render(
        request,
        'daily_work_update.html',
        context
    )

# =========================================================
# WORKER - NOTIFICATIONS
# =========================================================

@login_required(login_url='login')
def notifications(request):

    notification_list = Notification.objects.filter(
        recipient=request.user
    ).order_by(
        '-created_at'
    )

    unread_count = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).count()

    context = {

        'notifications': notification_list,

        'unread_count': unread_count,

    }

    return render(
        request,
        'notifications.html',
        context
    )

# =========================================================
# MARK NOTIFICATION AS READ
# =========================================================

@login_required(login_url='login')
def mark_notification_read(request, notification_id):

    notification = Notification.objects.filter(
        id=notification_id,
        recipient=request.user
    ).first()

    if not notification:

        messages.error(
            request,
            "Notification not found."
        )

        return redirect(
            'notifications'
        )

    notification.is_read = True

    notification.save(
        update_fields=['is_read']
    )

    return redirect(
        'notifications'
    )

# =========================================================
# MARK ALL NOTIFICATIONS AS READ
# =========================================================

@login_required(login_url='login')
def mark_all_notifications_read(request):

    if request.method == 'POST':

        Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).update(
            is_read=True
        )

        messages.success(
            request,
            "All notifications marked as read."
        )

    return redirect(
        'notifications'
    )

# =========================================================
# ADMIN - WORKER MANAGEMENT
# =========================================================

@login_required(login_url='login')
def worker_management(request):

    if not request.user.is_staff:

        messages.error(
            request,
            "Admin access required."
        )

        return redirect('login')

    workers = WorkerProfile.objects.select_related(
        'user'
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'worker_management.html',
        {
            'workers': workers
        }
    )

# =========================================================
# ADMIN - CITIZEN MANAGEMENT
# =========================================================

@login_required(login_url='login')
def citizen_management(request):

    if not request.user.is_staff:

        messages.error(
            request,
            "Admin access required."
        )

        return redirect('login')

    citizens = User.objects.filter(
        is_staff=False,
        is_superuser=False
    ).exclude(
        worker_profile__isnull=False
    ).order_by(
        '-date_joined'
    )

    return render(
        request,
        'citizen_management.html',
        {
            'citizens': citizens
        }
    )

# =========================================================
# ADMIN - BULK PICKUP MANAGEMENT
# =========================================================

@login_required(login_url='login')
def admin_bulk_pickup(request):

    if not request.user.is_staff:

        messages.error(
            request,
            "Admin access required."
        )

        return redirect('login')

    requests = BulkPickupRequest.objects.select_related(
        'citizen',
        'property'
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'admin_bulk_pickup.html',
        {
            'requests': requests
        }
    )

# =========================================================
# ADMIN - FOOD DONATION MANAGEMENT
# =========================================================

@login_required(login_url='login')
def admin_food_donations(request):

    if not request.user.is_staff:

        messages.error(
            request,
            "Admin access required."
        )

        return redirect('login')

    donations = FoodRedistributionRequest.objects.filter(
        request_type='DONATE'
    ).select_related(
        'citizen'
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'admin_food_donations.html',
        {
            'donations': donations
        }
    )

    # =========================================================
# ADMIN - FOOD REQUEST MANAGEMENT
# =========================================================

@login_required(login_url='login')
def admin_food_requests(request):

    if not request.user.is_staff:

        messages.error(
            request,
            "Admin access required."
        )

        return redirect('login')

    food_requests = FoodRedistributionRequest.objects.filter(
        request_type='REQUEST'
    ).select_related(
        'citizen'
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'admin_food_requests.html',
        {
            'food_requests': food_requests
        }
    )

# =========================================================
# ADMIN - ILLEGAL DUMPING REPORT MANAGEMENT
# =========================================================

@login_required(login_url='login')
def admin_dumping_reports(request):

    if not request.user.is_staff:

        messages.error(
            request,
            "Admin access required."
        )

        return redirect('login')

    reports = DumpingReport.objects.select_related(
        'citizen'
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'admin_dumping_reports.html',
        {
            'reports': reports
        }
    )

    # =========================================================
# ADMIN - SYSTEM REPORTS
# =========================================================

@login_required(login_url='login')
def admin_reports(request):

    if not request.user.is_staff:
        messages.error(request, "Admin access required.")
        return redirect('login')

    today = timezone.localdate()

    report_type = request.GET.get(
        'report_type',
        'daily'
    )

    selected_date = request.GET.get(
        'date',
        today.strftime('%Y-%m-%d')
    )

    selected_month = request.GET.get(
        'month',
        today.strftime('%Y-%m')
    )

    selected_year = request.GET.get(
        'year',
        str(today.year)
    )

    collections = WasteCollectionRecord.objects.all()

    # DAILY
    if report_type == 'daily':

        try:
            report_date = timezone.datetime.strptime(
                selected_date,
                '%Y-%m-%d'
            ).date()
        except (ValueError, TypeError):
            report_date = today

        collections = collections.filter(
            collection_date=report_date
        )

        report_title = (
            f"Daily Report - {report_date}"
        )

    # MONTHLY
    elif report_type == 'monthly':

        try:
            year, month = map(
                int,
                selected_month.split('-')
            )
        except (ValueError, AttributeError):
            year = today.year
            month = today.month

        collections = collections.filter(
            collection_date__year=year,
            collection_date__month=month
        )

        report_title = (
            f"Monthly Report - {year}-{month:02d}"
        )

    # YEARLY
    elif report_type == 'yearly':

        try:
            year = int(selected_year)
        except (ValueError, TypeError):
            year = today.year

        collections = collections.filter(
            collection_date__year=year
        )

        report_title = (
            f"Yearly Report - {year}"
        )

    # DEFAULT
    else:

        report_type = 'daily'

        collections = collections.filter(
            collection_date=today
        )

        report_title = (
            f"Daily Report - {today}"
        )

    # WASTE TOTALS
    waste_totals = collections.aggregate(

        biodegradable=Sum(
            'biodegradable'
        ),

        non_biodegradable=Sum(
            'non_biodegradable'
        ),

        plastic=Sum(
            'plastic'
        ),

        paper=Sum(
            'paper'
        ),

        glass=Sum(
            'glass'
        ),

        metal=Sum(
            'metal'
        ),

        electronic=Sum(
            'electronic'
        ),

        hazardous=Sum(
            'hazardous'
        ),
    )

    total_biodegradable = (
        waste_totals['biodegradable'] or 0
    )

    total_non_biodegradable = (
        waste_totals['non_biodegradable'] or 0
    )

    total_plastic = (
        waste_totals['plastic'] or 0
    )

    total_paper = (
        waste_totals['paper'] or 0
    )

    total_glass = (
        waste_totals['glass'] or 0
    )

    total_metal = (
        waste_totals['metal'] or 0
    )

    total_electronic = (
        waste_totals['electronic'] or 0
    )

    total_hazardous = (
        waste_totals['hazardous'] or 0
    )

    total_waste = (
        total_biodegradable
        + total_non_biodegradable
        + total_plastic
        + total_paper
        + total_glass
        + total_metal
        + total_electronic
        + total_hazardous
    )

    total_report_collections = collections.count()

    context = {

        # Overall system statistics

        'total_properties':
            Property.objects.count(),

        'total_collections':
            WasteCollectionRecord.objects.count(),

        'total_bulk_pickups':
            BulkPickupRequest.objects.count(),

        'total_food_donations':
            FoodRedistributionRequest.objects.filter(
                request_type='DONATE'
            ).count(),

        'total_food_requests':
            FoodRedistributionRequest.objects.filter(
                request_type='REQUEST'
            ).count(),

        'total_dumping_reports':
            DumpingReport.objects.count(),

        'total_workers':
            WorkerProfile.objects.filter(
                status='ACTIVE'
            ).count(),

        'total_citizens':
            User.objects.filter(
                is_staff=False,
                is_superuser=False
            ).exclude(
                worker_profile__isnull=False
            ).count(),

        # Report information

        'report_type':
            report_type,

        'selected_date':
            selected_date,

        'selected_month':
            selected_month,

        'selected_year':
            selected_year,

        'report_title':
            report_title,

        'report_collections':
            collections.select_related(
                'property',
                'worker'
            ).order_by(
                '-collection_date',
                '-created_at'
            ),

        'total_report_collections':
            total_report_collections,

        # Waste totals

        'total_waste':
            total_waste,

        'report_biodegradable':
            total_biodegradable,

        'report_non_biodegradable':
            total_non_biodegradable,

        'report_plastic':
            total_plastic,

        'report_paper':
            total_paper,

        'report_glass':
            total_glass,

        'report_metal':
            total_metal,

        'report_electronic':
            total_electronic,

        'report_hazardous':
            total_hazardous,
    }

    return render(
        request,
        'admin_reports.html',
        context
    )

# =========================================================
# ADMIN - WASTE STORAGE MANAGEMENT
# =========================================================

@login_required(login_url='login')
def admin_waste_storage(request):

    if not request.user.is_staff:
        messages.error(request, "Admin access required.")
        return redirect('login')

    storage_records = WasteStorageRecord.objects.select_related(
        'collection_record',
        'collection_record__property',
        'collection_record__worker'
    ).order_by(
        '-received_date',
        '-created_at'
    )

    context = {
        'storage_records': storage_records,
    }

    return render(
        request,
        'admin_waste_storage.html',
        context
    )

# =========================================================
# ADMIN - ILLEGAL DUMPING FINE MANAGEMENT
# =========================================================

@login_required(login_url='login')
def admin_dumping_fines(request):

    if not request.user.is_staff:
        messages.error(request, "Admin access required.")
        return redirect('login')

    fines = DumpingFine.objects.select_related(
        'dumping_report',
        'dumping_report__citizen'
    ).order_by(
        '-created_at'
    )

    context = {
        'fines': fines,
    }

    return render(
        request,
        'admin_dumping_fines.html',
        context
    )

@login_required(login_url='login')
def issue_dumping_fine(request):

    if not request.user.is_staff:
        messages.error(request, "Admin access required.")
        return redirect('login')

    reports = DumpingReport.objects.select_related(
        'citizen'
    ).order_by(
        '-created_at'
    )

    if request.method == 'POST':

        report_id = request.POST.get(
            'report_id',
            ''
        ).strip()

        fine_amount = request.POST.get(
            'fine_amount',
            ''
        ).strip()

        reason = request.POST.get(
            'reason',
            ''
        ).strip()

        issued_date = request.POST.get(
            'issued_date',
            ''
        ).strip()

        status = request.POST.get(
            'status',
            'ISSUED'
        ).strip()

        notes = request.POST.get(
            'notes',
            ''
        ).strip()

        if not report_id or not fine_amount or not reason or not issued_date:

            messages.error(
                request,
                "Please fill in all required fields."
            )

            return render(
                request,
                'issue_dumping_fine.html',
                {
                    'reports': reports,
                }
            )

        try:

            report = DumpingReport.objects.get(
                id=report_id
            )

        except DumpingReport.DoesNotExist:

            messages.error(
                request,
                "Selected dumping report was not found."
            )

            return render(
                request,
                'issue_dumping_fine.html',
                {
                    'reports': reports,
                }
            )

        existing_fine = getattr(
            report,
            'fine',
            None
        )

        if existing_fine:

            existing_fine.fine_amount = fine_amount
            existing_fine.reason = reason
            existing_fine.issued_date = issued_date
            existing_fine.status = status
            existing_fine.notes = notes

            existing_fine.save()

            messages.success(
                request,
                "Fine record updated successfully."
            )

        else:

            DumpingFine.objects.create(
                dumping_report=report,
                fine_amount=fine_amount,
                reason=reason,
                issued_date=issued_date,
                status=status,
                notes=notes
            )

            messages.success(
                request,
                "Fine issued successfully."
            )

        return redirect(
            'admin_dumping_fines'
        )

    return render(
        request,
        'issue_dumping_fine.html',
        {
            'reports': reports,
        }
    )

@login_required(login_url='login')
def add_worker(request):

    if not request.user.is_staff:
        messages.error(request, "Admin access required.")
        return redirect('login')

    if request.method == 'POST':

        worker_id = request.POST.get(
            'worker_id',
            ''
        ).strip()

        first_name = request.POST.get(
            'first_name',
            ''
        ).strip()

        last_name = request.POST.get(
            'last_name',
            ''
        ).strip()

        email = request.POST.get(
            'email',
            ''
        ).strip()

        phone = request.POST.get(
            'phone',
            ''
        ).strip()

        password = request.POST.get(
            'password',
            ''
        )

        assigned_area = request.POST.get(
            'assigned_area',
            ''
        ).strip()

        status = request.POST.get(
            'status',
            'ACTIVE'
        ).strip()

        # Required fields

        if not worker_id or not first_name or not password:

            messages.error(
                request,
                "Worker ID, First Name and Password are required."
            )

            return render(
                request,
                'add_worker.html'
            )

        # Check Worker ID

        if User.objects.filter(
            username=worker_id
        ).exists():

            messages.error(
                request,
                "This Worker ID already exists."
            )

            return render(
                request,
                'add_worker.html'
            )

        # Check email if provided

        if email and User.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                "This email is already registered."
            )

            return render(
                request,
                'add_worker.html'
            )

        # Create Django user

        user = User.objects.create_user(
            username=worker_id,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        # Create worker profile

        WorkerProfile.objects.create(
            user=user,
            worker_id=worker_id,
            phone=phone,
            assigned_area=assigned_area,
            status=status
        )

        messages.success(
            request,
            f"Worker {worker_id} added successfully."
        )

        return redirect(
            'worker_management'
        )

    return render(
        request,
        'add_worker.html'
    )