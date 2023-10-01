import uuid
import jdatetime
from django.db import models
from django.forms.utils import to_current_timezone
from django.utils.translation import gettext_lazy as _


def datetime2jalali(g_date):
    if g_date is None:
        return None

    g_date = to_current_timezone(g_date)
    jdatetime.set_locale("fa_IR")
    return jdatetime.datetime.fromgregorian(datetime=g_date)


class BaseModel(models.Model):
    """
    Base Model
    methods:
        - jalali_created_at: returns jalali format of created_at attr
    """

    class Meta:
        abstract = True

    def __str__(self):
        if hasattr(self, "title"):
            return str(self.title)

        if hasattr(self, "name"):
            return str(self.name)

        return "%s (%s)" % (self._meta.verbose_name, self.id)


class TimeStampedBaseModel(BaseModel):
    """
    Base Model
    methods:
        - jalali_created_at: returns jalali format of created_at attr
    """

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        abstract = True

    def jalali_created_at(self):
        """
        returns jalali format of created_at attr
        """
        return datetime2jalali(self.created_at)

    jalali_created_at.short_description = _("created_at")

    jalali_created_at = property(jalali_created_at)

    @property
    def formatted_jalali_date(self):
        return self.jalali_created_at.strftime("%d %b %Y")
