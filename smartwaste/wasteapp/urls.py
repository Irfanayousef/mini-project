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
    path('property/<int:property_id>/',views.property_detail,name='property_detail'),
    path('property/<int:property_id>/edit/',views.edit_property,name='edit_property'),
    path('property/<int:property_id>/delete/',views.delete_property,name='delete_property'),
    path('collection-records/',views.collection_records,name='collection_records'),
    path('worker-management/',views.worker_management,name='worker_management'),
    path('worker-management/add/',views.add_worker,name='add_worker'),
    path('citizen-management/',views.citizen_management,name='citizen_management'),


    path('waste-collection/',views.waste_collection,name='waste_collection'),
    path('bulk-pickup/',views.bulk_pickup,name='bulk_pickup'),
    path('report-dumping/',views.report_dumping,name='report_dumping'),
    path('food-redistribution/',views.food_redistribution,name='food_redistribution'),

    path('worker/verify-property/',views.verify_property,name='verify_property'),
    path('worker/record-collection/<str:property_id>/',views.record_collection,name='record_collection'),
    path('worker/my-collection-areas/',views.my_collection_areas,name='my_collection_areas'),

    # =========================================================
      # WORKER BULK PICKUP
    # =========================================================

    path('worker/bulk-pickup/',views.worker_bulk_pickup,name='worker_bulk_pickup'),
    path('worker/bulk-pickup/<int:request_id>/approve/',views.approve_bulk_pickup,name='approve_bulk_pickup'),
    path('worker/bulk-pickup/<int:request_id>/reject/',views.reject_bulk_pickup,name='reject_bulk_pickup'),
    path('worker/bulk-pickup/<int:request_id>/complete/',views.complete_bulk_pickup,name='complete_bulk_pickup'),

    path('worker/collection-history/',views.collection_history,name='collection_history'),
    path('worker/daily-work-update/',views.daily_work_update,name='daily_work_update'),

    path('worker/notifications/',views.notifications,name='notifications'),
    path('worker/notifications/<int:notification_id>/read/',views.mark_notification_read,name='mark_notification_read'),
    path('worker/notifications/mark-all-read/',views.mark_all_notifications_read,name='mark_all_notifications_read'),
    
    path('bulk-pickup-management/',views.admin_bulk_pickup,name='admin_bulk_pickup'),
    path('food-donations-management/',views.admin_food_donations,name='admin_food_donations'),
    path('food-requests-management/',views.admin_food_requests,name='admin_food_requests'),
    path('dumping-reports-management/',views.admin_dumping_reports,name='admin_dumping_reports'),
    path('system-reports/',views.admin_reports,name='admin_reports'),
    path('waste-storage/',views.admin_waste_storage,name='admin_waste_storage'),
    path('dumping-fines/',views.admin_dumping_fines,name='admin_dumping_fines'),
    path('dumping-fines/add/',views.issue_dumping_fine,name='issue_dumping_fine'),
    
]