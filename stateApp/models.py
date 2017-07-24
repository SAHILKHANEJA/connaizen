from django.db import models

class Location(models.Model):
	city = models.CharField(max_length=50)
	latitude = models.FloatField()
	longitude = models.FloatField()
	state = models.CharField(max_length=50)
	
	class Meta:
		db_table = 'location'
		unique_together = ("latitude", "longitude")

	def __str__(self):
		return str(self.latitude) + ':' + str(self.longitude) + ':' + str(self.city)


