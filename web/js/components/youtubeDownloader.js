// YouTube Downloader Component
class YouTubeDownloader {
    constructor() {
        console.log('YouTubeDownloader constructor called');
        console.log('window.api available:', !!window.api);
        
        this.currentVideoInfo = null;
        // Use the exposed API from preload script instead of require
        if (window.api && window.api.getDownloadsDir) {
            this.defaultDownloadDir = window.api.getDownloadsDir();
            console.log('Default download dir:', this.defaultDownloadDir);
        } else {
            this.defaultDownloadDir = '/home/user/Downloads';
            console.warn('window.api not available, using fallback download directory');
        }
    }
    
    getUserHome() {
        // Fallback method to get user home directory
        return window.api?.getHomeDir() || '/home/user';
    }

    render() {
        return `
            <div class="tool-view">
                <header class="tool-view-header">
                    <button class="back-btn" id="backBtn">
                        <span>←</span> Back to Home
                    </button>
                    <h1 class="tool-view-title">
                        <span class="tool-icon">🎥</span>
                        YouTube Downloader
                    </h1>
                    <p class="tool-view-subtitle">Download videos and audio from YouTube</p>
                </header>

                <div class="tool-view-content">
                    <!-- URL Input Section -->
                    <section class="section">
                        <div class="input-group">
                            <input type="text" id="urlInput" placeholder="Paste YouTube URL here..." autocomplete="off">
                            <button id="fetchBtn" class="btn btn-primary">
                                <span class="btn-icon">🔍</span>
                                Fetch Info
                            </button>
                        </div>
                    </section>

                    <!-- Video Info Section -->
                    <section class="section" id="infoSection" style="display: none;">
                        <div class="video-info">
                            <div class="thumbnail-container">
                                <img id="thumbnail" src="" alt="Video thumbnail">
                            </div>
                            <div class="video-details">
                                <h2 id="videoTitle">Video Title</h2>
                                <div class="metadata">
                                    <span id="duration" class="meta-item">⏱️ Duration</span>
                                    <span id="views" class="meta-item">👁️ Views</span>
                                    <span id="author" class="meta-item">👤 Author</span>
                                </div>
                                <p id="description" class="description"></p>
                            </div>
                        </div>
                    </section>

                    <!-- Download Options Section -->
                    <section class="section" id="optionsSection" style="display: none;">
                        <h3 class="section-title">Download Options</h3>
                        <div class="options-grid">
                            <div class="option-group">
                                <label for="qualitySelect">Quality</label>
                                <select id="qualitySelect">
                                    <option value="best">Best Quality</option>
                                    <option value="2160p">4K (2160p)</option>
                                    <option value="1440p">2K (1440p)</option>
                                    <option value="1080p">Full HD (1080p)</option>
                                    <option value="720p">HD (720p)</option>
                                    <option value="480p">SD (480p)</option>
                                    <option value="360p">Low (360p)</option>
                                </select>
                            </div>

                            <div class="option-group">
                                <label for="formatSelect">Format</label>
                                <select id="formatSelect">
                                    <option value="mp4">Video (MP4)</option>
                                    <option value="webm">Video (WebM)</option>
                                    <option value="mp3">Audio (MP3)</option>
                                    <option value="m4a">Audio (M4A)</option>
                                    <option value="opus">Audio (Opus)</option>
                                </select>
                            </div>

                            <div class="option-group full-width">
                                <label for="downloadDir">Download Directory</label>
                                <div class="input-group">
                                    <input type="text" id="downloadDir" placeholder="Select download directory..." readonly value="${this.defaultDownloadDir}">
                                    <button id="browseDirBtn" class="btn btn-secondary">Browse</button>
                                </div>
                            </div>
                        </div>

                        <div class="download-action">
                            <button id="downloadBtn" class="btn btn-download">
                                <span class="btn-icon">⬇️</span>
                                Download
                            </button>
                        </div>
                    </section>

                    <!-- Progress Section -->
                    <section class="section" id="progressSection" style="display: none;">
                        <h3 class="section-title">Download Progress</h3>
                        <div class="progress-info">
                            <span id="progressStatus">Preparing download...</span>
                            <span id="progressPercent">0%</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" id="progressFill"></div>
                        </div>
                    </section>
                </div>
            </div>
        `;
    }

