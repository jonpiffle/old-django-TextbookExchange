from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
class Textbook(models.Model):
	title = models.CharField(max_length=255)
	dept = models.CharField(max_length=10)
	course_num = models.CharField(max_length=10)

	def get_absolute_url(self):
		return reverse('exchange:textbook_detail', args=[self.pk])

	def __unicode__(self):
		return u"%s %s: %s" % (self.dept, self.course_num, self.title)

class Own(models.Model):
	owner = models.ForeignKey('message.Person', related_name='owns')
	textbook = models.ForeignKey(Textbook, related_name='belongs_to')
	asking_price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

	def get_absolute_url(self):
		return reverse('exchange:library')

	def __unicode__(self):
		textbook = self.textbook
		return u"%s %s: %s" % (textbook.dept, textbook.course_num, textbook.title)
