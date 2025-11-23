/**
 * Theme Hook - Manages user theme preferences with local storage
 *
 * Stores and retrieves theme preference (light/dark mode) in localStorage
 * Automatically applies theme on page load and provides toggle functionality
 */

const useTheme = (() => {
    const STORAGE_KEY = 'user-theme-preference';
    const THEME_LIGHT = 'light';
    const THEME_DARK = 'dark';

    /**
     * Get the current theme from localStorage
     * @returns {string} 'light' or 'dark', defaults to 'light' if not set
     */
    const getTheme = () => {
        const savedTheme = localStorage.getItem(STORAGE_KEY);
        return savedTheme || THEME_LIGHT;
    };

    /**
     * Set and save theme preference
     * @param {string} theme - 'light' or 'dark'
     */
    const setTheme = (theme) => {
        if (theme !== THEME_LIGHT && theme !== THEME_DARK) {
            console.warn(`Invalid theme: ${theme}. Use '${THEME_LIGHT}' or '${THEME_DARK}'`);
            return;
        }

        localStorage.setItem(STORAGE_KEY, theme);
        applyTheme(theme);
    };

    /**
     * Apply theme to the document
     * @param {string} theme - 'light' or 'dark'
     */
    const applyTheme = (theme) => {
        document.documentElement.setAttribute('data-theme', theme);
        document.body.classList.remove(THEME_LIGHT, THEME_DARK);
        document.body.classList.add(theme);
    };

    /**
     * Toggle between light and dark themes
     * @returns {string} The new theme after toggle
     */
    const toggleTheme = () => {
        const currentTheme = getTheme();
        const newTheme = currentTheme === THEME_LIGHT ? THEME_DARK : THEME_LIGHT;
        setTheme(newTheme);
        return newTheme;
    };

    /**
     * Initialize theme on page load
     * Applies the saved theme or defaults to light
     */
    const initTheme = () => {
        const theme = getTheme();
        applyTheme(theme);
    };

    /**
     * Check if current theme is dark
     * @returns {boolean}
     */
    const isDarkMode = () => {
        return getTheme() === THEME_DARK;
    };

    /**
     * Check if current theme is light
     * @returns {boolean}
     */
    const isLightMode = () => {
        return getTheme() === THEME_LIGHT;
    };

    // Public API
    return {
        getTheme,
        setTheme,
        toggleTheme,
        initTheme,
        isDarkMode,
        isLightMode,
        THEME_LIGHT,
        THEME_DARK
    };
})();

// Auto-initialize on DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', useTheme.initTheme);
} else {
    useTheme.initTheme();
}
