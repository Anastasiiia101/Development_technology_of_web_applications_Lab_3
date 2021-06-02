from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import URL, CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


class URLAdmin(admin.ModelAdmin):
    list_display = (
        'owner',
        'short_url',
    )
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'original_url',
                    'short_url',
                    'owner',
                )
            },
        ),
    )


admin.site.register(URL, URLAdmin)

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        'username',
        'email',
    )


CustomUserAdmin.fieldsets += (
    ('Other Info', {'fields': ('gender', 'birthday')}),
)

admin.site.register(CustomUser, CustomUserAdmin)
