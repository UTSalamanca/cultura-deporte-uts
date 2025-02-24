// script.js

const attendanceRecords = {}; // Objeto para guardar los registros de asistencia

function updateClock() {
    const clock = document.getElementById('clock');
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    clock.textContent = `Hora actual: ${timeString}`;
}

function generateCalendar() {
    const calendar = document.getElementById('calendar');
    const now = new Date();
    const year = now.getFullYear();
    const month = now.getMonth();

    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    const dayNames = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'];

    calendar.innerHTML = '';
    dayNames.forEach(day => {
        const dayElement = document.createElement('div');
        dayElement.classList.add('day');
        dayElement.textContent = day;
        calendar.appendChild(dayElement);
    });

    for (let i = 0; i < firstDay; i++) {
        const emptyDay = document.createElement('div');
        emptyDay.classList.add('day');
        calendar.appendChild(emptyDay);
    }

    for (let day = 1; day <= daysInMonth; day++) {
        const dayElement = document.createElement('div');
        dayElement.classList.add('day');
        dayElement.textContent = day;

        if (day === now.getDate()) {
            dayElement.classList.add('today');
        }

        dayElement.addEventListener('click', () => handleDayClick(day, month, year, dayElement));

        calendar.appendChild(dayElement);
    }
}

function handleDayClick(day, month, year, dayElement) {
    const dateKey = `${year}-${month + 1}-${day}`; // Formato: YYYY-MM-DD

    if (dayElement.classList.contains('attended')) {
        const record = attendanceRecords[dateKey];
        showModal(`Asistencia registrada`, `Día: ${record.date}<br>Hora: ${record.time}`);
        return;
    }

    const date = new Date(year, month, day);
    const dayOfWeek = date.getDay();

    if (dayOfWeek === 0 || dayOfWeek === 6) {
        alert('No es posible tomar asistencia en sábados o domingos.');
        return;
    }

    showModal(`Registrar Asistencia`, `¿Deseas registrar asistencia para el día ${date.toLocaleDateString()}?`, () => {
        const now = new Date();
        const record = {
            date: now.toLocaleDateString(),
            time: now.toLocaleTimeString()
        };
        attendanceRecords[dateKey] = record;

        dayElement.classList.add('attended');
        closeModal();
    });
}

function showModal(title, message, confirmCallback = null) {
    const modal = document.getElementById('attendanceModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalMessage = document.getElementById('modalMessage');
    const confirmButton = document.getElementById('confirmAttendance');

    modalTitle.textContent = title;
    modalMessage.innerHTML = message;
    modal.style.display = 'block';

    if (confirmCallback) {
        confirmButton.style.display = 'block';
        confirmButton.onclick = confirmCallback;
    } else {
        confirmButton.style.display = 'none';
    }
}

function closeModal() {
    const modal = document.getElementById('attendanceModal');
    modal.style.display = 'none';
}

document.addEventListener('DOMContentLoaded', () => {
    updateClock();
    generateCalendar();
    setInterval(updateClock, 1000);

    const modal = document.getElementById('attendanceModal');
    const closeModalButton = document.querySelector('.close');

    closeModalButton.onclick = closeModal;

    window.onclick = (event) => {
        if (event.target === modal) {
            closeModal();
        }
    };
});
