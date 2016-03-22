# coding=utf-8

from django.conf.urls import url

from api.v1 import views

urlpatterns = [
    url(
        r'^device/apns/?$',
        views.CustomAPNSDeviceAuthorizedViewSet.as_view({'post': 'create'})
    ),
    url(
        r'^device/gcm/?$',
        views.CustomGCMDeviceAuthorizedViewSet.as_view({'post': 'create'})
    ),

    url(
        r'^registration$',
        views.RegistrationView.as_view(),
        name='registration'
    ),
    url(
        r'^confirmation$',
        views.ConfirmationView.as_view(),
        name='confirmation'
    ),
    url(
        r'^reconfirmation$',
        views.ReconfirmationView.as_view(),
        name='reconfirmation'
    ),
    url(
        r'^authentication$',
        views.AuthenticationView.as_view(),
        name='authentication'
    ),
    url(
        r'^password/restore$',
        views.RestorePasswordRequestView.as_view(),
        name='password.restore'
    ),
    url(
        r'^password/restore/change$',
        views.RestorePasswordView.as_view(),
        name='password.restore.change'
    ),
    url(
        r'^password/change$',
        views.ChangePasswordView.as_view(),
        name='password.change'
    ),
    url(
        r'^profile$',
        views.ProfileView.as_view(),
        name='profile'
    ),
]
