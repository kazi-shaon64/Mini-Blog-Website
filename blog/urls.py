from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("post/<int:id>/", views.post_detail, name="post_detail"),
    path("create/", views.create_post, name="create_post"),
    path("post/<int:id>/edit/", views.edit_post, name="edit_post"),
    path("post/<int:id>/delete/", views.delete_post, name="delete_post"),
    path("post/<int:id>/like/", views.like_post, name="like_post"),
    path("post/<int:id>/comment/", views.add_comment, name="add_comment"),
    path(
        "profile/",
        views.profile,
        name="profile"
    ),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("search/", views.search, name="search"),
]