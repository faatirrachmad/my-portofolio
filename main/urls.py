from django.urls import path

from main.views import (
    create_project,
    delete_project,
    login_user,
    logout_user,
    register,
    show_experience,
    show_main,
    show_projects,
    show_skills,
    toggle_star,
    update_project,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("skills/", show_skills, name="show_skills"),
    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path(
        "projects/<uuid:project_id>/delete/",
        delete_project,
        name="delete_project",
    ),
    path(
        "projects/<uuid:project_id>/edit/",
        update_project,
        name="update_project",
    ),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path(
        "projects/<uuid:project_id>/star/",
        toggle_star,
        name="toggle_star",
    ),
]
