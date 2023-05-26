from django.contrib import admin
from .models import Customer, Address
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

admin.site.register(Address)
admin.site.unregister(Group)


@admin.register(Customer)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["get_full_name", "username", "persian_created_at", "persian_edited_at", "persian_deleted_at"]


admin.site.register(Group)
admin_group = Group.objects.create(name='ادمین')
observer_group = Group.objects.create(name='ناظر')

content_type = ContentType.objects.get_for_model(Customer)

permission = Permission.objects.create(
    codename='can_change_customer',
    name='Can change customer',
    content_type=content_type,
)

admin_group.permissions.add(permission)
admin_group.permissions.add(Permission.objects.get(codename='add_customer'))
admin_group.permissions.add(Permission.objects.get(codename='delete_customer'))
