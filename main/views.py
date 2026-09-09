from django.shortcuts import render

from main.models import Experience


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
