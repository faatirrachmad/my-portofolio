from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "tech_stack",
            "project_url",
            "repository_url",
            "project_image_url",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]
        read_only_fields = ["id", "star_count", "is_starred", "starred_by_names"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Judul proyek tidak boleh kosong.")
        return value

    def validate_description(self, value):
        return strip_tags(value)

    def validate_tech_stack(self, value):
        return strip_tags(value).strip()

    def get_star_count(self, project):
        return project.starred_by.count()

    def get_is_starred(self, project):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return project.starred_by.filter(pk=request.user.pk).exists()

    def get_starred_by_names(self, project):
        return ", ".join(user.username for user in project.starred_by.all())
