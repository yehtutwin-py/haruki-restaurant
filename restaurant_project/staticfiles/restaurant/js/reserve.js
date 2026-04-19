const dateInput = document.getElementById('booking-date');

function isMondayOrPast(dateStr) {
    if (!dateStr) return false;
    const d = new Date(dateStr + 'T00:00:00');
    return d.getDay() === 1;
}

function validateDate() {
    const val = dateInput.value;
    if (isMondayOrPast(val)) {
        dateInput.setCustomValidity('We are closed on Mondays. Please choose another day.');
        dateInput.reportValidity();
        dateInput.value = '';
    } else {
        dateInput.setCustomValidity('');
    }
}

dateInput.addEventListener('change', validateDate);

dateInput.closest('form').addEventListener('submit', function(e) {
    if (isMondayOrPast(dateInput.value)) {
        e.preventDefault();
        dateInput.setCustomValidity('We are closed on Mondays. Please choose another day.');
        dateInput.reportValidity();
        dateInput.value = '';
    }
});