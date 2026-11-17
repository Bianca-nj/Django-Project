"""
URL configuration for Hospital project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from patient import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'patients', views.PatientViewSet, basename='patient')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.index,name="index"),
    path('login/',views.userlogin,name="login"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('profile/',views.profile,name="profile"),
    path('appointment/',views.appointment,name="appointment"),
    path('logout/',views.logout_view,name="logout"),
    path('add_patient/',views.add_patient,name="add_patient"),

    path('edit/<int:patient_id>/', views.edit_patient, name='edit_patient'),
    path('detail/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('delete/<int:patient_id>/', views.delete_patient, name='delete_patient'),

    path('', include(router.urls)),

    path('make_payment/', views.make_payment, name='make_payment'),
]
