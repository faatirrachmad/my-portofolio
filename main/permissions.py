from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    """Public read access; owner writes all data; Editor can update only."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return (
            request.method in ("PUT", "PATCH")
            and (
                request.user.groups.filter(name="Editor").exists()
                or request.user.has_perm("main.change_project")
            )
        )
