from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import (
    Property,
    WasteCollectionRequest,
    BulkPickupRequest,
    DumpingReport,
    FoodRedistributionRequest,
    WasteCollectionRecord,
    DailyWorkUpdate,
    Notification,

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

            return redirect(
                'login'
            )


        # Username is email
        username = email


        # Create user
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


        return redirect(
            'login'
        )


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


# =========================================================
# WORKER - VERIFY PROPERTY
# =========================================================

@login_required(login_url='login')
def verify_property(request):

    property_obj = None

    searched_id = ''


    # -----------------------------------------------------
    # POST SEARCH
    # -----------------------------------------------------

    if request.method == 'POST':

        searched_id = request.POST.get(
            'property_id',
            ''
        ).strip().upper()


    # -----------------------------------------------------
    # GET SEARCH
    # -----------------------------------------------------

    elif request.method == 'GET':

        searched_id = request.GET.get(
            'property_id',
            ''
        ).strip().upper()


    # -----------------------------------------------------
    # FIND PROPERTY
    # -----------------------------------------------------

    if searched_id:

        property_obj = Property.objects.filter(
            property_id=searched_id
        ).first()


        if not property_obj:

            messages.error(
                request,
                f"No property found with Property ID: {searched_id}"
            )


    return render(
        request,
        'verify_property.html',
        {
            'property': property_obj,
            'searched_id': searched_id,
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