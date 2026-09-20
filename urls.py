from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/citizen/', views.citizen_dashboard, name='citizen_dashboard'),
    path('dashboard/worker/', views.worker_dashboard, name='worker_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),

    # Property URLs
    path('add-property/', views.add_property, name='add_property'),
    path('my-property/', views.my_property, name='my_property'),
    path('property-list/', views.property_list, name='property_list'),

    path('waste-collection/',views.waste_collection,name='waste_collection'),
    path('bulk-pickup/',views.bulk_pickup,name='bulk_pickup'),
    path('report-dumping/',views.report_dumping,name='report_dumping'),

    path('food-redistribution/',views.food_redistribution,name='food_redistribution'),
]