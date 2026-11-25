import os
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "pr5"
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from apps.accounts.models import User
from apps.catalog.models import Author, Book
from apps.readers.models import Reader
from apps.loans.models import Loan

if Book.objects.exists():
    print("Демо-данные уже есть")
    sys.exit(0)

admin = User.objects.filter(username="admin").first() or User(username="admin")
admin.first_name, admin.last_name = "Ольга", "Смирнова"
admin.email, admin.phone = "admin@library.local", "+7 495 100-20-30"
admin.position = User.Position.ADMIN
admin.is_staff = admin.is_superuser = True
admin.set_password("Admin12345")
admin.save()

staff = []
for username, first, last, pos in [
    ("belova", "Ирина", "Белова", User.Position.LIBRARIAN),
    ("orlov", "Андрей", "Орлов", User.Position.LIBRARIAN),
    ("kuznetsova", "Наталья", "Кузнецова", User.Position.HEAD),
]:
    u = User(username=username, first_name=first, last_name=last, position=pos, is_staff=True)
    u.set_password("Library12345")
    u.save()
    staff.append(u)

authors = {}
for name, country in [
    ("Лев Толстой", "Россия"), ("Фёдор Достоевский", "Россия"), ("Антон Чехов", "Россия"),
    ("Михаил Булгаков", "Россия"), ("Роберт Мартин", "США"), ("Эрих Гамма", "Швейцария"),
    ("Рэй Брэдбери", "США"), ("Артур Конан Дойл", "Великобритания"),
]:
    authors[name] = Author.objects.create(name=name, country=country)

books = [
    ("Война и мир. Том 1", "Лев Толстой", 1869, "Эксмо", "fiction", 704, "Т-001", "А-1/2"),
    ("Война и мир. Том 2", "Лев Толстой", 1869, "Эксмо", "fiction", 688, "Т-002", "А-1/2"),
    ("Анна Каренина", "Лев Толстой", 1877, "АСТ", "fiction", 864, "Т-003", "А-1/2"),
    ("Преступление и наказание", "Фёдор Достоевский", 1866, "Азбука", "fiction", 608, "Д-001", "А-1/3"),
    ("Идиот", "Фёдор Достоевский", 1869, "Азбука", "fiction", 640, "Д-002", "А-1/3"),
    ("Вишнёвый сад", "Антон Чехов", 1904, "Детская литература", "fiction", 96, "Ч-001", "А-1/4"),
    ("Собачье сердце", "Михаил Булгаков", 1925, "АСТ", "fiction", 160, "Б-001", "А-1/5"),
    ("Мастер и Маргарита", "Михаил Булгаков", 1967, "АСТ", "fiction", 480, "Б-002", "А-1/5"),
    ("Чистый код", "Роберт Мартин", 2008, "Питер", "science", 464, "М-001", "Н-3/1"),
    ("Приёмы объектно-ориентированного проектирования", "Эрих Гамма", 1994, "Питер", "textbook", 368, "Г-001", "Н-3/2"),
    ("451 градус по Фаренгейту", "Рэй Брэдбери", 1953, "Эксмо", "fiction", 256, "Бр-001", "А-2/1"),
    ("Записки о Шерлоке Холмсе", "Артур Конан Дойл", 1894, "Азбука", "fiction", 320, "К-001", "А-2/2"),
]
book_objs = {}
for i, (title, author, year, pub, genre, pages, inv, shelf) in enumerate(books):
    book_objs[inv] = Book.objects.create(
        title=title, author=authors[author], year=year, publisher=pub, genre=genre,
        pages=pages, isbn=f"978-5-04-1000{i + 10}", inventory_number=inv, shelf=shelf,
    )

readers = []
for name, ticket, phone, group, lib in [
    ("Широков Михаил Андреевич", "Ч-10001", "+7 900 111-22-01", "ИСП-271", staff[0]),
    ("Петрова Дарья Сергеевна", "Ч-10002", "+7 900 111-22-02", "ИСП-271", staff[0]),
    ("Гусев Артём Олегович", "Ч-10003", "+7 900 111-22-03", "ИСП-272", staff[1]),
    ("Кузьмина Анна Викторовна", "Ч-10004", "+7 900 111-22-04", "ОИБ-231", staff[1]),
    ("Васильева Елена Игоревна", "Ч-10005", "+7 900 111-22-05", "Преподаватель", staff[0]),
]:
    readers.append(Reader.objects.create(
        full_name=name, ticket_number=ticket, phone=phone, group=group,
        librarian=lib, birth_date=date(2007, 3, 14),
    ))

l1 = Loan.objects.create(reader=readers[0], book=book_objs["Г-001"], librarian=staff[0], loan_type="home")
l1.issue()
l2 = Loan.objects.create(reader=readers[1], book=book_objs["Т-001"], librarian=staff[0], loan_type="home")
l2.issue()
l3 = Loan.objects.create(reader=readers[2], book=book_objs["Д-001"], librarian=staff[1], loan_type="hall")
l3.issue()
l3.return_book()
Loan.objects.create(reader=readers[3], book=book_objs["Б-002"], librarian=staff[1], loan_type="reserve")
l5 = Loan.objects.create(reader=readers[4], book=book_objs["Ч-001"], librarian=staff[0], loan_type="home")
l5.cancel()

print("Демо-данные загружены: вход admin / Admin12345")
