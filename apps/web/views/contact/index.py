from django.shortcuts import render
from sqlalchemy.sql import text

from configs.db import MYSQL_DB, session

from ..utils.nav import nav

# @login_required(login_url="auth:login")


def index(request):

    context = {
        "page": "detail",
        "nav_menu": nav()["contact"],
        "contact": {"data": []},
    }

    qry = session.execute(
        text(
            f"""
            SELECT contact_id, name, age, gender, phone, email, created_at
            FROM {MYSQL_DB}.contact
            WHERE deleted_at IS NULL
            """
        )
    ).mappings().fetchall()
    context["contact"]["data"] = qry

    return render(request=request, template_name="pages/contact/index.html", context=context)
