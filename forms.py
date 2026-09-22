from django import forms

from .models import (
    Property,
    WasteCollectionRequest,
    BulkPickupRequest,
    DumpingReport,
    FoodRedistributionRequest,
    WasteCollectionRecord,
    DailyWorkUpdate,
)

class WasteCollectionRecordForm(forms.ModelForm):

    class Meta:
        model = WasteCollectionRecord

        fields = [
            'biodegradable',
            'non_biodegradable',
            'plastic',
            'paper',
            'glass',
            'metal',
            'electronic',
            'hazardous',
            'notes',
        ]

        widgets = {
            'biodegradable': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00 kg'
            }),

            'non_biodegradable': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00 kg'
            }),

            'plastic': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00 kg'
            }),

            'paper': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00 kg'
            }),

            'glass': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00 kg'
            }),

            'metal': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00 kg'
            }),

            'electronic': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00 kg'
            }),

            'hazardous': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00 kg'
            }),

            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter collection notes...'
            }),
        }

        labels = {
            'biodegradable': 'Biodegradable Waste (kg)',
            'non_biodegradable': 'Non-Biodegradable Waste (kg)',
            'plastic': 'Plastic (kg)',
            'paper': 'Paper (kg)',
            'glass': 'Glass (kg)',
            'metal': 'Metal (kg)',
            'electronic': 'Electronic Waste (kg)',
            'hazardous': 'Hazardous Waste (kg)',
            'notes': 'Collection Notes',
        }


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

# =========================================================
# DAILY WORK UPDATE FORM
# =========================================================

class DailyWorkUpdateForm(forms.ModelForm):

    class Meta:

        model = DailyWorkUpdate

        fields = [
            'properties_visited',
            'properties_completed',
            'total_waste_collected',
            'work_summary',
            'issues_reported',
            'additional_notes',
        ]

        widgets = {

            'properties_visited': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '0',
                    'placeholder': 'Enter number of properties visited'
                }
            ),

            'properties_completed': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '0',
                    'placeholder': 'Enter number of completed collections'
                }
            ),

            'total_waste_collected': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': '0.01',
                    'min': '0',
                    'placeholder': 'Enter total waste collected in kg'
                }
            ),

            'work_summary': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Describe the work completed today...'
                }
            ),

            'issues_reported': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Mention any issues encountered during collection...'
                }
            ),

            'additional_notes': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Enter any additional notes...'
                }
            ),
        }

        labels = {

            'properties_visited':
                'Properties Visited',

            'properties_completed':
                'Properties Completed',

            'total_waste_collected':
                'Total Waste Collected (kg)',

            'work_summary':
                'Work Summary',

            'issues_reported':
                'Issues / Problems Reported',

            'additional_notes':
                'Additional Notes',
        }