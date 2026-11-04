from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from main.models import Experience, Skill


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(
            response, f'href="{reverse("main:show_experience")}"'
        )

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")
        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(
            response, f'href="{reverse("main:show_main")}"'
        )

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))
        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))
        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")

    def test_skills_url_is_accessible(self):
        response = self.client.get(reverse("main:show_skills"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "skills.html")

    def test_skills_page_displays_data(self):
        skill = Skill.objects.create(
            name="Python",
            category="technical",
            description="Bahasa pemrograman untuk pengembangan aplikasi.",
        )

        response = self.client.get(reverse("main:show_skills"))

        self.assertContains(response, skill.name)
        self.assertContains(response, skill.description)
        self.assertContains(response, "Technical Skill")

    def test_empty_skills_page(self):
        response = self.client.get(reverse("main:show_skills"))

        self.assertContains(response, "Belum ada skill yang ditambahkan.")

    def test_projects_page_uses_drf_ajax_and_csrf_cookie(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="project-search-form"')
        self.assertContains(response, 'id="grid"')
        self.assertContains(response, 'const BASE_PROJECTS_ENDPOINT = "/api/v1/projects/";')
        self.assertContains(response, "X-CSRFToken")
        self.assertNotContains(response, "hx-get=")
        self.assertIn("csrftoken", response.cookies)

        owner = User.objects.create_superuser(
            username="projects-owner",
            password="test-password",
            email="projects-owner@example.com",
        )
        self.client.force_login(owner)
        owner_page = self.client.get(reverse("main:show_projects"))
        self.assertContains(owner_page, 'id="project-form"')


