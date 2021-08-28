from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Certificate_url(models.Model):
    certificate_id = models.CharField(max_length=1000)

class Event(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	event_name = models.CharField(max_length=250)
	event_type = models.CharField(max_length=250)
	starting_date = models.DateField()
	ending_date = models.DateField(null=True)
	csv_file = models.FileField(upload_to="certificates/csv_files/")
	template = models.FileField(upload_to="certificates/templates/")
	name_column = models.CharField(max_length=250, null=True, blank=True)
	email_column = models.CharField(max_length=250, null=True, blank=True)
	org_column = models.CharField(max_length=250, null=True, blank=True)
	message = models.TextField(null=True, blank=True)
	slug = models.SlugField(null=True, blank=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.event_name)
		super(Event, self).save(*args, **kwargs)

class Participant(models.Model):
	event = models.ForeignKey(Event,  on_delete=models.CASCADE)
	name = models.CharField(max_length=250)
	email = models.CharField(max_length=250)
	org = models.CharField(max_length=250)
	status = models.BooleanField(default=False)