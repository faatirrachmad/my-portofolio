from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import ProjectForm
from main.models import Experience, Project, Skill


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
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    context = {
        "name": "Faatir Wibowo Rachmad",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "projects.html", context)


def create_project(request):
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

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")


def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")


def update_project(request, project_id):
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
