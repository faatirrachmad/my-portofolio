from django.urls import path
from main.views import (
    create_project,
    create_project_ajax,
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
    project_list_fragment,
    create_project_htmx,
    delete_project_htmx,
    edit_project_htmx,
    project_row_htmx,
    update_project_htmx,
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
    path(
        "projects/add/ajax/",
        create_project_ajax,
        name="create_project_ajax",
    ),
    path("projects/htmx/", project_list_fragment, name="project_list_htmx"),
    path("projects/htmx/add/", create_project_htmx, name="create_project_htmx"),
    path(
        "projects/htmx/<uuid:project_id>/delete/",
        delete_project_htmx,
        name="delete_project_htmx",
    ),
    path(
        "projects/htmx/<uuid:project_id>/edit/",
        edit_project_htmx,
        name="edit_project_htmx",
    ),
    path(
        "projects/htmx/<uuid:project_id>/row/",
        project_row_htmx,
        name="project_row_htmx",
    ),
    path(
        "projects/htmx/<uuid:project_id>/update/",
        update_project_htmx,
        name="update_project_htmx",
    ),
]
