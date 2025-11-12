"""
URL configuration for person_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from django.urls import path
from .views import PersonListCreateAPIView, PersonDetailAPIView, health

urlpatterns = [
    path("api/v1/persons", PersonListCreateAPIView.as_view(), name="persons-list-create"),
    path("api/v1/persons/<int:pk>", PersonDetailAPIView.as_view(), name="persons-detail"),
    path("api/v1/health", health, name="health"),
]
