from django.db import models


# Create your models here.
from samples.models import Sampletbl


class Principalinvestigatortbl(models.Model):
    name = models.CharField(max_length=140, blank=True, null=True)
    email = models.CharField(max_length=140, blank=True, null=True)
    affiliation = models.CharField(max_length=140, blank=True, null=True)
    oid = models.IntegerField(blank=True, null=True)
    last_name = models.CharField(max_length=140, blank=True, null=True)
    first_initial = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'PrincipalInvestigatorTbl'


class Projecttbl(models.Model):
    name = models.CharField(max_length=80, blank=True, null=True)
    principal_investigatorid = models.ForeignKey(Principalinvestigatortbl, models.DO_NOTHING,
                                                 db_column='principal_investigatorID')  # Field name made lowercase.
    checkin_date = models.DateField(blank=True, null=True)
    lab_contact = models.CharField(max_length=80, blank=True, null=True)
    institution = models.CharField(max_length=80, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        return '/projects/{}/'.format(self.id)

    class Meta:
        managed = False
        db_table = 'ProjectTbl'
