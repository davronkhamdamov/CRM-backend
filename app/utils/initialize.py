import hashlib

from app.api.models import Staffs
from app.db import db1

admin = db1.query(Staffs).filter(Staffs.login == "admin")
if not admin:
    _staff = Staffs(
        name="admin",
        surname="admin",
        address="Uzb",
        login="admin",
        password=hashlib.sha256("admin".encode()).hexdigest(),
        phone_number="+99898765432",
        gender="male",
        role="admin",
    )

    db1.add(_staff)
    db1.commit()
