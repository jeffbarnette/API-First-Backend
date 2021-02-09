from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator

class File(models.Model):
    file = models.FileField(upload_to='files/',
        validators=[FileExtensionValidator(allowed_extensions=['txt'])],
        blank=False, null=False)
    rows = models.IntegerField(blank=True, default=0)
    items = models.TextField(blank=True, default='')
    uploaded_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """Return the filename."""
        return self.file.name