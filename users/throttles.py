from rest_framework.throttling import UserRateThrottle

class AdminUserRateThrottle(UserRateThrottle):
    scope = "admin"

    def allow_request(self, request, view):
        # Inicjalizuj atrybuty, żeby DRF się nie wykrzaczył
        self.key = self.get_cache_key(request, view)
        self.history = self.cache.get(self.key, []) if self.key else []
        self.now = self.timer()
        if request.user.is_staff:
            return super().allow_request(request, view)
        return False