from django.db import models


# Create your models here.
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

    class Meta:
        managed = False
        db_table = 'ProjectTbl'


class Materialtbl(models.Model):
    name = models.CharField(max_length=80, blank=True, null=True)
    grainsize = models.CharField(max_length=80, blank=True, null=True)

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
        managed = False
        db_table = 'SampleTbl'
