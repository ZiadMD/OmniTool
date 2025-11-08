// Home View Component
class HomeView {
    constructor() {
        this.tools = [
            {
                id: 'youtube-downloader',
                icon: '🎥',
                title: 'YouTube Downloader',
                description: 'Download videos and audio from YouTube with multiple quality options',
                category: 'media',
                enabled: true
            }
        ];
        
        this.filteredTools = [...this.tools];
    }

    filter(searchTerm) {
        if (!searchTerm) {
            this.filteredTools = [...this.tools];
        } else {
            const term = searchTerm.toLowerCase();
            this.filteredTools = this.tools.filter(tool => 
                tool.title.toLowerCase().includes(term) ||
                tool.description.toLowerCase().includes(term) ||
                tool.category.toLowerCase().includes(term)
            );
        }
    }

    render() {
        return `
            <div class="home-view">
                <header class="home-header">
                    <h1 class="home-title">
                        <span class="title-icon">🛠️</span>
                        Welcome to OmniTool
                    </h1>
                    <p class="home-subtitle">
                        Your all-in-one toolkit for everyday tasks
                    </p>
                </header>

                <section class="tools-section">
                    <div class="section-header">
                        <h2>Available Tools</h2>
                        <p class="tools-count">${this.filteredTools.length} tool${this.filteredTools.length !== 1 ? 's' : ''} found</p>
                    </div>
                    ${this.filteredTools.length > 0 
                        ? ToolCard.renderGrid(this.filteredTools)
                        : '<div class="no-results"><p>No tools found matching your search</p></div>'
                    }
                </section>
            </div>
        `;
    }

    attachEventListeners() {
        // Attach click handlers to tool cards
        document.querySelectorAll('.tool-card:not(.disabled)').forEach(card => {
            card.addEventListener('click', (e) => {
                const toolId = card.dataset.toolId;
                window.router.navigateTo(toolId);
            });
        });
    }
}

// Make it globally available
window.HomeView = HomeView;
