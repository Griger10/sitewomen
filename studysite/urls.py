from django.conf.urls.static import static
from django.views.decorators.cache import cache_page
from studysite import settings
from women.sitemaps import PostSitemap, CategorySitemap
from women.views import page_not_found
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from women import views
import debug_toolbar

"""
URL configuration for studysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

sitemaps = {'posts': PostSitemap, 'cats': CategorySitemap}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('women.urls')),
    path('users/', include('users.urls', namespace='users')),
    path("__debug__/", include("debug_toolbar.urls")),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('captcha/', include('captcha.urls')),
    path('sitemap.xml', cache_page(86400)(sitemap), {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = page_not_found

admin.site.site_header = 'Панель администрирования'
admin.site.index_header = 'Известные женщины мира'
