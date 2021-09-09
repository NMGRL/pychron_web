from django.db import models

from samples.models import Sampletbl

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


class Irradiationtbl(models.Model):
    name = models.CharField(max_length=80, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'IrradiationTbl'


class Leveltbl(models.Model):
    name = models.CharField(max_length=80, blank=True, null=True)
    irradiationid = models.ForeignKey(Irradiationtbl, models.DO_NOTHING, db_column='irradiationID', blank=True,
                                      null=True)  # Field name made lowercase.
    # productionid = models.ForeignKey('Productiontbl', models.DO_NOTHING, db_column='productionID', blank=True, null=True)  # Field name made lowercase.
    holder = models.CharField(max_length=45, blank=True, null=True)
    z = models.FloatField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'LevelTbl'


class Irradiationpositiontbl(models.Model):
    identifier = models.CharField(unique=True, max_length=80, blank=True, null=True)
    sampleid = models.ForeignKey(Sampletbl, models.DO_NOTHING, db_column='sampleID', blank=True,
                                 null=True)  # Field name made lowercase.
    levelid = models.ForeignKey(Leveltbl, models.DO_NOTHING, db_column='levelID', blank=True,
                                null=True)  # Field name made lowercase.
    position = models.IntegerField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    j = models.FloatField(blank=True, null=True)
    j_err = models.FloatField(blank=True, null=True)
    packet = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'IrradiationPositionTbl'


class Analysistbl(models.Model):
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
