from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^login/',views.LoginView.as_view(),name='member_login'),
    url(r'^logout/',views.LogoutView.as_view(), name='member_logout'),
    url(r'^logout/(?P<next>register|login)', views.LogoutView.as_view(),name='member_logout'),
    url(r'^register/', views.RegisterView.as_view(), name='member_register'),
    url(r'^change/', views.ChangePassView.as_view(), name='member_user_change'),
    url(r'^change/', views.ChangePassView.as_view(), name='member_non_user_change'),
    url(r'^change/(?P<user>\w+)/(?P<confirm>[a-zA-Z0-9]{16})', views.ChangePassView.as_view(), name='member_non_user_change'),
    url(r'^change/(?P<u>\w+)', views.ChangePassView.as_view(), name='member_non_user_change_done'),
]