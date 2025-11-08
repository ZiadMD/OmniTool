// Settings View Component
class SettingsView {
    constructor() {
        const os = require('os');
        this.defaultDir = os.homedir() + '/Downloads';
    }

    render() {
        return `
            <div class="tool-view">
                <header class="tool-view-header">
                    <button class="back-btn" id="backBtn">
                        <span>←</span> Back to Home
                    </button>
                    <h1 class="tool-view-title">
                        <span class="tool-icon">⚙️</span>
                        Settings
                    </h1>
                    <p class="tool-view-subtitle">Configure your OmniTool preferences</p>
                </header>

                <div class="tool-view-content">
                    <section class="section">
                        <h3 class="section-title">General Settings</h3>
                        
                        <div class="setting-item">
                            <label for="defaultDownloadDir">Default Download Directory</label>
                            <div class="input-group">
                                <input type="text" id="defaultDownloadDir" placeholder="${this.defaultDir}" readonly>
                                <button id="browseDefaultDirBtn" class="btn btn-secondary">Browse</button>
                            </div>
                        </div>
                        
                        <div class="setting-item">
                            <label for="themeSelect">Theme</label>
                            <select id="themeSelect">
                                <option value="dark">Dark Mode</option>
                                <option value="light">Light Mode (Coming Soon)</option>
                            </select>
                        </div>
                    </section>

                    <section class="section">
                        <h3 class="section-title">YouTube Downloader</h3>
                        
                        <div class="setting-item">
                            <label for="defaultQuality">Default Quality</label>
                            <select id="defaultQuality">
                                <option value="best">Best Quality</option>
                                <option value="1080p">Full HD (1080p)</option>
                                <option value="720p">HD (720p)</option>
                                <option value="480p">SD (480p)</option>
                            </select>
                        </div>
                        
                        <div class="setting-item">
                            <label for="defaultFormat">Default Format</label>
                            <select id="defaultFormat">
                                <option value="mp4">Video (MP4)</option>
                                <option value="mp3">Audio (MP3)</option>
                            </select>
                        </div>
                    </section>

                    <div class="settings-actions">
                        <button class="btn btn-primary" id="saveSettingsBtn">
                            <span class="btn-icon">💾</span>
                            Save Settings
                        </button>
                        <button class="btn btn-secondary" id="resetSettingsBtn">
                            <span class="btn-icon">🔄</span>
                            Reset to Defaults
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    attachEventListeners() {
        document.getElementById('backBtn').addEventListener('click', () => {
            window.router.navigateTo('home');
        });

        this.loadSettings();

        document.getElementById('browseDefaultDirBtn').addEventListener('click', async () => {
            const dir = await window.api.selectDirectory();
            if (dir) {
                document.getElementById('defaultDownloadDir').value = dir;
            }
        });

        document.getElementById('saveSettingsBtn').addEventListener('click', () => {
            this.saveSettings();
            alert('Settings saved successfully!');
        });

        document.getElementById('resetSettingsBtn').addEventListener('click', () => {
            if (confirm('Reset all settings to defaults?')) {
                this.resetSettings();
                this.loadSettings();
                alert('Settings reset to defaults');
            }
        });
    }

    loadSettings() {
        const settings = JSON.parse(localStorage.getItem('omnitool-settings') || '{}');
        
        const defaultDir = settings.defaultDownloadDir || this.defaultDir;
        document.getElementById('defaultDownloadDir').value = defaultDir;
        
        if (settings.defaultQuality) {
            document.getElementById('defaultQuality').value = settings.defaultQuality;
        }
        
        if (settings.defaultFormat) {
            document.getElementById('defaultFormat').value = settings.defaultFormat;
        }
    }

    saveSettings() {
        const settings = {
            defaultDownloadDir: document.getElementById('defaultDownloadDir').value,
            defaultQuality: document.getElementById('defaultQuality').value,
            defaultFormat: document.getElementById('defaultFormat').value,
            theme: document.getElementById('themeSelect').value
        };
        
        localStorage.setItem('omnitool-settings', JSON.stringify(settings));
    }

    resetSettings() {
        localStorage.removeItem('omnitool-settings');
    }
}

window.SettingsView = SettingsView;
