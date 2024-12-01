from django.shortcuts import render


def page_not_found(request, exception):

    return render(None, "404.html", context={})
