from django.urls import path, include
from django.conf.urls import url
from users import views
from rest_framework.authtoken import views as v


urlpatterns=[
    url(r'^login/', views.ObtainExpiringAuthToken.as_view()),
    url(r'^register/', views.RegisterView.as_view()),
]