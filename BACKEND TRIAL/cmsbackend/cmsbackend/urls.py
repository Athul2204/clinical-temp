from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    # Django Admin Panel
    path('admin/', admin.site.urls),

    # 🔐 Authentication (JWT)
    path('api/auth/', include('authentication.urls')),

    # 📦 Modules (CLEAN & UNIQUE)
    path('api/administration/', include('administration.urls')),
    path('api/reception/', include('reception.urls')),
    path('doctor/', include('doctor.urls')),
    path('api/pharmacist/', include('pharmacist.urls')),
    path('api/labtechnician/', include('labtechnician.urls')),
]