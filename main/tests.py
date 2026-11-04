from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from urllib.parse import urlencode
from main.models import Experience, Project, Skill


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


class ProjectHTMXTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", email="owner@example.com", password="test-pass"
        )
        self.client.force_login(self.owner)
        self.project = Project.objects.create(
            title="Portfolio App",
            description="A Django portfolio project.",
            tech_stack="Django",
            repository_url="https://github.com/example/portfolio",
        )

    def test_project_page_exposes_tutorial_fields_and_controls(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(response, "name=\"repository_url\"")
        self.assertContains(response, "hx-post=")
        self.assertContains(response, "hx-trigger=\"keyup changed delay:300ms, search\"")

    def test_htmx_live_search_returns_project_fragment(self):
        response = self.client.get(
            reverse("main:project_list_htmx"), {"title": "portfolio"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Portfolio App")
        self.assertContains(response, "Lihat Repository")
        self.assertNotContains(response, "Belum ada proyek")

    def test_htmx_add_and_inline_edit_project(self):
        add_response = self.client.post(
            reverse("main:create_project_htmx"),
            {
                "title": "New Project",
                "description": "New description",
                "tech_stack": "Python",
                "repository_url": "https://github.com/example/new-project",
            },
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(add_response.status_code, 200)
        self.assertContains(add_response, "hx-swap-oob=\"innerHTML\"")
        created = Project.objects.get(title="New Project")
        edit_response = self.client.get(
            reverse("main:edit_project_htmx", args=[created.pk])
        )
        self.assertContains(edit_response, "name=\"repository_url\"")

        update_response = self.client.put(
            reverse("main:update_project_htmx", args=[created.pk]),
            urlencode({
                "title": "Updated Project",
                "description": "Updated description",
                "tech_stack": "Django",
                "repository_url": "https://github.com/example/updated-project",
            }),
            content_type="application/x-www-form-urlencoded",
        )

        self.assertEqual(update_response.status_code, 200)
        created.refresh_from_db()
        self.assertEqual(created.title, "Updated Project")
        self.assertEqual(
            created.repository_url,
            "https://github.com/example/updated-project",
        )

    def test_htmx_delete_removes_project(self):
        response = self.client.delete(
            reverse("main:delete_project_htmx", args=[self.project.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())
