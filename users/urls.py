from django.urls import path, include
from django.conf.urls import url
from users import views
from rest_framework.authtoken import views as v


urlpatterns=[
    #path('passwordless/', include('drfpasswordless.urls')),
    #url(r'^token-auth/', v.obtain_auth_token),
    #url(r'^expiring-token-auth/', views.ObtainExpiringAuthToken.as_view()),
    url(r'^expiring-token-auth/', views.SuperUserObtainExpiringAuthToken.as_view()),
    #url(r'^change-password/', views.ChangePasswordView.as_view()),
]