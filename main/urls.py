from django.urls import path
from main.views import (
    create_project,
    delete_project,
    get_projects_json,
    show_experience,
    show_main,
    show_projects,
    show_skills,
    update_project,
    toggle_star,
    register,
    login_user,
    logout_user,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("skills/", show_skills, name="show_skills"),
    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/delete/",
         delete_project, name="delete_project"),
    path("projects/<uuid:project_id>/edit/",
         update_project,
         name="update_project",
         ),
    # URL untuk pendaftaran akun dan sesi login pengguna.
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    # URL POST untuk memberi atau membatalkan star pada proyek.
    path(
        "projects/<uuid:project_id>/star/",
        toggle_star,
        name="toggle_star",
    ),
]
