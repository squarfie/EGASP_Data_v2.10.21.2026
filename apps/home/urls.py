# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path, include
from apps.home import views
from apps.authentication.decorators import admin_required



urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('crf/', views.crf_data,name='crf_data'),
    path('show/', views.show_data,name='show_data'),
    path('reports/monthly/', views.monthly_report, name='monthly_report'),
    path('edit/<int:id>/',views.edit_data,name='edit_data'),
    path('delete/<int:id>/',views.delete_data,name='delete_data'),
    path('generate-pdf/<int:id>/', views.generate_pdf, name='generate_pdf'),
    path('clinic-add/', admin_required(views.add_dropdown),name='add_dropdown'),
    path('clinic-view', admin_required(views.clinic_view),name='clinic_view'),
    path('clinic-delete/<int:id>/',admin_required(views.delete_dropdown),name='delete_dropdown'),
    path("clinic/edit/<int:pk>/", admin_required(views.add_dropdown), name="edit_clinic"),
    path("search/", views.search, name="search"),
    path('clinic-code/', views.get_clinic_code, name='get_clinic_code'),
    path('breakpoints-view/', admin_required(views.breakpoints_view), name='breakpoints_view'),
    path('breakpoints-delete/<int:id>', admin_required(views.breakpoints_del), name='breakpoints_del'),
    path('breakpoints-add/', admin_required(views.add_breakpoints), name='add_breakpoints'),
    path('breakpoints-edit/<int:pk>/', admin_required(views.add_breakpoints), name='edit_breakpoints'),
    path('breakpoints-upload/', admin_required(views.upload_breakpoints), name='upload_breakpoints'),
    path('breakpoints-deleteAll/', admin_required(views.delete_all_breakpoints), name='delete_all_breakpoints'),
    path('breakpoints-export/', admin_required(views.export_breakpoints), name='export_breakpoints'),
    path('test_results-view/', admin_required(views.abxentry_view), name='abxentry_view'),
    path('specimens/', admin_required(views.specimen_list), name='specimen_list'),
    path('specimens-add/', admin_required(views.add_specimen), name='add_specimen'),
    path('specimens-edit/<int:pk>/', admin_required(views.edit_specimen), name='edit_specimen'),
    path('specimens-delete/<int:pk>/', admin_required(views.delete_specimen), name='delete_specimen'),
    path('generate_gs/<int:id>/', views.generate_gs, name='generate_gs'),
    path('antibioticentry-export/', admin_required(views.export_Antibioticentry), name='export_Antibioticentry'),
   
    path('contact/add/', admin_required(views.add_contact), name='add_contact'),
    path('contact/delete/<int:id>/', admin_required(views.delete_contact), name='delete_contact'),
    path('contact/view/', admin_required(views.contact_view), name='contact_view'),
    path('contact/edit/<int:pk>/', admin_required(views.edit_contact), name='edit_contact'),
    path('get_clinic_staff_details/', views.get_clinic_staff_details, name='get_clinic_staff_details'),
    
    path('clinstaff/add/', admin_required(views.add_clin_pers), name='add_clin_pers'),
    path('clinstaff/view/', admin_required(views.view_clin_pers), name='view_clin_pers'),
    path('clinstaff/edit/<int:pk>/', admin_required(views.edit_clin_pers), name='edit_clin_pers'),
    path('clinstaff/del/<int:pk>/', admin_required(views.delete_clin_pers), name='delete_clin_pers'),
    path('get_clinic_pers_details/', views.get_clinic_pers_details, name='get_clinic_pers_details'),
   
    
    path("add-location/", admin_required(views.add_location), name="add_location"),
    path('upload-location/', admin_required(views.upload_locations), name='upload_locations'),
    path('view-location/', admin_required(views.view_locations), name='view_locations'),
    path('delete_cities/', admin_required(views.delete_cities), name='delete_cities'),
    path('delete_city/<int:id>/', admin_required(views.delete_city), name='delete_city'),
    path('download_combined_table/', admin_required(views.download_combined_table), name='download_combined_table'),
    path('download/', admin_required(views.download_date_range_table), name='download_date_range_table'),
    path('upload-egasp/', admin_required(views.upload_egasp), name='upload_egasp'),
    path('upload-antibiotic-entries/', admin_required(views.upload_antibiotic_entries), name='upload_antibiotic_entries'),
    path('get-cities/', views.get_cities_by_province, name='get_cities_by_province'),
    path('delete-all-egasp/', admin_required(views.delete_all_egasp), name='delete_all_egasp'),
    path('edit_city/<int:id>/', admin_required(views.edit_city), name='edit_city'),
    path('check-egasp-id/', views.check_egasp_id, name='check_egasp_id'),

    # path("ajax/get-cities/", views.get_cities, name="get_cities"),

   
     
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
 
    

]
