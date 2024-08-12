from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class Types(TextChoices):
    BYLIST = "BYLIST", _("By list")
    BYCLASS = "BYCLASS", _("By class")
    BYCLASSANDUNIT = "BYCLASSANDUNIT", _("By class and unit")
    BYDEPARTMENT = "BYDEPARTMENT", _("By Department")
    BYDOCS = "BYDOCS", _("By docs")
    BYSCHOOL = "BYSCHOOL", _("By school")


class Departments(TextChoices):
    BOOK = "BOOK", _("Darslik")
    TEACHERBOOK = "TEACHERBOOK", _("O‘qituvchi kitobi")
    NOTEBOOK = "NOTEBOOK", _("Daftar")


class Schools(TextChoices):
    PRIMARY = "PRIMARY", _("Boshlang‘ich maktab.")
    SECONDARY = "SECONDARY", _("O‘rta maktab")
    TERTIARY = "TERTIARY", _("Katta maktab")


class Docs(TextChoices):
    DOCS = "DOCS", _("Hujjatlar, testlar ")
    MULTIMEDIA = "MULTIMEDIA", _("O‘qituvchining o‘z-o‘zini tarbiyalashi uchun multimedia resurslari")