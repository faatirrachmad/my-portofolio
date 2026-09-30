from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.http import HttpResponseNotAllowed
from main.forms import ProjectForm
from main.models import Experience, Project, Skill
from django.views.decorators.http import require_POST


def show_main(request):
    context = {
        "name": "Faatir Wibowo Rachmad",
        "npm": "2506595146",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Information Systems student at Universitas Indonesia focusing on "
            "Product Management and Data Science. Driven to combine data "
            "analytics with strategic thinking to build impactful digital products."
        ),
        # Cookie last_login dibaca untuk ditampilkan pada halaman profil.
        "last_login": request.COOKIES.get(
            "last_login",
            "Belum ada sesi login / Cookie tidak ditemukan",
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Faatir Wibowo Rachmad",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def show_skills(request):
    # Data dari model dikirim ke template agar halaman bersifat dinamis.
    context = {
        "name": "Faatir Wibowo Rachmad",
        "skill_list": Skill.objects.all(),
    }
    return render(request, "skills.html", context)


def show_projects(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all().prefetch_related("starred_by")

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    context = {
        "name": "Faatir Wibowo Rachmad",
        "project_list": projects,
        "title_query": title_query,
        "form": ProjectForm(),
    }
    return render(request, "projects.html", context)


@login_required(login_url="/login/")
def create_project(request):
    # Hanya pemilik portofolio yang boleh membuat proyek.
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Faatir Wibowo Rachmad",
        "form": form,
    }
    return render(request, "projects_form.html", context)


def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    data = [
        {
            "id": str(project.id),
            "title": project.title,
            "description": project.description,
            "tech_stack": project.tech_stack,
            "project_url": project.project_url,
            "project_image_url": project.project_image_url,
        }
        for project in projects
    ]

    return JsonResponse(data, safe=False)


@login_required(login_url="/login/")
def delete_project(request, project_id):
    # Editor tidak boleh menghapus meskipun boleh mengubah proyek.
    if not request.user.is_superuser:
        raise PermissionDenied

    # Penghapusan hanya boleh berasal dari form POST, bukan membuka URL dengan GET.
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    project = get_object_or_404(Project, pk=project_id)
    project.delete()
    messages.success(request, "Project berhasil dihapus!")
    return redirect("main:show_projects")


@login_required(login_url="/login/")
def update_project(request, project_id):
    # Pemilik adalah superuser; Editor mendapat permission change_project.
    if not request.user.has_perm("main.change_project"):
        raise PermissionDenied

    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek berhasil diperbarui!")
        return redirect("main:show_projects")

    context = {
        "name": "Faatir Wibowo Rachmad",
        "form": form,
        "project": project,
    }
    return render(request, "projects_form.html", context)


def register(request):
    # UserCreationForm menangani validasi username dan konfirmasi password.
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Faatir Wibowo Rachmad",
        "form": form,
    }
    return render(request, "register.html", context)


def login_user(request):
    # AuthenticationForm memeriksa kredensial melalui sistem autentikasi Django.
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        auth_login(request, user)

        # Django menyimpan session ID; cookie khusus ini hanya mencatat waktu login.
        response = redirect("main:show_main")
        response.set_cookie(
            "last_login",
            timezone.localtime().strftime("%Y-%m-%d %H:%M:%S"),
        )
        return response

    context = {
        "name": "Faatir Wibowo Rachmad",
        "form": form,
    }
    return render(request, "login.html", context)


def logout_user(request):
    # Logout menghapus session autentikasi dan cookie waktu login dari browser.
    auth_logout(request)
    response = redirect("main:show_main")
    response.delete_cookie("last_login")
    return response


@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    # Star adalah perubahan data, jadi hanya boleh dikirim lewat POST.
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    # Jika sudah memberi star, batalkan; jika belum, tambahkan.
    if project.starred_by.filter(pk=request.user.pk).exists():
        project.starred_by.remove(request.user)
    else:
        project.starred_by.add(request.user)

    return redirect("main:show_projects")


@require_POST
@login_required(login_url="/login/")
def create_project_ajax(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ProjectForm(request.POST)

    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"success": True, "message": "Proyek berhasil ditambahkan."},
            status=201,
        )

    return JsonResponse(
        {
            "success": False,
            "errors": form.errors.get_json_data(),
        },
        status=400,
    )