    attachEventListeners() {
        // Back button
        document.getElementById('backBtn').addEventListener('click', () => {
            window.router.navigateTo('home');
        });

        // YouTube downloader functionality
        const urlInput = document.getElementById('urlInput');
        const fetchBtn = document.getElementById('fetchBtn');
        const infoSection = document.getElementById('infoSection');
        const optionsSection = document.getElementById('optionsSection');
        const progressSection = document.getElementById('progressSection');
        const downloadBtn = document.getElementById('downloadBtn');
        const browseDirBtn = document.getElementById('browseDirBtn');

        fetchBtn.addEventListener('click', () => this.fetchVideoInfo());
        urlInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.fetchVideoInfo();
        });
        
        browseDirBtn.addEventListener('click', () => this.selectDirectory());
        downloadBtn.addEventListener('click', () => this.startDownload());

        // Listen for download progress
        if (window.api && window.api.onDownloadProgress) {
            window.api.onDownloadProgress((data) => this.updateProgress(data));
        } else {
            console.error('window.api.onDownloadProgress is not available');
        }
    }

    async fetchVideoInfo() {
        const urlInput = document.getElementById('urlInput');
        const fetchBtn = document.getElementById('fetchBtn');
        const infoSection = document.getElementById('infoSection');
        const optionsSection = document.getElementById('optionsSection');
        
        const url = urlInput.value.trim();
        
        if (!url) {
            alert('Please enter a YouTube URL');
            return;
        }

        if (!this.isValidYouTubeUrl(url)) {
            alert('Please enter a valid YouTube URL');
            return;
        }

        fetchBtn.disabled = true;
        fetchBtn.innerHTML = '<span class="btn-icon">⏳</span> Loading...';

        try {
            const info = await window.api.getVideoInfo(url);
            this.currentVideoInfo = info;
            this.displayVideoInfo(info);
            
            infoSection.style.display = 'block';
            optionsSection.style.display = 'block';
            
            fetchBtn.innerHTML = '<span class="btn-icon">🔍</span> Fetch Info';
        } catch (error) {
            console.error('Error fetching video info:', error);
            alert('Failed to fetch video information. Please check the URL and try again.');
            fetchBtn.innerHTML = '<span class="btn-icon">🔍</span> Fetch Info';
        } finally {
            fetchBtn.disabled = false;
        }
    }

    displayVideoInfo(info) {
        document.getElementById('thumbnail').src = info.thumbnail || '';
        document.getElementById('videoTitle').textContent = info.title || 'Unknown Title';
        document.getElementById('duration').textContent = `⏱️ ${this.formatDuration(info.duration)}`;
        document.getElementById('views').textContent = `👁️ ${this.formatNumber(info.view_count)} views`;
        document.getElementById('author').textContent = `👤 ${info.uploader || 'Unknown'}`;
        document.getElementById('description').textContent = info.description || 'No description available';
    }

    async selectDirectory() {
        const dir = await window.api.selectDirectory();
        if (dir) {
            document.getElementById('downloadDir').value = dir;
        }
    }

    async startDownload() {
        if (!this.currentVideoInfo) {
            alert('Please fetch video info first');
            return;
        }

        const urlInput = document.getElementById('urlInput');
        const qualitySelect = document.getElementById('qualitySelect');
        const formatSelect = document.getElementById('formatSelect');
        const downloadDir = document.getElementById('downloadDir');
        const downloadBtn = document.getElementById('downloadBtn');
        const progressSection = document.getElementById('progressSection');

        const options = {
            url: urlInput.value.trim(),
            quality: qualitySelect.value,
            format: formatSelect.value,
            outputPath: downloadDir.value
        };

        downloadBtn.disabled = true;
        progressSection.style.display = 'block';
        
        try {
            await window.api.downloadVideo(options);
            
            document.getElementById('progressStatus').textContent = 'Download completed!';
            document.getElementById('progressPercent').textContent = '100%';
            document.getElementById('progressFill').style.width = '100%';
            
            setTimeout(() => {
                progressSection.style.display = 'none';
                document.getElementById('progressFill').style.width = '0%';
                document.getElementById('progressStatus').textContent = 'Preparing download...';
                document.getElementById('progressPercent').textContent = '0%';
            }, 3000);
            
        } catch (error) {
            console.error('Download error:', error);
            alert('Download failed. Please try again.');
            progressSection.style.display = 'none';
        } finally {
            downloadBtn.disabled = false;
        }
    }

    updateProgress(data) {
        if (data.status) {
            document.getElementById('progressStatus').textContent = data.status;
        }
        
        if (data.percent !== undefined) {
            const percent = Math.round(data.percent);
            document.getElementById('progressPercent').textContent = `${percent}%`;
            document.getElementById('progressFill').style.width = `${percent}%`;
        }
    }

    isValidYouTubeUrl(url) {
        const pattern = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+/;
        return pattern.test(url);
    }

    formatDuration(seconds) {
        if (!seconds) return 'Unknown';
        
        const hrs = Math.floor(seconds / 3600);
        const mins = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;
        
        if (hrs > 0) {
            return `${hrs}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        }
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }

    formatNumber(num) {
        if (!num) return '0';
        
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        }
        if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num.toString();
    }
}

// Make it globally available
window.YouTubeDownloader = YouTubeDownloader;
