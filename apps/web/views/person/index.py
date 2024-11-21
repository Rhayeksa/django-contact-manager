from django.shortcuts import render
from ..utils.nav import nav

# @login_required(login_url="auth:login")


def index(request):

    qry = None
    context = {
        "nav_menu": nav()["person"]
    }

    return render(request=request, template_name="pages/person/index.html", context=context)
