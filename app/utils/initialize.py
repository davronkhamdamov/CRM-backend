import hashlib

import requests

from app.api.models import Services, Staffs, Users, Payment_type
from app.db import db1

url = "https://randomuser.me/api?results=50"

users = requests.get(url).json()["results"]

for user in users:
    _user = Users(
        name=user["name"]["first"],
        surname=user["name"]["last"],
        date_birth=user["dob"]["date"],
        address=user["location"]["street"]["name"],
        phone_number=user["phone"],
        gender=user["gender"],
        job="Ishsiz",
        img_url=user["picture"]["large"],
    )
    db1.add(_user)


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
_staff_r = Staffs(
    name="reception",
    surname="reception",
    address="Uzb",
    login="reception",
    password=hashlib.sha256("reception".encode()).hexdigest(),
    phone_number="+99898765432",
    gender="male",
    role="reception",
)

db1.add(_staff)
db1.add(_staff_r)


for method in ["Naqt", "Karta"]:
    _payment_type = Payment_type(method=method)
    db1.add(_payment_type)

for method in [
    {
        "name": "Olib tashlash",
        "price": 30000,
        "raw_material_price": 0,
        "service_price_price": 30000,
    },
    {
        "name": "Plomba",
        "price": 20000,
        "raw_material_price": 30000,
        "service_price_price": 50000,
    },
]:
    _service = Services(
        name=method["name"],
        price=method["price"],
        raw_material_price=method["raw_material_price"],
        service_price_price=method["service_price_price"],
    )
    db1.add(_service)

for staff in users[10:]:
    _staff = Staffs(
        name=staff["name"]["first"],
        surname=staff["name"]["last"],
        address=staff["location"]["street"]["name"],
        login=staff["login"]["username"],
        password=hashlib.sha256(staff["login"]["password"].encode()).hexdigest(),
        phone_number=staff["phone"],
        gender=staff["gender"],
        role="doctor",
    )
    db1.add(_staff)
db1.commit()
