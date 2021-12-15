from django.db import models

from samples.models import SampleTbl

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
    sampleid = models.ForeignKey(SampleTbl, models.DO_NOTHING, db_column='sampleID', blank=True,
                                 null=True)  # Field name made lowercase.
    levelid = models.ForeignKey(Leveltbl, models.DO_NOTHING, db_column='levelID', blank=True,
                                null=True)  # Field name made lowercase.
    position = models.IntegerField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    j = models.FloatField(blank=True, null=True)
    j_err = models.FloatField(blank=True, null=True)
    packet = models.CharField(max_length=80, blank=True, null=True)

    def to_info(self):
        irrad = self.levelid.irradiationid.name
        level = self.levelid.name
        pos = self.position
        id = self.identifier
        id = f'({id})' if id else ''
        return f'{irrad} {level}{pos}{id}'

    class Meta:
        managed = False
        db_table = 'IrradiationPositionTbl'



