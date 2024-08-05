document.addEventListener("DOMContentLoaded", function() {
    var buttons = document.querySelectorAll('button[type="submit"][x-show="action"]');
    buttons.forEach(function(button) {
        button.style.display = "block";
    });
});