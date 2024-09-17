# Generated by Django 5.0.8 on 2024-09-17 07:01

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("classcom", "0001_initial"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="ClassGroup",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Yaratilgan vaqti"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Yangilangan vaqti"
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Sinf turi"),
                ),
                (
                    "name_uz",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Sinf turi"
                    ),
                ),
                (
                    "name_ru",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Sinf turi"
                    ),
                ),
                (
                    "name_en",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Sinf turi"
                    ),
                ),
            ],
            options={
                "verbose_name": "Sinf turi",
                "verbose_name_plural": "Sinf turlari",
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Yaratilgan vaqti"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Yangilangan vaqti"
                    ),
                ),
                (
                    "text",
                    models.CharField(max_length=255, verbose_name="Matn"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="FrontendTranslation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Yaratilgan vaqti"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Yangilangan vaqti"
                    ),
                ),
                (
                    "key",
                    models.CharField(
                        max_length=255, unique=True, verbose_name="Key"
                    ),
                ),
                ("value", models.TextField(verbose_name="Qiymati")),
                (
                    "value_uz",
                    models.TextField(null=True, verbose_name="Qiymati"),
                ),
                (
                    "value_ru",
                    models.TextField(null=True, verbose_name="Qiymati"),
                ),
                (
                    "value_en",
                    models.TextField(null=True, verbose_name="Qiymati"),
                ),
            ],
            options={
                "verbose_name": "Frontend Translation",
                "verbose_name_plural": "Frontend Translations",
            },
        ),
        migrations.CreateModel(
            name="Region",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Yaratilgan vaqti"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Yangilangan vaqti"
                    ),
                ),
                (
                    "region",
                    models.CharField(max_length=255, verbose_name="Viloyat"),
                ),
                (
                    "region_uz",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Viloyat"
                    ),
                ),
                (
                    "region_ru",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Viloyat"
                    ),
                ),
                (
                    "region_en",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Viloyat"
                    ),
                ),
            ],
            options={
                "verbose_name": "Viloyat",
                "verbose_name_plural": "Viloyatlar",
            },
        ),
        migrations.CreateModel(
            name="SchoolType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Yaratilgan vaqti"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Yangilangan vaqti"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=255, verbose_name="Maktab turi"
                    ),
                ),
                (
                    "name_uz",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Maktab turi"
                    ),
                ),
                (
                    "name_ru",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Maktab turi"
                    ),
                ),
                (
                    "name_en",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Maktab turi"
                    ),
                ),
                (
                    "institution",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("OLIY", "Oliy"),
                            ("O'rta maxsus", "O'rta maxsus"),
                            ("O'rta", "O'rta"),
                        ],
                        max_length=255,
                        null=True,
                        verbose_name="Muassasa",
                    ),
                ),
            ],
            options={
                "verbose_name": "Maktab turi",
                "verbose_name_plural": "Maktab turlari",
            },
        ),
        migrations.CreateModel(
            name="ScienceGroups",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Yaratilgan vaqti"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Yangilangan vaqti"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=255, verbose_name="Fan guruhi"
                    ),
                ),
                (
                    "name_uz",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Fan guruhi"
                    ),
                ),
                (
                    "name_ru",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Fan guruhi"
                    ),
                ),
                (
                    "name_en",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Fan guruhi"
                    ),
                ),
            ],
            options={
                "verbose_name": "Fan guruhi",
                "verbose_name_plural": "Fan guruhi",
            },
        ),
        migrations.CreateModel(
            name="SmsConfirm",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Yaratilgan vaqti"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Yangilangan vaqti"
                    ),
                ),
                ("code", models.IntegerField(verbose_name="Kod")),
                (
                    "try_count",
                    models.IntegerField(
                        default=0, verbose_name="Urinishlar soni"
                    ),
                ),
                (
                    "resend_count",
                    models.IntegerField(
                        default=0, verbose_name="Qayta yuborishlar soni"
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        max_length=255, verbose_name="Telefon raqami"
                    ),
                ),
                (
                    "expire_time",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Muddati"
                    ),
                ),
                (
                    "unlock_time",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Bloklanish vaqti"
                    ),
                ),
                (
                    "resend_unlock_time",
                    models.DateTimeField(
                        blank=True,
                        null=True,
                        verbose_name="Qayta yuborish bloklanish vaqti",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Tags",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Yaratilgan vaqti"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Yangilangan vaqti"
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Nomi"),
                ),
            ],
            options={
                "verbose_name": "Tag",
                "verbose_name_plural": "Tags",
            },
        ),
        migrations.CreateModel(
            name="BaseComment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Yaratilgan vaqti"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Yangilangan vaqti"
                    ),
                ),
                (
                    "polymorphic_ctype",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="polymorphic_%(app_label)s.%(class)s_set+",
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "comments",
                    models.ManyToManyField(
                        blank=True, to="http.comment", verbose_name="Izohlar"
                    ),
                ),
            ],
            options={
                "abstract": False,
                "base_manager_name": "objects",
            },
        ),
        migrations.CreateModel(
            name="District",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Yaratilgan vaqti"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Yangilangan vaqti"
                    ),
                ),
                (
                    "district",
                    models.CharField(max_length=255, verbose_name="Tuman"),
                ),
                (
                    "district_uz",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Tuman"
                    ),
                ),
                (
                    "district_ru",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Tuman"
                    ),
                ),
                (
                    "district_en",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Tuman"
                    ),
                ),
                (
                    "region",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="districts",
                        to="http.region",
                        verbose_name="Viloyat",
                    ),
                ),
            ],
            options={
                "verbose_name": "Tuman",
                "verbose_name_plural": "Tumanlar",
            },
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "password",
                    models.CharField(max_length=128, verbose_name="password"),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        max_length=254,
                        verbose_name="email address",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="date joined",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Yaratilgan vaqti"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Yangilangan vaqti"
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        max_length=255, unique=True, verbose_name="Telefon"
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Foydalanuvchi nomi",
                    ),
                ),
                (
                    "avatar",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="avatar/",
                        verbose_name="Avatar",
                    ),
                ),
                (
                    "validated_at",
                    models.DateTimeField(
                        blank=True,
                        null=True,
                        verbose_name="Tasdiqlangan vaqti",
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("admin", "Administrator"),
                            ("moderator", "Moderator"),
                            ("user", "Foydalanuvchi"),
                        ],
                        default="user",
                        max_length=255,
                        null=True,
                        verbose_name="Rol",
                    ),
                ),
                (
                    "institution",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("OLIY", "Oliy"),
                            ("O'rta maxsus", "O'rta maxsus"),
                            ("O'rta", "O'rta"),
                        ],
                        max_length=255,
                        null=True,
                        verbose_name="Muassasa",
                    ),
                ),
                (
                    "institution_number",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Muassasa raqami",
                    ),
                ),
                (
                    "classes",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="classcom.classes",
                        verbose_name="Sinflar",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "science",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="classcom.science",
                        verbose_name="Fan",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
                (
                    "class_group",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="http.classgroup",
                        verbose_name="Sinf turi",
                    ),
                ),
                (
                    "district",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="http.district",
                        verbose_name="Tuman",
                    ),
                ),
                (
                    "region",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="http.region",
                        verbose_name="Viloyat",
                    ),
                ),
                (
                    "school_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="http.schooltype",
                        verbose_name="Maktab turi",
                    ),
                ),
                (
                    "science_group",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="http.sciencegroups",
                        verbose_name="Fan guruhi",
                    ),
                ),
            ],
            options={
                "verbose_name": "Foydalanuvchilar",
                "verbose_name_plural": "Foydalanuvchilar",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "basecomment_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="http.basecomment",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=255, verbose_name="Sarlavha"),
                ),
                (
                    "title_uz",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Sarlavha"
                    ),
                ),
                (
                    "title_ru",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Sarlavha"
                    ),
                ),
                (
                    "title_en",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Sarlavha"
                    ),
                ),
                ("desc", models.TextField(verbose_name="Tavsif")),
                (
                    "desc_uz",
                    models.TextField(null=True, verbose_name="Tavsif"),
                ),
                (
                    "desc_ru",
                    models.TextField(null=True, verbose_name="Tavsif"),
                ),
                (
                    "desc_en",
                    models.TextField(null=True, verbose_name="Tavsif"),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="posts/",
                        verbose_name="Rasm",
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(
                        blank=True, to="http.tags", verbose_name="Teglar"
                    ),
                ),
            ],
            options={
                "abstract": False,
                "base_manager_name": "objects",
            },
            bases=("http.basecomment",),
        ),
    ]
