"""damienssite3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import permission_required
from uploads.views import UploadView

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) +\
static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +\
[
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')),
    path('upload/', permission_required("uploads.can_add_upload", login_url="/login/")(UploadView.as_view())),
    path('flags/', include('flags.urls')),
    path('', include('content.urls'))
]