from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_admin(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    if not User.objects.filter(username="admin").exists():
        User.objects.create(
            username="admin",
            email="admin@example.com",
            password=make_password("AdminPass123"),
            is_superuser=True,
            is_staff=True,
        )

class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),  # depends on your Django version
    ]

    operations = [
        migrations.RunPython(create_admin),
    ]