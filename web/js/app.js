// Main Application
class App {
    constructor() {
        this.router = new Router();
        this.homeView = new HomeView();
        this.init();
    }

    init() {
        // Initialize router
        window.router = this.router;

        // Set up navbar actions
        this.setupNavbar();

        // Navigate to home view
        this.router.navigateTo('home');
    }

    setupNavbar() {
        // Settings button
        document.getElementById('settingsBtn').addEventListener('click', () => {
            this.router.navigateTo('settings');
        });

        // About button
        document.getElementById('aboutBtn').addEventListener('click', () => {
            this.router.navigateTo('about');
        });

        // Search functionality
        const searchInput = document.getElementById('searchInput');
        let searchTimeout;

        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                this.handleSearch(e.target.value);
            }, 300);
        });

        // Click on brand to go home
        document.querySelector('.navbar-brand').addEventListener('click', () => {
            searchInput.value = '';
            this.router.navigateTo('home');
        });
        document.querySelector('.navbar-brand').style.cursor = 'pointer';
    }

    handleSearch(searchTerm) {
        const currentView = this.router.getCurrentView();
        
        // Only filter if we're on the home view
        if (currentView instanceof HomeView) {
            currentView.filter(searchTerm);
            this.router.render(currentView);
        } else {
            // If not on home, navigate to home and then filter
            this.router.navigateTo('home');
            setTimeout(() => {
                const homeView = this.router.getCurrentView();
                if (homeView instanceof HomeView) {
                    homeView.filter(searchTerm);
                    this.router.render(homeView);
                }
            }, 100);
        }
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM Content Loaded');
    console.log('window.api available:', !!window.api);
    if (window.api) {
        console.log('window.api methods:', Object.keys(window.api));
    } else {
        console.error('window.api is NOT available - preload script may have failed');
    }
    
    window.app = new App();
});
