document.addEventListener('DOMContentLoaded', function() {
    const tabLinks = document.querySelectorAll('.tab-link');
    const tabContents = document.querySelectorAll('.tab-content');

    tabLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();

            const tabId = this.getAttribute('data-tab');

            tabLinks.forEach(link => link.classList.remove('active'));
            this.classList.add('active');

            tabContents.forEach(content => content.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const addModelBtn = document.getElementById('addModelBtn');
    const modelFileInput = document.getElementById('modelFile');

    addModelBtn.addEventListener('click', function(e) {
        // e.preventDefault();
        modelFileInput.click();
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const addModelBtn = document.getElementById('addModelBtn');
    const modelFileInput = document.getElementById('modelFile');

    addModelBtn.addEventListener('click', function(e) {
        // e.preventDefault();
        modelFileInput.click();
    });
});




