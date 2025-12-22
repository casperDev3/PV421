from rest_framework import permissions


class IsManagerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Read-only permissions for any request
        if request.method in permissions.SAFE_METHODS:  # SAFE_METHODS are GET, HEAD, OPTIONS
            return True

        # Authenticated users only
        if not request.user or not request.user.is_authenticated:
            return False

        # Manager group access
        if request.user.groups.filter(name='Managers').exists():
            return True

        # High-level admin access
        if request.user.is_superuser:
            return True

        # Had specific permissions for each action
        if request.method == 'POST' and request.user.has_perm('products.add_product'):
            return True
        if request.method in ['PUT', 'PATCH'] and request.user.has_perm('products.change_product'):
            return True
        if request.method == 'DELETE' and request.user.has_perm('products.delete_product'):
            return True

        # Default deny
        return False


class IsManagerCanOnlyCreateOrEdit(permissions.BasePermission):
    def has_permission(self, request, view):
        # Read-only permissions for any request
        if request.method in permissions.SAFE_METHODS:  # SAFE_METHODS are GET, HEAD, OPTIONS
            print("Read-only request")
            return True

        # Authenticated users only
        if not request.user or not request.user.is_authenticated:
            print("User is not authenticated")
            return False

        # Manager group can create or edit
        if request.user.groups.filter(name='Managers').exists():
            print("User is in managers group")
            if request.method in ['POST', 'PUT', 'PATCH']:
                print("Manager creating or editing")
                return True
            else:
                print("Manager trying to delete - denied")
                return False

        # High-level admin access
        if request.user.is_superuser:
            print("Superuser access")
            return True

        # Default deny
        print("Default deny")
        return False
