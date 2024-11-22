from datetime import datetime

from django.shortcuts import redirect, render
from pytz import timezone
from sqlalchemy.sql import text

from configs.db import MYSQL_DB, session

from ...utils.nav import nav

# @login_required(login_url="auth:login")


def btn_delete(request, id):

    try:
        qry = session.execute(
            text(
                f"""
                SELECT COUNT(1) AS total FROM {MYSQL_DB}.contact
                WHERE contact_id = :contact_id AND deleted_at IS NULL
                """
            ), {"contact_id": id}
        ).mappings().fetchone()
        if qry["total"] < 1:
            session.commit()
            session.close()
            return render(request=None, template_name="404.html", context={"nav_menu": nav()["contact"], "msg": "ID not found"})

        session.execute(
            text(
                f"""
                UPDATE {MYSQL_DB}.contact
                SET deleted_at = :deleted_at
                WHERE contact_id = :contact_id
                """
            ), {"contact_id": id, "deleted_at": datetime.now(timezone('Asia/Jakarta'))}
        )
        session.execute(
            text(
                f"""
                UPDATE {MYSQL_DB}.education
                SET deleted_at = :deleted_at
                WHERE contact_id = :contact_id
                AND deleted_at IS NULL
                """
            ), {"contact_id": id, "deleted_at": datetime.now(timezone('Asia/Jakarta'))}
        )
        session.execute(
            text(
                f"""
                UPDATE {MYSQL_DB}.work_experience
                SET deleted_at = :deleted_at
                WHERE contact_id = :contact_id                
                AND deleted_at IS NULL
                """
            ), {"contact_id": id, "deleted_at": datetime.now(timezone('Asia/Jakarta'))}
        )
        session.commit()
        session.close()
        return redirect(to="web:contact")
    except Exception as e:
        session.rollback()
        session.close()
        print("\nError Message : ", str(e), "\n")
        return render(request=None, template_name="500.html", context={"nav_core": nav()["contact"]})
