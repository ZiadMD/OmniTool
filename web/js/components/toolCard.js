// Tool Card Component
class ToolCard {
    constructor(data) {
        this.icon = data.icon;
        this.title = data.title;
        this.description = data.description;
        this.id = data.id;
        this.enabled = data.enabled !== false;
        this.category = data.category || 'general';
    }

    render() {
        const disabledClass = this.enabled ? '' : 'disabled';
        const comingSoonBadge = this.enabled ? '' : '<span class="coming-soon-badge">Coming Soon</span>';
        
        return `
            <div class="tool-card ${disabledClass}" data-tool-id="${this.id}" data-category="${this.category}">
                <div class="tool-card-icon">${this.icon}</div>
                <div class="tool-card-content">
                    <h3 class="tool-card-title">${this.title}</h3>
                    <p class="tool-card-description">${this.description}</p>
                    ${comingSoonBadge}
                </div>
                <div class="tool-card-action">
                    <button class="tool-open-btn ${this.enabled ? '' : 'disabled'}" ${this.enabled ? '' : 'disabled'}>
                        ${this.enabled ? 'Open →' : 'Coming Soon'}
                    </button>
                </div>
            </div>
        `;
    }

    static renderGrid(tools) {
        return `
            <div class="tools-grid">
                ${tools.map(tool => new ToolCard(tool).render()).join('')}
            </div>
        `;
    }
}

// Make it globally available
window.ToolCard = ToolCard;
