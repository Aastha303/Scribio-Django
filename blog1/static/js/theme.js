document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchInput');
    const themeCards = document.querySelectorAll('.theme-card');

    if (!searchInput || themeCards.length === 0) {
        console.warn("🟡 searchInput or themeCards not found");
        return;
    }

    searchInput.addEventListener('input', function (e) {
        const query = e.target.value.toLowerCase().trim();

        themeCards.forEach(card => {
            const themeName = card.getAttribute('data-theme-name').toLowerCase();
            if (themeName.includes(query)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
});
