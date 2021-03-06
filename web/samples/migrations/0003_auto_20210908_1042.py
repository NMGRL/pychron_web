# Generated by Django 3.2.7 on 2021-09-08 16:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class IntForeignKey(models.ForeignKey):
    def db_type(self, connection):
        """ Adds support for foreign keys to big integers as primary keys.
        """
        return models.PositiveIntegerField().db_type(connection=connection)


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('samples', '0002_auto_20210906_0743'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='principalinvestigatortbl',
            options={},
        ),
        migrations.CreateModel(
            name='Userpiassociationtbl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('principal_investigatorid', IntForeignKey(db_column='principal_investigatorID',
                                                           on_delete=django.db.models.deletion.DO_NOTHING,
                                                           to='samples.principalinvestigatortbl')),
                ('user', models.ForeignKey(blank=True, db_column='userID', null=True,
                                           on_delete=django.db.models.deletion.DO_NOTHING,
                                           to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
