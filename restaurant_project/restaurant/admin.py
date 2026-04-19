from django.contrib import admin
from .models import RestaurantInfo, MenuItem, DailyMenu, Reservation


@admin.register(RestaurantInfo)
class RestaurantInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email']


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display  = ['name', 'course', 'price', 'is_active']
    list_filter   = ['course', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active']


@admin.register(DailyMenu)
class DailyMenuAdmin(admin.ModelAdmin):
    list_display         = ['date', 'note']
    filter_horizontal    = ('items',)
    date_hierarchy       = 'date'


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display  = ['guest_name', 'date', 'time_slot', 'party_size', 'status']
    list_filter   = ['status', 'date']
    search_fields = ['guest_name', 'email']
    list_editable = ['status']
    date_hierarchy = 'date'