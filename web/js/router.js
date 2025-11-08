// Router - Handles navigation between views
class Router {
    constructor() {
        this.currentView = null;
        this.appView = document.getElementById('app-view');
    }

    navigateTo(viewName) {
        let view;

        try {
            switch(viewName) {
                case 'home':
                    view = new HomeView();
                    break;
                case 'youtube-downloader':
                    console.log('Creating YouTubeDownloader instance...');
                    view = new YouTubeDownloader();
                    console.log('YouTubeDownloader instance created successfully');
                    break;
                case 'settings':
                    view = new SettingsView();
                    break;
                case 'about':
                    view = new AboutView();
                    break;
                default:
                    view = new HomeView();
            }

            this.render(view);
        } catch (error) {
            console.error('Error navigating to view:', viewName, error);
            alert(`Error loading ${viewName}: ${error.message}`);
            // Fallback to home
            view = new HomeView();
            this.render(view);
        }
    }

    render(view) {
        this.currentView = view;
        this.appView.innerHTML = view.render();
        
        // Attach event listeners if the view has them
        if (view.attachEventListeners) {
            view.attachEventListeners();
        }

        // Scroll to top
        this.appView.scrollTop = 0;
    }

    getCurrentView() {
        return this.currentView;
    }
}

// Make it globally available
window.Router = Router;
