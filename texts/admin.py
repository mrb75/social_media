from django.contrib import admin
from .models import Text
# Register your models here.


class TextAdmin(admin.ModelAdmin):
    pass


admin.site.register(Text, TextAdmin)
