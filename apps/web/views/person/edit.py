from django.shortcuts import render


# @login_required(login_url="auth:login")


def edit(request):

    qry = None
    context = {}

    return render(request=request, template_name="pages/person/edit.html", context=context)
