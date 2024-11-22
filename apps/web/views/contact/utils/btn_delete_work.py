from datetime import datetime

from django.shortcuts import redirect, render
from pytz import timezone
from sqlalchemy.sql import text

from configs.db import MYSQL_DB, session

from ...utils.nav import nav

# @login_required(login_url="auth:login")


def btn_delete_work(request, contact_id, id):

    try:
        qry = session.execute(
            text(
                f"""
                SELECT COUNT(1) AS total FROM {MYSQL_DB}.contact
                WHERE contact_id = :contact_id AND deleted_at IS NULL
                """
            ), {"contact_id": contact_id}
        ).mappings().fetchone()
        if qry["total"] < 1:
            session.commit()
            session.close()
            return render(request=None, template_name="404.html", context={"nav_menu": nav()["contact"], "msg": "Contact ID not found"})
        qry = session.execute(
            text(
                f"""
                SELECT COUNT(1) AS total FROM {MYSQL_DB}.work_experience
                WHERE work_experience_id = :work_experience_id AND deleted_at IS NULL
                """
            ), {"work_experience_id": id}
        ).mappings().fetchone()
        if qry["total"] < 1:
            session.commit()
            session.close()
            return render(request=None, template_name="404.html", context={"nav_menu": nav()["contact"], "msg": "work_experience ID not found"})

        session.execute(
            text(
                f"""
                UPDATE {MYSQL_DB}.work_experience SET deleted_at = :deleted_at
                WHERE work_experience_id = :work_experience_id AND deleted_at IS NULL
                """
            ), {"work_experience_id": id, "deleted_at": datetime.now(timezone('Asia/Jakarta'))}
        )
        session.commit()
        session.close()
        return redirect(to="web:contact_edit", id=contact_id)
    except Exception as e:
        session.rollback()
        session.close()
        print("\nError Message : ", str(e), "\n")
        return render(request=None, template_name="500.html", context={"nav_core": nav()["contact"]})
