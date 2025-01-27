from django.db import models
from django.utils.translation import gettext_lazy as _

from core.http.models import AbstractBaseModel


class ElectronResourceCategory(AbstractBaseModel):
    """
    Model for storing electron resources.
    """

    class Meta:
        verbose_name = _("Electron Resource")
        verbose_name_plural = _("Electron Resources")

    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True, null=True)
    is_active = models.BooleanField(_("Is Active"), default=True)

    def __str__(self):
        return self.name


class ElectronResourceSubCategory(AbstractBaseModel):
    """
    Model for storing electron resources.
    """

    class Meta:
        verbose_name = _("Electron Resource Sub Category")
        verbose_name_plural = _("Electron Resource Sub Categories")

    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True, null=True)
    category = models.ForeignKey(
        ElectronResourceCategory,
        on_delete=models.CASCADE,
        related_name="sub_categories",
    )
    is_active = models.BooleanField(_("Is Active"), default=True)

    def __str__(self):
        return self.name


class ElectronResource(AbstractBaseModel):
    """
    Model for storing electron resources.
    """

    class Meta:
        verbose_name = _("Electron Resource File")
        verbose_name_plural = _("Electron Resource Files")
        ordering = ["-created_at"]
        db_table = "electron_resource_files"

    user = models.ForeignKey(
        "http.User",
        on_delete=models.CASCADE,
        related_name="files",
        db_index=True,
        blank=True,
        null=True,
    )
    description = models.TextField(_("Description"), blank=True, null=True)
    file = models.FileField(_("File"), upload_to="electron_resources/")
    name = models.CharField(_("Name"), max_length=255)
    size = models.CharField(_("Size"), max_length=255, blank=True, null=True)
    type = models.CharField(_("Type"), max_length=255, blank=True, null=True)
    category = models.ForeignKey(
        ElectronResourceSubCategory,
        on_delete=models.CASCADE,
        related_name="resources",
    )
    is_active = models.BooleanField(_("Is Active"), default=True)

    def __str__(self):
        return str(self.name)

    def get_file_size(self, size=None):
        if size < 1024:
            return f"{size} bytes"
        elif size < 1024 * 1024:
            return f"{round(size / 1024, 2)} KB"
        elif size < 1024 * 1024 * 1024:
            return f"{round(size / (1024 * 1024), 2)} MB"
        else:
            return f"{round(size / (1024 * 1024 * 1024), 2)} GB"

    def get_file_name(self, file=None):
        if file:
            return file.split("/")[-1]

    def save(self, *args, **kwargs):
        self.size = self.get_file_size(self.file.size)
        self.type = self.file.name.split(".")[-1]
        self.name = self.get_file_name(self.file.name)
        super().save(*args, **kwargs)
