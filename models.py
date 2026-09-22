from django.db import models
from django.contrib.auth.models import User
import uuid


class Property(models.Model):

    PROPERTY_TYPES = [
        ('HOUSE', 'House'),
        ('APARTMENT', 'Apartment'),
        ('HOTEL', 'Hotel'),
        ('RESTAURANT', 'Restaurant'),
        ('SCHOOL', 'School'),
        ('HOSPITAL', 'Hospital'),
        ('COMMERCIAL', 'Commercial Establishment'),
    ]

    property_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='properties'
    )

    owner_name = models.CharField(
        max_length=100
    )

    property_type = models.CharField(
        max_length=30,
        choices=PROPERTY_TYPES
    )

    address = models.TextField()

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        if not self.property_id:
            self.property_id = "SW-" + str(uuid.uuid4().int)[:5]

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.property_id} - {self.owner_name}"


class WasteCollectionRequest(models.Model):

    WASTE_TYPES = [
        ('GENERAL', 'General Waste'),
        ('PLASTIC', 'Plastic'),
        ('PAPER', 'Paper'),
        ('ORGANIC', 'Organic Waste'),
        ('E_WASTE', 'E-Waste'),
        ('OTHER', 'Other'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('COLLECTED', 'Collected'),
        ('REJECTED', 'Rejected'),
    ]

    citizen = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE
    )

    waste_type = models.CharField(
        max_length=30,
        choices=WASTE_TYPES
    )

    description = models.TextField(
        blank=True
    )

    collection_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.citizen.username} - {self.waste_type}"

# =========================================================
# BULK PICKUP REQUEST
# =========================================================

class BulkPickupRequest(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('COLLECTED', 'Collected'),
        ('REJECTED', 'Rejected'),
    ]

    BULK_TYPES = [
        ('FURNITURE', 'Furniture'),
        ('ELECTRONICS', 'Electronics'),
        ('APPLIANCES', 'Appliances'),
        ('CONSTRUCTION', 'Construction Waste'),
        ('GARDEN', 'Garden Waste'),
        ('OTHER', 'Other'),
    ]

    citizen = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE
    )

    bulk_type = models.CharField(
        max_length=30,
        choices=BULK_TYPES
    )

    description = models.TextField()

    preferred_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Bulk Pickup - {self.property.property_id}"


# =========================================================
# REPORT DUMPING
# =========================================================

class DumpingReport(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('INVESTIGATING', 'Investigating'),
        ('RESOLVED', 'Resolved'),
        ('REJECTED', 'Rejected'),
    ]

    DUMPING_TYPES = [
        ('HOUSEHOLD', 'Household Waste'),
        ('PLASTIC', 'Plastic Waste'),
        ('CONSTRUCTION', 'Construction Waste'),
        ('FOOD', 'Food Waste'),
        ('HAZARDOUS', 'Hazardous Waste'),
        ('OTHER', 'Other'),
    ]

    citizen = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    location = models.TextField()

    dumping_type = models.CharField(
        max_length=30,
        choices=DUMPING_TYPES
    )

    description = models.TextField()

    reported_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Dumping Report - {self.citizen.username}"


# =========================================================
# FOOD REDISTRIBUTION REQUEST
# =========================================================

class FoodRedistributionRequest(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('FULFILLED', 'Fulfilled'),
        ('REJECTED', 'Rejected'),
    ]

    REQUEST_TYPES = [
        ('DONATE', 'Donate Food'),
        ('REQUEST', 'Request Food'),
    ]

    citizen = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    request_type = models.CharField(
        max_length=20,
        choices=REQUEST_TYPES
    )

    food_name = models.CharField(
        max_length=150
    )

    quantity = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
    )

    preferred_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Food Request - {self.food_name}"

# =========================================================
class WasteCollectionRecord(models.Model):

    worker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='waste_collection_records'
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='collection_records'
    )

    collection_date = models.DateField()

    biodegradable = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    non_biodegradable = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    plastic = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    paper = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    glass = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    metal = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    electronic = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    hazardous = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.property.property_id} - {self.collection_date}"

# =========================================================
# DAILY WORK UPDATE
# =========================================================

class DailyWorkUpdate(models.Model):

    worker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='daily_work_updates'
    )

    update_date = models.DateField()

    properties_visited = models.PositiveIntegerField(
        default=0
    )

    properties_completed = models.PositiveIntegerField(
        default=0
    )

    total_waste_collected = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    work_summary = models.TextField()

    issues_reported = models.TextField(
        blank=True
    )

    additional_notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.worker.username} - {self.update_date}"

# =========================================================
# WORKER NOTIFICATIONS
# =========================================================

class Notification(models.Model):

    NOTIFICATION_TYPES = [
        ('INFO', 'Information'),
        ('SUCCESS', 'Success'),
        ('WARNING', 'Warning'),
        ('ALERT', 'Alert'),
    ]

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    title = models.CharField(
        max_length=150
    )

    message = models.TextField()

    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default='INFO'
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.recipient.username} - {self.title}"