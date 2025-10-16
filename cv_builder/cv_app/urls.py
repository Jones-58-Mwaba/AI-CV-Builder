from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('create-cv/', views.create_cv, name='create_cv'),
    path('edit-cv/<int:cv_id>/', views.edit_cv, name='edit_cv'),
]