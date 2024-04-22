from django.contrib import admin

from .models import watchlist,listings,User
# Register your models here.
from .models import comments,bids
admin.site.register(watchlist)

admin.site.register(listings)

admin.site.register(User)
admin.site.register(comments)
admin.site.register(bids)