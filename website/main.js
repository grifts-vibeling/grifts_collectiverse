document.addEventListener('DOMContentLoaded', () => {
    // Check if we are on the lore page
    if (document.getElementById('lore-content')) {
        loadMarkdownContent('../data/lore/lore.md', 'lore-content');
    }
});

/**
 * Fetches and renders a Markdown file into a specified HTML element.
 * @param {string} filePath - The path to the Markdown file.
 * @param {string} elementId - The ID of the HTML element to render the content into.
 */
async function loadMarkdownContent(filePath, elementId) {
    try {
        const response = await fetch(filePath);
        if (!response.ok) {
            throw new Error(`Failed to load Markdown file: ${response.statusText}`);
        }
        const markdown = await response.text();
        const html = marked.parse(markdown);
        document.getElementById(elementId).innerHTML = html;
    } catch (error) {
        console.error("Error loading Markdown content:", error);
        document.getElementById(elementId).innerHTML = `<p class="text-red-400">Failed to load lore. Please check the console for details.</p>`;
    }
}