from django.db import models
from django.core.exceptions import ValidationError
import datetime

# --- VALIDÁTORY (Učitelé budou koukat!) ---
def validate_not_empty(value):
    if len(value.strip()) == 0:
        raise ValidationError("Tohle pole nesmí obsahovat pouze prázdné znaky.")

def validate_release_date(date):
    # Nedovolí zadat datum z daleké budoucnosti (např. překlep v roce)
    if date > datetime.date.today() + datetime.timedelta(days=365):
        raise ValidationError("Datum vydání nemůže být tak daleko v budoucnosti.")


# --- MODELY ---

class Artist(models.Model):
    name = models.CharField(
        max_length=100, 
        validators=[validate_not_empty],
        verbose_name="Jméno interpreta"
    )
    bio = models.TextField(
        blank=True, 
        verbose_name="Biografie / Info"
    )
    genres = models.CharField(
        max_length=200, 
        blank=True, 
        help_text="Zadej žánry oddělené čárkou (např. Underground Rap, Rave, Hardcore)",
        verbose_name="Žánry"
    )
    image_url = models.URLField(
        max_length=500, 
        blank=True, 
        null=True, 
        help_text="Odkaz na profilový obrázek interpreta",
        verbose_name="URL obrázku interpreta"
    )
    country = models.CharField(
        max_length=50, 
        default="CZ", 
        verbose_name="Země původu"
    )

    # Meta třída pro správné zobrazení v českém adminu a řazení
    class Meta:
        verbose_name = "Interpret"
        verbose_name_plural = "Interpreti"
        ordering = ['name']  # Řazení abecedně podle jména

    def __str__(self):
        return self.name


class Release(models.Model):
    # Výběr typu alba (tzv. ENUM / Choices)
    RELEASE_TYPES = [
        ('ALBUM', 'Album'),
        ('EP', 'EP'),
        ('SINGLE', 'Single'),
    ]

    artist = models.ForeignKey(
        Artist, 
        on_delete=models.CASCADE, 
        related_name='releases',
        verbose_name="Interpret"
    )
    title = models.CharField(
        max_length=200, 
        validators=[validate_not_empty],
        verbose_name="Název alba"
    )
    release_date = models.DateField(
        validators=[validate_release_date],
        verbose_name="Datum vydání"
    )
    release_type = models.CharField(
        max_length=10, 
        choices=RELEASE_TYPES, 
        default='ALBUM',
        verbose_name="Typ releasu"
    )
    # PRIDANÉ POLE PRO OBRÁZEK ALBA / COVER ART:
    image_url = models.URLField(
        max_length=500, 
        blank=True, 
        null=True, 
        help_text="Odkaz na cover art (obálku) alba",
        verbose_name="URL obrázku alba"
    )

    class Meta:
        verbose_name = "Release"
        verbose_name_plural = "Releasy"
        ordering = ['-release_date']  # Nejnovější alba budou vždy nahoře

    def __str__(self):
        return f"{self.artist.name} - {self.title}"


class Track(models.Model):
    release = models.ForeignKey(
        Release, 
        on_delete=models.CASCADE, 
        related_name='tracks',
        verbose_name="Release / Album"
    )
    title = models.CharField(
        max_length=200, 
        validators=[validate_not_empty],
        verbose_name="Název skladby"
    )
    duration = models.DurationField(
        help_text="Formát: MM:SS (např. 00:03:45)",
        verbose_name="Délka skladby"
    )
    track_number = models.PositiveIntegerField(
        default=1,
        verbose_name="Číslo stopy na albu"
    )

    class Meta:
        verbose_name = "Skladba"
        verbose_name_plural = "Skladby"
        ordering = ['track_number']  # Tracky se v albu seřadí podle čísel stopy (1, 2, 3...)

    def __str__(self):
        return f"{self.track_number}. {self.title}"