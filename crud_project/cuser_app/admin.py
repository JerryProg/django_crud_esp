from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from crud_project.forms import UserCreationForm, UserChangeForm
from cuser_app.models import CustomUser


# Register your models here
class MyUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('id', 'email', 'date_joined', 'last_login','is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        #('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_admin','is_active',)}),
    )

    add_fieldsets = (
        (None,{
            'classes': ('wide',),
            'fields':('email',  'password1', 'password2'),
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(CustomUser, MyUserAdmin)
admin.site.unregister(Group)