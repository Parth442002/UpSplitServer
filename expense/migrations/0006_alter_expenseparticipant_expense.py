# Generated by Django 3.2.6 on 2023-06-04 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0005_auto_20230605_0107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenseparticipant',
            name='expense',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='expense.expense'),
        ),
    ]