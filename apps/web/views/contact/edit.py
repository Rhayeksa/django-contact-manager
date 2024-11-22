from datetime import datetime

from django.shortcuts import redirect, render
from pytz import timezone
from sqlalchemy.sql import text

from configs.db import MYSQL_DB, session
from configs.imgbb import IMGBB_API_URL, IMGBB_KEY

from ..utils.nav import nav
from ..utils.upload_img import upload_img
import json

# @login_required(login_url="auth:login")


def edit(request, id):

    context = {
        "page": "edit",
        "nav_menu": nav()["contact"],
        "bio": {
            "field": {
                "name": {"label": "Name", "value": ""},
                "age": {"label": "Age", "value": 0},
                "phone": {"label": "Phone", "value": "", "msg_err": []},
                "email": {"label": "Email", "value": "", "msg_err": []},
                "gender": {"label": "Gender", "value": "", "opt": (("", "---------"), ("1", "Pria"), ("0", "Wanita"))},
                "portfolio": {"label": "Portfolio", "value": "", "msg_err": []},
                "photo": {"label": "Photo"},
                "address": {"label": "Address", "value": ""},
            },
            "data": {"photo_url": "", "contact_id": id}
        },
        "edu": {
            "field": {
                "name": {"label": "Name", "value": ""},
                "major": {"label": "Major", "value": ""},
                "category": {"label": "Category", "opt": (("", "---------"), ("High School", "High School"), ("University", "University"), ("Course", "Course"))},
                "date_in": {"label": "Date in", "value": ""},
                "date_out": {"label": "Date out", "value": ""},
            },
            "data": [],
        },
        "work": {
            "field": {
                "name": {"label": "Name", "value": ""},
                "industry": {"label": "Industry", "value": ""},
                "role": {"label": "Role", "value": ""},
                "date_in": {"label": "Date_in", "value": ""},
                "date_out": {"label": "Date_out", "value": ""},
            },
            "data": [],
        },
    }

    try:
        if request.method == "POST":
            if "add_edu" in request.POST:
                session.execute(
                    text(
                        f"""
                        INSERT INTO {MYSQL_DB}.education(name, category, major, date_in, date_out, created_at, updated_at, contact_id)
                        VALUES(:name, :category, :major, :date_in, :date_out, :created_at, :updated_at, :contact_id)
                        """
                    ), {
                        "name": str(request.POST["edu_nm"]).strip(),
                        "category": str(request.POST["category"]).strip(),
                        "major": str(request.POST["major"]).strip(),
                        "date_in": str(request.POST["date_in"]).strip(),
                        "date_out": str(request.POST["date_out"]).strip(),
                        "created_at": datetime.now(timezone('Asia/Jakarta')),
                        "updated_at": datetime.now(timezone('Asia/Jakarta')),
                        "contact_id": id,
                    }
                )
                session.commit()
                session.close()
                return redirect(to="web:contact_edit", id=id)
            if "add_work" in request.POST:
                session.execute(
                    text(
                        f"""
                        INSERT INTO {MYSQL_DB}.work_experience(name, industry, role, date_in, date_out, created_at, updated_at, contact_id)
                        VALUES(:name, :industry, :role, :date_in, :date_out, :created_at, :updated_at, :contact_id)
                        """
                    ), {
                        "name": str(request.POST["work_nm"]).strip(),
                        "industry": str(request.POST["industry"]).strip(),
                        "role": str(request.POST["role"]).strip(),
                        "date_in": str(request.POST["date_in"]).strip(),
                        "date_out": str(request.POST["date_out"]).strip(),
                        "created_at": datetime.now(timezone('Asia/Jakarta')),
                        "updated_at": datetime.now(timezone('Asia/Jakarta')),
                        "contact_id": id,
                    }
                )
                session.commit()
                session.close()
                return redirect(to="web:contact_edit", id=id)
            if "save_bio" in request.POST:
                session.execute(
                    text(
                        f"""
                        UPDATE {MYSQL_DB}.contact
                        SET name = :name
                            , age = :age
                            , gender = :gender
                            , phone = :phone
                            , email = :email
                            , portfolio = :portfolio
                            , photo = :photo
                            , address = :address
                            , updated_at = :updated_at
                        WHERE contact_id = :contact_id
                        """
                    ), {
                        "contact_id": id,
                        "name": None if request.POST["name"] == "" else str(request.POST["name"]).strip(),
                        "age": request.POST["age"],
                        "gender": 1 if dict(request.POST).get("gender") == ['1'] else 0,
                        "phone": str(request.POST["phone"]).strip(),
                        "email": None if request.POST["email"] == "" else str(request.POST["email"]).strip(),
                        "portfolio": None if request.POST["portfolio"] == "" else str(request.POST["portfolio"]).strip(),
                        "photo": None if dict(request.FILES).get("photo") == None else upload_img(img=request.FILES['photo'], url=IMGBB_API_URL, key=IMGBB_KEY),
                        "address": str(request.POST["address"]).strip(),
                        "updated_at": datetime.now(timezone('Asia/Jakarta')),
                    }
                )
                session.commit()
                session.close()
                return redirect(to="web:contact_edit", id=id)

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
        context["bio"]["field"]["name"]["value"] = "" if qry["name"] == None else qry["name"]
        context["bio"]["field"]["age"]["value"] = "" if qry["age"] == None else qry["age"]
        context["bio"]["field"]["gender"]["value"] = "" if qry["gender"] == None else qry["gender"]
        context["bio"]["field"]["phone"]["value"] = "" if qry["phone"] == None else qry["phone"]
        context["bio"]["field"]["email"]["value"] = "" if qry["email"] == None else qry["email"]
        context["bio"]["field"]["portfolio"]["value"] = "" if qry["portfolio"] == None else qry["portfolio"]
        context["bio"]["field"]["address"]["value"] = "" if qry["address"] == None else qry["address"]

        if qry["photo"] != None:
            photo = json.loads(qry["photo"])
            photo = photo["data"]["url"]
        context["bio"]["data"]["photo_url"] = "" if qry["photo"] == None else photo

        qry = session.execute(
            text(
                f"""
                SELECT education_id, name, major, category, date_in, date_out
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
                SELECT work_experience_id, name, industry, role, date_in, date_out
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
