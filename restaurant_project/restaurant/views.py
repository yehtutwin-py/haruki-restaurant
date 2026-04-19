from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import RestaurantInfo, DailyMenu, Reservation, CLOSED_DAYS, TIME_SLOT_CHOICES
import datetime
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404

def get_info():
    return RestaurantInfo.objects.first()

def home(request):
    info       = get_info()
    today_menu = DailyMenu.get_today()
    is_closed  = DailyMenu.is_closed_today()
    return render(request, 'restaurant/home.html', {
        'info':       info,
        'today_menu': today_menu,
        'is_closed':  is_closed,
    })


def about(request):
    info = get_info()
    return render(request, 'restaurant/about.html', {'info': info})


def todays_menu(request):
    today     = timezone.localdate()
    is_closed = DailyMenu.is_closed_today()
    menu      = DailyMenu.get_today()
    return render(request, 'restaurant/menu.html', {
        'menu':      menu,
        'today':     today,
        'is_closed': is_closed,
    })


def reserve(request):
    info     = get_info()
    today    = timezone.localdate()
    min_date = today + datetime.timedelta(days=1)

    if request.method == 'POST':
        date_str   = request.POST.get('date')
        time_slot  = request.POST.get('time_slot')
        party_size = request.POST.get('party_size')
        guest_name = request.POST.get('guest_name')
        email      = request.POST.get('email')
        phone      = request.POST.get('phone')
        special    = request.POST.get('special_requests', '')

        try:
            chosen_date = datetime.date.fromisoformat(date_str)
        except (ValueError, TypeError):
            messages.error(request, 'Please choose a valid date.')
            return redirect('reserve')

        # Block Monday
        if chosen_date.weekday() in CLOSED_DAYS:
            messages.error(request, 'We are closed on Mondays. Please choose another day.')
            return redirect('reserve')

        # Block past dates
        if chosen_date <= today:
            messages.error(request, 'Please book at least one day in advance.')
            return redirect('reserve')

        # ✅ Check if time slot is already taken
        already_booked = Reservation.objects.filter(
            date      = chosen_date,
            time_slot = time_slot,
            status__in = ['pending', 'confirmed']   # ignore cancelled
        ).exists()

        if already_booked:
            messages.error(
                request,
                f'Sorry, the {dict(TIME_SLOT_CHOICES)[time_slot]} slot on '
                f'{chosen_date.strftime("%A, %d %B %Y")} is already reserved. '
                f'Please choose a different time.'
            )
            return redirect('reserve')

        reservation = Reservation.objects.create(
            guest_name       = guest_name,
            email            = email,
            phone            = phone,
            date             = chosen_date,
            time_slot        = time_slot,
            party_size       = int(party_size),
            special_requests = special,
            status           = 'pending',
        )
        messages.success(request, f'Thank you, {guest_name}! Your reservation request has been received.')
        return redirect('reservation_confirmed', pk=reservation.pk)

    # Build availability map for the next 30 days
    from datetime import timedelta
    booked_slots = Reservation.objects.filter(
        date__gte  = min_date,
        date__lte  = today + timedelta(days=30),
        status__in = ['pending', 'confirmed']
    ).values_list('date', 'time_slot')

    # Make a set of "date|time_slot" strings for easy JS lookup
    booked_set = [f"{d}|{t}" for d, t in booked_slots]

    return render(request, 'restaurant/reserve.html', {
        'info':       info,
        'time_slots': TIME_SLOT_CHOICES,
        'min_date':   min_date.isoformat(),
        'booked_set': booked_set,        # ← pass to template
    })

def reservation_confirmed(request, pk):
    reservation = Reservation.objects.get(pk=pk)
    return render(request, 'restaurant/reservation_confirmed.html', {
        'reservation': reservation,
    })


def contact(request):
    info = get_info()
    return render(request, 'restaurant/contact.html', {'info': info})

@staff_member_required(login_url='/staff/login/')
def staff_reservations(request):
    status_filter = request.GET.get('status', 'all')
    date_filter   = request.GET.get('date', '')

    reservations = Reservation.objects.all().order_by('date', 'time_slot')

    if status_filter != 'all':
        reservations = reservations.filter(status=status_filter)

    if date_filter:
        reservations = reservations.filter(date=date_filter)

    # counts always from full list, not filtered
    all_reservations = Reservation.objects.all()

    return render(request, 'restaurant/staff_reservations.html', {
        'reservations':    reservations,
        'status_filter':   status_filter,
        'date_filter':     date_filter,
        'status_choices':  Reservation.STATUS_CHOICES,
        'pending_count':   all_reservations.filter(status='pending').count(),
        'confirmed_count': all_reservations.filter(status='confirmed').count(),
        'total_guests':    sum(r.party_size for r in all_reservations.filter(status__in=['pending','confirmed'])),
    })


@staff_member_required(login_url='/staff/login/')
def update_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Reservation.STATUS_CHOICES):
            reservation.status = new_status
            reservation.save()
            messages.success(request, f'Reservation #{reservation.pk} updated to {reservation.get_status_display()}.')

    return redirect('staff_reservations')