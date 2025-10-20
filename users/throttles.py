from rest_framework.throttling import UserRateThrottle

class AdminUserRateThrottle(UserRateThrottle):
    scope = 'admin'

    def allow_request(self, request, view):
        if request.user.is_staff:
            return super().allow_request(request, view)
        return False
