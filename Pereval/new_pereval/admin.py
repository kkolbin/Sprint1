from django.contrib import admin
from .models import Users, Coords, Levels, Pass, PassImages

admin.site.register(Users)
admin.site.register(Coords)
admin.site.register(Levels)
admin.site.register(Pass)
admin.site.register(PassImages)
