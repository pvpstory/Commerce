from django.contrib import admin

from .models import watchlist,listings,User
# Register your models here.
admin.site.register(watchlist)

admin.site.register(listings)

admin.site.register(User)