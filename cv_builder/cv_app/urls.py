from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-cv/', views.create_cv, name='create_cv'),
    path('edit-cv/<int:cv_id>/', views.edit_cv, name='edit_cv'),
    path('delete-cv/<int:cv_id>/', views.delete_cv, name='delete_cv'), 
    path('preview-cv/<int:cv_id>/', views.preview_cv, name='preview_cv'),  
    path('duplicate-cv/<int:cv_id>/', views.duplicate_cv, name='duplicate_cv'), 
    path('download-cv-pdf/<int:cv_id>/', views.download_cv_pdf, name='download_cv_pdf'),
]