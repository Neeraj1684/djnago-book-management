from rest_framework.permissions import BasePermission,SAFE_METHODS

class IsAuthorOrReadOnly(BasePermission):
    """
    Custom permission:
    - Anyone can read (GET)
    - Only the author of the book can update/delete 
    """

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS = [GET, HEAD, OPTIONS]
        if request.method in SAFE_METHODS:
            return True
        
        # For PUT/PATCH/DELETE, only author can modify
        return obj.author.user == request.user