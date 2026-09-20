from django import forms

from .models import (
    Property,
    WasteCollectionRequest,
    BulkPickupRequest,
    DumpingReport,
    FoodRedistributionRequest,
)


# =========================================================
# PROPERTY FORM
# =========================================================

class PropertyForm(forms.ModelForm):

    class Meta:
        model = Property

        fields = [
            'property_type',
            'address',
            'phone',
        ]

        widgets = {

            'property_type': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'address': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Enter complete property address'
                }
            ),

            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter phone number'
                }
            ),
        }

        labels = {
            'property_type': 'Property Type',
            'address': 'Property Address',
            'phone': 'Contact Phone',
        }


# =========================================================
# WASTE COLLECTION FORM
# =========================================================

class WasteCollectionRequestForm(forms.ModelForm):

    class Meta:
        model = WasteCollectionRequest

        fields = [
            'waste_type',
            'description',
            'collection_date',
        ]

        widgets = {

            'waste_type': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Enter waste details'
                }
            ),

            'collection_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),
        }


# =========================================================
# BULK PICKUP FORM
# =========================================================

class BulkPickupRequestForm(forms.ModelForm):

    class Meta:
        model = BulkPickupRequest

        fields = [
            'bulk_type',
            'description',
            'preferred_date',
        ]

        widgets = {

            'bulk_type': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Enter details about the bulky waste'
                }
            ),

            'preferred_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),
        }


# =========================================================
# DUMPING REPORT FORM
# =========================================================

class DumpingReportForm(forms.ModelForm):

    class Meta:
        model = DumpingReport

        fields = [
            'location',
            'dumping_type',
            'description',
            'reported_date',
        ]

        widgets = {

            'location': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Enter dumping location'
                }
            ),

            'dumping_type': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Describe the illegal dumping'
                }
            ),

            'reported_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),
        }


# =========================================================
# FOOD REDISTRIBUTION FORM
# =========================================================

class FoodRedistributionRequestForm(forms.ModelForm):

    class Meta:
        model = FoodRedistributionRequest

        fields = [
            'request_type',
            'food_name',
            'quantity',
            'description',
            'preferred_date',
        ]

        widgets = {

            'request_type': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'food_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Example: Cooked rice, bread, vegetables'
                }
            ),

            'quantity': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Example: 10 kg / 20 meals'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Enter additional details'
                }
            ),

            'preferred_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),
        }