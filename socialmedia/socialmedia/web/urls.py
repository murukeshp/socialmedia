from django.urls import path
from .views import *
urlpatterns = [
    path("register/",SignUpView.as_view(),name="signup"),
    path("login/",SignInView.as_view(),name="signin"),
    path("index/",IndexView.as_view(),name="index"),
    path("posts/<int:id>/comment/add/",add_comments,name="add-comments"),
    path("post/<int:id>/like/add/",like_post,name="add-like"),
    path("logout",sign_out_view,name="sign-out"),
    path("user/<int:id>/follower/add",add_follower, name="add-follower"),
    path("post/<int:id>/remove",post_delete,name="post-delete"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("people/", ListPeopleView.as_view(),name="people"),
    # path("users/profile/<int:id>/change",EditprofileView.as_view(),name="edit-profile")
]
