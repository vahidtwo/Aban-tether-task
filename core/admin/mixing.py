from django.db import models
from django.utils.translation import gettext_lazy as _

from core.admin.utils import link_image


class ThumbnailAdminMixing:
    """
    add a field named icon to list display of admin class
    """

    thumbnail_field_name = ...

    def thumb(self, obj):
        if self.thumbnail_field_name and self.thumbnail_field_name is not ...:
            pass
        elif hasattr(obj, "thumbnail"):
            self.thumbnail_field_name = "thumbnail"
        elif hasattr(obj, "logo"):
            self.thumbnail_field_name = "logo"
        else:
            for field in self.model._meta.fields:
                if isinstance(field, models.fields.files.ImageField):
                    self.thumbnail_field_name = field.name
                    break
            if self.thumbnail_field_name is ...:
                raise ValueError("not set the thumbnail_field_name on django admin")
        img = getattr(obj, self.thumbnail_field_name)
        return link_image(img) if img else None

    thumb.short_description = _("icon")

    def get_list_display(self, request):
        return self.list_display + ("thumb",)


class SlugAdminMixing:
    def get_fieldsets(self, request, obj=None):
        if obj is None:
            self.exclude = ("slug",) + self.exclude
        return super().get_fieldsets(request, obj)
