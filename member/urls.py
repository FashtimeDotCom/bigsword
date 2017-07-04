from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^login/',views.LoginView.as_view(),name='member_login'),
    url(r'^logout/',views.LogoutView.as_view(), name='member_logout'),
    url(r'^resiter/', views.RegisterView.as_view(), name='member_register'),
]