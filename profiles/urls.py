from django.urls import path
from  . import views

app_name = "profiles"
urlpatterns = [ 
    path('reqister/', views.register_form_view, name="register"),
    path('login/', views.authentication_form_view, name="login"),
    path('logout/', views.logout_user_view, name="logout"),
    path("my-profile/", views.my_profile_view, name="my_profile"),
    path('profile/<slug>/', views.get_profile_user_view, name="profile_user"),
    path('invataions-friends/', views.invatation_friends_view, name="invatations"),
    path("accept-invite/", views.accept_invite_view, name="accept_invite"),
    path("reject-invite/", views.reject_invite_view, name="reject_invite"),
    path("send-invite/", views.send_invite_view, name="send_invite"),
    path("remove-friends/", views.remove_profile_from_friends_view, name="remove_friend"),
    path("my-profile/update-info/", views.update_profile_info_view, name="update_info"),
]