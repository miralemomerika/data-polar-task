document.addEventListener('DOMContentLoaded', function() {
    var dropdownBtn = document.getElementById('dropdownBtn');
    var closeBtn = document.getElementById('closeBtn');
    var sidebar = document.getElementById('sidebar');

    // Function to open the dropdown
    function openDropdown() {
        sidebar.style.left = '0'; // Open the sidebar
        dropdownBtn.style.display = 'none'; // Hide open button
        closeBtn.style.display = 'block'; // Show close button
        sidebar.classList.add('active'); // Add active class
    }

    // Function to close the dropdown
    function closeDropdown() {
        if (sidebar.classList.contains('active')) {
            closeBtn.style.display = 'none'; // Hide close button
            dropdownBtn.style.display = 'block'; // Show open button
            sidebar.classList.remove('active'); // Remove active class
        }
    }

    dropdownBtn.addEventListener('click', openDropdown);
    closeBtn.addEventListener('click', closeDropdown);

    window.addEventListener('click', function(e) {
        if (!sidebar.contains(e.target) && !dropdownBtn.contains(e.target)) {
            closeDropdown();
        }
    });
});
