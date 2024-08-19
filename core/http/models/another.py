from django.db import models
from django.utils.translation import gettext as _
from polymorphic import models as polymorphic

from core.http.models.base import AbstractBaseModel


class Tags(AbstractBaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Nomi"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class Comment(AbstractBaseModel):
    text = models.CharField(max_length=255, verbose_name=_("Matn"))

    def __str__(self) -> str:
        return self.text


class BaseComment(polymorphic.PolymorphicModel, AbstractBaseModel):
    comments = models.ManyToManyField(
        Comment, blank=True, verbose_name=_("Izohlar")
    )


class Post(BaseComment):
    title = models.CharField(max_length=255, verbose_name=_("Sarlavha"))
    desc = models.TextField(verbose_name=_("Tavsif"))
    image = models.ImageField(
        upload_to="posts/", blank=True, null=True, verbose_name=_("Rasm")
    )
    tags = models.ManyToManyField(Tags, blank=True, verbose_name=_("Teglar"))

    def __str__(self):
        return self.title


class FrontendTranslation(AbstractBaseModel):
    key = models.CharField(max_length=255, unique=True, verbose_name=_("Key"))
    value = models.TextField(verbose_name=_("Qiymati"))

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = _("Frontend Translation")
        verbose_name_plural = _("Frontend Translations")
