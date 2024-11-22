import json

from django.shortcuts import render
from sqlalchemy.sql import text

from configs.db import MYSQL_DB, session

from ..utils.nav import nav

# @login_required(login_url="auth:login")


def detail(request, id):

    context = {
        "page": "detail",
        "nav_menu": nav()["contact"],
        "bio": {
            "field": {
                "name": {"label": "Name", "value": ""},
                "age": {"label": "Age", "value": 0},
                "phone": {"label": "Phone", "value": "", "msg_err": []},
                "email": {"label": "Email", "value": "", "msg_err": []},
                "gender": {"label": "Gender", "value": "", "opt": (("", "---------"), ("1", "Pria"), ("0", "Wanita"))},
                "portfolio": {"label": "Portfolio", "value": "", "msg_err": []},
                "photo": {"label": "Photo", "url": ""},
                "address": {"label": "Address", "value": ""},
            },
            "data": {"photo_url": "", "contact_id": id}
        },
        "edu": {
            "field": {
                "category": {"label": "Category", "opt": (("", "---------"), ("High School", "High School"), ("University", "University"), ("Course", "Course"))},
            },
            "data": [],
        },
        "work": {
            "field": {},
            "data": [],
        },
    }

    try:
        qry = session.execute(
            text(
                f"""
                SELECT name, age, gender, phone, email, portfolio, photo, address
                FROM {MYSQL_DB}.contact
                WHERE contact_id = :contact_id
                AND deleted_at IS NULL
                """
            ), {"contact_id": id}
        ).mappings().fetchone()
        if qry == None:
            session.commit()
            session.close()
            return render(request=None, template_name="404.html", context={"nav_menu": nav()["contact"], "msg": "ID not found"})
        context["bio"]["field"]["name"]["value"] = qry["name"]
        context["bio"]["field"]["age"]["value"] = qry["age"]
        context["bio"]["field"]["gender"]["value"] = qry["gender"]
        context["bio"]["field"]["phone"]["value"] = qry["phone"]
        context["bio"]["field"]["email"]["value"] = qry["email"]
        context["bio"]["field"]["portfolio"]["value"] = qry["portfolio"]
        context["bio"]["field"]["address"]["value"] = qry["address"]

        if qry["photo"] != None:
            photo = json.loads(qry["photo"])
            photo = photo["data"]["url"]
        context["bio"]["data"]["photo_url"] = "" if qry["photo"] == None else photo

        qry = session.execute(
            text(
                f"""
                SELECT name, major, category, date_in, date_out
                FROM {MYSQL_DB}.education
                WHERE contact_id = :contact_id
                AND deleted_at IS NULL
                """
            ), {"contact_id": id}
        ).mappings().fetchall()
        context["edu"]["data"] = qry

        qry = session.execute(
            text(
                f"""
                SELECT name, industry, role, date_in, date_out
                FROM {MYSQL_DB}.work_experience
                WHERE contact_id = :contact_id                
                AND deleted_at IS NULL
                """
            ), {"contact_id": id}
        ).mappings().fetchall()
        context["work"]["data"] = qry

        session.commit()
        session.close()
        return render(request=request, template_name="pages/contact/form/index.html", context=context)
    except Exception as e:
        session.rollback()
        session.close()
        print("\nError Message : ", str(e), "\n")
        return render(request=None, template_name="500.html", context={"nav_core": nav()})
