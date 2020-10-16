from django.contrib import admin
from users.models import UserProfile
# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'phone_number']
    list_display = ('get_name', 'phone_number', )

    def get_name(self, obj):
        return obj.user.username
    get_name.admin_order_field  = 'user'  #Allows column order sorting
    get_name.short_description = 'Username'  #Renames column head