from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Создание пользователя в Админке."""
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
    )
    list_editable = ('email', 'first_name', 'last_name',)
    search_fields = ('username', 'email',)
    list_filter = ('username', 'email',)
    empty_value_display = '-пусто-'
