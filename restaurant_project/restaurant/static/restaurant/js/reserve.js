const bookedSlots = new Set(JSON.parse(document.getElementById('booked-data').textContent));

const dateInput  = document.getElementById('booking-date');
const timeSelect = document.getElementById('time-slot');
const submitBtn  = document.getElementById('submit-btn');

function isMonday(dateStr) {
    if (!dateStr) return false;
    return new Date(dateStr + 'T00:00:00').getDay() === 1;
}

function updateSlotAvailability() {
    const chosenDate = dateInput.value;
    if (!chosenDate) return;

    let anyAvailable = false;

    Array.from(timeSelect.options).forEach(option => {
        if (!option.value) return;

        const key   = `${chosenDate}|${option.value}`;
        const taken = bookedSlots.has(key);

        option.disabled = taken;
        option.text     = taken
            ? option.text.replace(' — Full', '') + ' — Full'
            : option.text.replace(' — Full', '');

        if (!taken) anyAvailable = true;
    });

    if (timeSelect.value && bookedSlots.has(`${chosenDate}|${timeSelect.value}`)) {
        timeSelect.value = '';
    }

    if (!anyAvailable) {
        submitBtn.disabled    = true;
        submitBtn.textContent = 'No availability on this date';
    } else {
        submitBtn.disabled    = false;
        submitBtn.textContent = 'Request Reservation';
    }
}

function validateDate() {
    if (isMonday(dateInput.value)) {
        dateInput.setCustomValidity('We are closed on Mondays. Please choose another day.');
        dateInput.reportValidity();
        dateInput.value = '';
        return;
    }
    dateInput.setCustomValidity('');
    updateSlotAvailability();
}

dateInput.addEventListener('change', validateDate);

dateInput.closest('form').addEventListener('submit', function(e) {
    if (isMonday(dateInput.value)) {
        e.preventDefault();
        dateInput.setCustomValidity('We are closed on Mondays. Please choose another day.');
        dateInput.reportValidity();
        dateInput.value = '';
    }
});