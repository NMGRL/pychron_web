from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Principalinvestigatortbl(models.Model):
    name = models.CharField(max_length=140, blank=True, null=True)
    email = models.CharField(max_length=140, blank=True, null=True)
    affiliation = models.CharField(max_length=140, blank=True, null=True)
    oid = models.IntegerField(blank=True, null=True)
    last_name = models.CharField(max_length=140, blank=True, null=True)
    first_initial = models.CharField(max_length=10, blank=True, null=True)

    @property
    def full_name(self):
        return f'{self.last_name}, {self.first_initial}' if self.first_initial else self.last_name

    def get_absolute_url(self):
        return '/principal_investigators/{}/'.format(self.id)

    class Meta:
        db_table = 'PrincipalInvestigatorTbl'


class Projecttbl(models.Model):
    name = models.CharField(max_length=80, blank=True, null=True)
    principal_investigatorid = models.ForeignKey(Principalinvestigatortbl, models.DO_NOTHING,
                                                 db_column='principal_investigatorID')  # Field name made lowercase.
    checkin_date = models.DateField(blank=True, null=True)
    lab_contact = models.CharField(max_length=80, blank=True, null=True)
    institution = models.CharField(max_length=80, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    # userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userID')
    @property
    def piname(self):
        return f'{self.name}({self.principal_investigatorid.full_name})'

    def get_absolute_url(self):
        return '/projects/{}/'.format(self.id)

    class Meta:
        managed = False
        db_table = 'ProjectTbl'


class Materialtbl(models.Model):
    name = models.CharField(max_length=80, blank=True, null=True)
    grainsize = models.CharField(max_length=80, blank=True, null=True)

    def get_absolute_url(self):
        return f'/materials/{self.id}/'

    @property
    def full_name(self):
        grainsize = f'({self.grainsize})' if self.grainsize else ''
        return f'{self.name}{grainsize}'

    class Meta:
        managed = False
        db_table = 'MaterialTbl'


class Sampletbl(models.Model):
    name = models.CharField(max_length=80, blank=True, null=True)
    materialid = models.ForeignKey(Materialtbl, models.DO_NOTHING, db_column='materialID', blank=True,
                                   null=True)  # Field name made lowercase.
    projectid = models.ForeignKey(Projecttbl, models.DO_NOTHING, db_column='projectID', blank=True,
                                  null=True)  # Field name made lowercase.
    note = models.CharField(max_length=140, blank=True, null=True)
    igsn = models.CharField(max_length=140, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    storage_location = models.CharField(max_length=140, blank=True, null=True)
    lithology = models.CharField(max_length=140, blank=True, null=True)
    location = models.CharField(max_length=140, blank=True, null=True)
    approximate_age = models.FloatField(blank=True, null=True)
    elevation = models.FloatField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)
    lithology_class = models.CharField(max_length=140, blank=True, null=True)
    lithology_group = models.CharField(max_length=140, blank=True, null=True)
    lithology_type = models.CharField(max_length=140, blank=True, null=True)
    unit = models.CharField(max_length=80, blank=True, null=True)

    def get_absolute_url(self):
        return f"/samples/{self.id}/"

    class Meta:
        db_table = 'SampleTbl'


class Samplesubmittbl(models.Model):
    sample = models.ForeignKey(Sampletbl, models.DO_NOTHING, db_column='sampleID', blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, db_column='userID', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'SampleSubmitTbl'


# class IntForeignKey(models.ForeignKey):
#     def db_type(self, connection):
#         """ Adds support for foreign keys to big integers as primary keys.
#         """
#         rel_field = self.rel.get_related_field()
#         if (isinstance(rel_field, models.AutoField) or
#                 (not connection.features.related_fields_match_type and
#                  isinstance(rel_field, (models.IntegerField,)))):
#             return models.IntegerField().db_type(connection=connection)
#         return super(IntForeignKey, self).db_type(connection)
#


class Userpiassociationtbl(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, db_column='userID', blank=True, null=True)
    principal_investigatorid = models.ForeignKey(Principalinvestigatortbl, models.DO_NOTHING,
                                                 db_column='principal_investigatorID')