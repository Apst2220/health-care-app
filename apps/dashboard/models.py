from django.db import models


class WorldHealthStatistics(models.Model):
    country = models.CharField(max_length=3)
    sex = models.CharField(max_length=10)
    deaths_per_1lac_diabetes = models.DecimalField(max_digits=10, decimal_places=5)
    deaths_per_1lac_alcohols = models.DecimalField(max_digits=10, decimal_places=5)
    deaths_per_1lac_airpol = models.DecimalField(max_digits=10, decimal_places=5)
    prob_dying_30_70_cardiovascular = models.DecimalField(max_digits=10, decimal_places=5)
    deaths_per_1lac_road = models.DecimalField(max_digits=10, decimal_places=5)
    percent_prevalence_tabacco = models.DecimalField(max_digits=10, decimal_places=5)
    percent_obesity = models.DecimalField(max_digits=10, decimal_places=5)
    percent_poor = models.DecimalField(max_digits=10, decimal_places=5)
    avail_mach_diab = models.CharField(max_length=20)
    exist_protocols_diab = models.CharField(max_length=20)
    adol_alcohol_percent_intake = models.DecimalField(max_digits=10, decimal_places=5)
    household_Air_pol_deaths_under_5_year = models.DecimalField(max_digits=10, decimal_places=5)
    class Meta:
        db_table = "world_health_statistics"
        