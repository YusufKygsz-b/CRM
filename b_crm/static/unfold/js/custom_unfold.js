document.addEventListener("DOMContentLoaded", function() {
    var buttons = document.querySelectorAll('button[type="submit"][x-show="action"]');
    buttons.forEach(function(button) {
        button.style.display = "block";
    });
});


document.addEventListener("DOMContentLoaded", function() {
    var elements = document.querySelectorAll('button, input, optgroup, select, textarea');
    elements.forEach(function(element) {
        element.style.color = 'black'; // Varsayılan rengi uygular
    });
});