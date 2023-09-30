from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    exclude = ("is_active",)

    def get_fieldsets(self, request, obj=None):
        if obj is None and hasattr(self, "add_fieldsets"):
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)


class BaseTabularInline(admin.TabularInline):
    exclude = ("is_active",)


class BaseStackInline(admin.StackedInline):
    exclude = ("is_active",)
