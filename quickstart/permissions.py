from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly


class IsTweetAuthorOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    The request is authenticated as a user, or is a read-only request.
    """
    # Проверка автор ли ты и авторизован
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            obj.author == request.user
        )

#
# class IsFollowedOrReadOnly(IsAuthenticatedOrReadOnly):
#     def has_object_permission(self, request, view, obj):
#         return bool(
#             request.method in SAFE_METHODS or
#             request.user and
#             request.user.is_authenticated
#         )
