// About View Component
class AboutView {
    render() {
        return `
            <div class="tool-view">
                <header class="tool-view-header">
                    <button class="back-btn" id="backBtn">
                        <span>←</span> Back to Home
                    </button>
                    <h1 class="tool-view-title">
                        <span class="tool-icon">ℹ️</span>
                        About OmniTool
                    </h1>
                    <p class="tool-view-subtitle">Multi-purpose desktop utility</p>
                </header>

                <div class="tool-view-content">
                    <section class="section about-section">
                        <div class="about-logo">
                            <div class="logo-large">🛠️</div>
                            <h2>OmniTool</h2>
                            <p class="version-large">Version 1.0.0</p>
                        </div>

                        <div class="about-info">
                            <h3>About</h3>
                            <p>
                                OmniTool is a modern, cross-platform desktop application built with Electron and Python.
                                It provides various utilities including YouTube downloading, file conversion, and more.
                            </p>

                            <h3>Features</h3>
                            <ul class="feature-list">
                                <li>✅ YouTube video and audio downloading</li>
                                <li>✅ Multiple quality options</li>
                                <li>✅ Multiple format support</li>
                                <li>✅ Modern, easy-to-use interface</li>
                                <li>✅ Component-based architecture</li>
                                <li>🔄 More tools coming soon!</li>
                            </ul>

                            <h3>Technology Stack</h3>
                            <div class="tech-stack">
                                <span class="tech-badge">Electron</span>
                                <span class="tech-badge">Python</span>
                                <span class="tech-badge">yt-dlp</span>
                                <span class="tech-badge">HTML/CSS/JS</span>
                            </div>

                            <h3>Developer</h3>
                            <p>Created by <strong>ZiadMD</strong></p>

                            <h3>License</h3>
                            <p>MIT License - See LICENSE file for details</p>

                            <div class="about-actions">
                                <button class="btn btn-secondary" id="checkUpdatesBtn">
                                    <span class="btn-icon">🔄</span>
                                    Check for Updates
                                </button>
                                <button class="btn btn-secondary" id="viewLicenseBtn">
                                    <span class="btn-icon">📄</span>
                                    View License
                                </button>
                            </div>
                        </div>
                    </section>
                </div>
            </div>
        `;
    }

    attachEventListeners() {
        document.getElementById('backBtn').addEventListener('click', () => {
            window.router.navigateTo('home');
        });

        document.getElementById('checkUpdatesBtn').addEventListener('click', () => {
            alert('You are using the latest version!');
        });

        document.getElementById('viewLicenseBtn').addEventListener('click', () => {
            alert('MIT License - See LICENSE file in the project root');
        });
    }
}

window.AboutView = AboutView;
