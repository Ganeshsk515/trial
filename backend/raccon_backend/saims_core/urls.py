from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include

def home(request):
    return HttpResponse(
        """
        <h1>SAIMS Backend is running</h1>
        <p>Available endpoints:</p>
        <ul>
          <li><a href="/admin/">/admin/</a></li>
          <li><a href="/auth/register/">/auth/register/</a></li>
          <li><a href="/auth/login/">/auth/login/</a></li>
          <li><a href="/assignments/">/assignments/</a></li>
          <li><a href="/internships/">/internships/</a></li>
          <li><a href="/reports/assignments/">/reports/assignments/</a></li>
          <li><a href="/auth/audit-logs/">/auth/audit-logs/</a></li>
        </ul>
        """,
    )

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('assignments/', include('academics.urls')),
    path('internships/', include('internships.urls')),
    path('api/admin/', include('users.urls')),
    path('reports/', include('academics.urls')),
]
