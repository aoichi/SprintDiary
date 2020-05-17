# Generated by Django 2.1.15 on 2020-05-16 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0003_auto_20200517_0002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diary',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='diary.Category', verbose_name='Category'),
        ),
    ]