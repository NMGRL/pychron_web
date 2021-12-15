from django.db import models


from irradiations.models import Irradiationpositiontbl

BASE = 26
A_UPPERCASE = ord('A')


def alphas(n):
    a = ''
    if n is not None:
        def decompose(n):
            while n >= 0:
                nn, rem = divmod(n, BASE)
                n = nn - 1
                yield rem

        digits = reversed([chr(A_UPPERCASE + part) for part in decompose(n)])
        a = ''.join(digits)

    return a


class AnalysisTbl(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    uuid = models.CharField(max_length=40, blank=True, null=True)
    analysis_type = models.CharField(max_length=45, blank=True, null=True)
    aliquot = models.IntegerField(blank=True, null=True)
    increment = models.IntegerField(blank=True, null=True)
    irradiation_positionid = models.ForeignKey(Irradiationpositiontbl, models.DO_NOTHING,
                                               db_column='irradiation_positionID', blank=True,
                                               null=True)  # Field name made lowercase.
    measurementname = models.CharField(db_column='measurementName', max_length=45, blank=True,
                                       null=True)  # Field name made lowercase.
    extractionname = models.CharField(db_column='extractionName', max_length=45, blank=True,
                                      null=True)  # Field name made lowercase.
    posteqname = models.CharField(db_column='postEqName', max_length=45, blank=True,
                                  null=True)  # Field name made lowercase.
    postmeasname = models.CharField(db_column='postMeasName', max_length=45, blank=True,
                                    null=True)  # Field name made lowercase.
    mass_spectrometer = models.CharField(max_length=45, blank=True, null=True)
    # mass_spectrometer = models.ForeignKey('Massspectrometertbl', models.DO_NOTHING, db_column='mass_spectrometer',
    #                                       blank=True, null=True)
    # extract_device = models.ForeignKey('Extractdevicetbl', models.DO_NOTHING, db_column='extract_device', blank=True,
    #                                    null=True)
    extract_value = models.FloatField(blank=True, null=True)
    extract_units = models.CharField(max_length=45, blank=True, null=True)
    cleanup = models.FloatField(blank=True, null=True)
    duration = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    comment = models.CharField(max_length=200, blank=True, null=True)
    # simple_identifier = models.ForeignKey('Simpleidentifiertbl', models.DO_NOTHING, db_column='simple_identifier',
    #                                       blank=True, null=True)
    experiment_type = models.CharField(max_length=32, blank=True, null=True)
    pre_cleanup = models.FloatField(blank=True, null=True)
    post_cleanup = models.FloatField(blank=True, null=True)

    @property
    def dtimestamp(self):
        return self.timestamp.strftime('%m/%d/%Y %H:%M:%S')

    @property
    def runid(self):
        i = self.increment
        i = alphas(i) if i is not None else ''
        return f'{self.irradiation_positionid.identifier}-{self.aliquot:02n}{i}'

    class Meta:
        managed = False
        db_table = 'AnalysisTbl'


# Create your models here.
class RepositoryAssociationTbl(models.Model):
    idrepositoryassociationTbl = models.IntegerField(primary_key=True)
    repository = models.CharField(max_length=140)
    analysisID = models.ForeignKey(AnalysisTbl,
                                   models.DO_NOTHING, related_name="repository",
                                   db_column='analysisID',)
    class Meta:
        managed = False
        db_table = 'RepositoryAssociationTbl'