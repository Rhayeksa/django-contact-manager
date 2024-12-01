"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf.urls.static import static
# handler404 = "apps.web.views.page_not_found"
from django.shortcuts import render
# from django.contrib import admin
from django.urls import include, path
# from django.views.defaults import page_not_found

# from django.conf.urls import handler404
# from apps.web.views.page_not_found import page_not_found
from .settings import STATIC_ROOT, STATIC_URL


# def page_not_foundx(request):

#     # return render(None, "404.html", context={})
#     return page_not_found(request, None, "404.html")


urlpatterns = [
    # path('admin/', admin.site.urls),
    path(route="", view=include(arg="apps.web.urls")),
    # path(route="*", view=page_not_foundx),
]

urlpatterns += static(prefix=STATIC_URL, document_root=STATIC_ROOT)
