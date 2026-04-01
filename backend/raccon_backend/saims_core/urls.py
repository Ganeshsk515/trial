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
          <li><a href="/submissions/">/submissions/</a></li>
          <li><a href="/admin/users/">/admin/users/</a></li>
          <li><a href="/reports/assignments/">/reports/assignments/</a></li>
          <li><a href="/audit-logs/">/audit-logs/</a></li>
        </ul>
        """,
    )

urlpatterns = [
    path('', home, name='home'),
    path('', include('users.urls')),
    path('', include('academics.urls')),
    path('', include('internships.urls')),
    path('admin/', admin.site.urls),
]
