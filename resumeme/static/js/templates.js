document.addEventListener('DOMContentLoaded', function() {
    // Template search functionality
    const searchInput = document.getElementById('template-search');
    const templateCards = document.querySelectorAll('.template-card');

    searchInput.addEventListener('input', function(e) {
        const searchTerm = e.target.value.toLowerCase();

        templateCards.forEach(card => {
            const templateName = card.querySelector('h3').textContent.toLowerCase();
            const templateCategory = card.dataset.category.toLowerCase();

            if (templateName.includes(searchTerm) || templateCategory.includes(searchTerm)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });

    // Color scheme selection
    const colorSchemes = document.querySelectorAll('.color-scheme');
    colorSchemes.forEach(scheme => {
        scheme.addEventListener('click', function() {
            const colors = JSON.parse(this.dataset.colors);
            // Apply colors to template preview
            applyColorScheme(colors);
        });
    });

    // Font pair selection
    const fontPairs = document.querySelectorAll('.font-pair');
    fontPairs.forEach(pair => {
        pair.addEventListener('click', function() {
            const headingFont = this.querySelector('span:first-child').style.fontFamily;
            const bodyFont = this.querySelector('span:last-child').style.fontFamily;
            // Apply fonts to template preview
            applyFontPair(headingFont, bodyFont);
        });
    });
});

function applyColorScheme(colors) {
    // Implementation for applying colors to template
    // This would update CSS variables or classes
}

function applyFontPair(headingFont, bodyFont) {
    // Implementation for applying fonts to template
    // This would update CSS variables or classes
}