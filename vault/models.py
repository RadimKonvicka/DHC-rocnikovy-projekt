from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Release(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    release_date = models.DateField()

    def __str__(self):
        return f"{self.artist.name} - {self.title}"

class Track(models.Model):
    release = models.ForeignKey(Release, on_delete=models.CASCADE, related_name='tracks')
    title = models.CharField(max_length=200)
    duration = models.DurationField(help_text="Format: MM:SS")

    def __str__(self):
        return self.title