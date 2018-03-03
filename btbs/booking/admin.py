from django.contrib import admin

# Register your models here.
from .models import User,UserFeedback,Wallet,WalletTransaction,Bus,Booking

admin.site.register(User)
admin.site.register(UserFeedback)
admin.site.register(Wallet)
admin.site.register(WalletTransaction)
admin.site.register(Bus)
admin.site.register(Booking)
