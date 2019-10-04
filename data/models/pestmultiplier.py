from django.db import models

class PestMultiplier(models.Model):
    """
    These multipliers will boost or handicap the practice depending on the pests the
    user is having problems with. A value larger than 1 will boost the practice, whereas
    a value lower than 1 will handicap it. A value equal to 1 will not make a difference.
    """
    practice = models.ForeignKey('Practice', on_delete=models.CASCADE)
    pest = models.ForeignKey('Pest', on_delete=models.CASCADE)
    multiplier = models.DecimalField(max_digits=7, decimal_places=6)
