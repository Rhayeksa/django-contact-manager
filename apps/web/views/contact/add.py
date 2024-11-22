import uuid
from datetime import datetime

from django.shortcuts import render, redirect
from pytz import timezone
from sqlalchemy.sql import text

from configs.db import MYSQL_DB, session
from configs.imgbb import IMGBB_API_URL, IMGBB_KEY

from ..utils.nav import nav
from ..utils.upload_img import upload_img

# @login_required(login_url="auth:login")


def add(request):

    context = {
        "page": "add",
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
            "data": {"photo_url": ""}
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
        if request.method == "POST":
            contact_id = str(uuid.uuid4())[:8]
            session.execute(
                text(
                    f"""
                    INSERT INTO {MYSQL_DB}.contact(contact_id, name, age, gender, phone, email, portfolio, photo, address, created_at, updated_at)
                    VALUES(:contact_id, :name, :age, :gender, :phone, :email, :portfolio, :photo, :address, :created_at, :updated_at)
                    """
                ),
                {
                    "contact_id": contact_id,
                    "name": str(request.POST["name"]).strip(),
                    "age": request.POST["age"],
                    "gender": 1 if dict(request.POST).get("gender") == ['1'] else 0,
                    "phone": str(request.POST["phone"]).strip(),
                    "email": str(request.POST["email"]).strip(),
                    "portfolio": str(request.POST["portfolio"]).strip(),
                    "photo": None if dict(request.FILES).get("photo") == None else upload_img(img=request.FILES['photo'], url=IMGBB_API_URL, key=IMGBB_KEY),
                    "address": str(request.POST["address"]).strip(),
                    "created_at": datetime.now(timezone('Asia/Jakarta')),
                    "updated_at": datetime.now(timezone('Asia/Jakarta')),
                }
            )
            session.commit()
            session.close()
            return redirect(to="web:contact_edit", id=contact_id)

        return render(request=request, template_name="pages/contact/form/index.html", context=context)
    except Exception as e:
        session.rollback()
        session.close()
        print("\nError Message : ", str(e), "\n")
        return render(request=None, template_name="500.html", context={"nav_core": nav()["contact"]})
