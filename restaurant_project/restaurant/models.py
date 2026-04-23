from django.db import models
from django.utils import timezone
import datetime

COURSE_CHOICES = [
    ('main',    'Main Dish'),
    ('side',    'Side Dish'),
    ('dessert', 'Dessert'),
]

TIME_SLOT_CHOICES = [
    ('18:00', '6:00 PM'),
    ('18:30', '6:30 PM'),
    ('19:00', '7:00 PM'),
    ('19:30', '7:30 PM'),
    ('20:00', '8:00 PM'),
    ('20:30', '8:30 PM'),
    ('21:00', '9:00 PM'),
]

CLOSED_DAYS = [0]  # 0 = Monday


class RestaurantInfo(models.Model):
    name        = models.CharField(max_length=200)
    tagline     = models.CharField(max_length=300, blank=True)
    story       = models.TextField(help_text="The restaurant's story — shown on About page")
    history     = models.TextField(help_text="History & founding — shown on About page")
    chef_name   = models.CharField(max_length=200, blank=True)
    chef_bio    = models.TextField(blank=True)
    address     = models.TextField()
    phone       = models.CharField(max_length=50)
    email       = models.EmailField()
    dinner_start = models.TimeField(default=datetime.time(18, 0))
    dinner_end   = models.TimeField(default=datetime.time(21, 0))
    hero_image  = models.ImageField(upload_to='restaurant/', blank=True)
    chef_image  = models.ImageField(upload_to='restaurant/', blank=True)

    class Meta:
        verbose_name = "Restaurant info"
        verbose_name_plural = "Restaurant info"

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    course      = models.CharField(max_length=20, choices=COURSE_CHOICES, default='main')
    name        = models.CharField(max_length=200)
    description = models.TextField()
    price       = models.DecimalField(max_digits=8, decimal_places=2)
    allergens   = models.CharField(max_length=300, blank=True,
                                   help_text="e.g. nuts, dairy, gluten")
    image       = models.ImageField(upload_to='menu/', blank=True)
    is_active   = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_course_display()} — {self.name}"


class DailyMenu(models.Model):
    date  = models.DateField(unique=True)
    items = models.ManyToManyField(MenuItem, related_name='daily_menus')
    note  = models.CharField(max_length=300, blank=True,
                              help_text="Optional note e.g. 'Chef's special tasting menu'")

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Menu for {self.date.strftime('%A, %d %B %Y')}"

    def get_mains(self):
        return self.items.filter(course='main')

    def get_sides(self):
        return self.items.filter(course='side')

    def get_desserts(self):
        return self.items.filter(course='dessert')

    @classmethod
    def get_today(cls):
        today = timezone.localdate()
        try:
            return cls.objects.get(date=today)
        except cls.DoesNotExist:
            return None

    @classmethod
    def is_closed_today(cls):
        return timezone.localdate().weekday() in CLOSED_DAYS


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    guest_name  = models.CharField(max_length=200)
    email       = models.EmailField()
    phone       = models.CharField(max_length=50)
    date        = models.DateField()
    time_slot   = models.CharField(max_length=10, choices=TIME_SLOT_CHOICES)
    party_size  = models.PositiveIntegerField()
    special_requests = models.TextField(blank=True)
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES,
                                   default='pending')
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'time_slot']

    def __str__(self):
        return f"{self.guest_name} — {self.date} {self.time_slot} ({self.party_size} guests)"
    
class GalleryPhoto(models.Model):
    CATEGORY_CHOICES = [
        ('ambience', 'Ambience'),
        ('food',     'Food'),
        ('chef',     'Chef'),
        ('events',   'Events'),
    ]

    title      = models.CharField(max_length=200, blank=True)
    image      = models.ImageField(upload_to='gallery/')
    category   = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='ambience')
    order      = models.PositiveIntegerField(default=0, help_text='Lower number shows first')
    is_active  = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return self.title or f'Photo {self.id}'
    