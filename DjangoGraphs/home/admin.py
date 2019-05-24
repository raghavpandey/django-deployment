from django.contrib import admin
from .models import SocTable, LogTable, Reviews, SocMaster


admin.site.register(SocTable)
admin.site.register(LogTable)
admin.site.register(Reviews)
admin.site.register(SocMaster)


