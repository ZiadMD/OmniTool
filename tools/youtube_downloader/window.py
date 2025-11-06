"""
YouTube Downloader Window
Modern PyQt6 interface with thumbnail preview and quality selection
"""

import requests
from io import BytesIO
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QProgressBar,
    QTextEdit, QFileDialog, QRadioButton, QButtonGroup,
    QGroupBox, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPixmap, QImage, QFont
from PIL import Image

from .downloader import YouTubeDownloader


class DownloadThread(QThread):
    """Background thread for downloading"""
    progress = pyqtSignal(dict)
    finished = pyqtSignal(dict)
    
    def __init__(self, downloader, url, download_type, quality=None):
        super().__init__()
        self.downloader = downloader
        self.url = url
        self.download_type = download_type
        self.quality = quality
        
    def run(self):
        """Run download in background"""
        self.downloader.set_progress_callback(lambda data: self.progress.emit(data))
        
        if self.download_type == "video":
            result = self.downloader.download_video(self.url, self.quality or 'best')
        else:
            result = self.downloader.download_audio(self.url)
            
        self.finished.emit(result)


class VideoInfoThread(QThread):
    """Background thread for fetching video info"""
    finished = pyqtSignal(dict)
    
    def __init__(self, downloader, url):
        super().__init__()
        self.downloader = downloader
        self.url = url
        
    def run(self):
        """Fetch video info in background"""
        video_info = self.downloader.get_video_info(self.url)
        self.finished.emit(video_info)


class YouTubeDownloaderWindow(QMainWindow):
    """Modern YouTube Downloader window"""

    def __init__(self):
        super().__init__()
        self.downloader = YouTubeDownloader()
        self.video_info = None
        self.is_downloading = False

        self._initialize_ui()
        self._apply_modern_theme()

    def _initialize_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("YouTube Downloader Pro")
        self.setMinimumSize(900, 700)
        self.resize(1000, 750)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Build UI sections
        self._create_header_section(main_layout)
        self._create_url_input_section(main_layout)
        self._create_video_info_section(main_layout)
        self._create_download_options_section(main_layout)
        self._create_progress_section(main_layout)
        self._create_activity_log_section(main_layout)
        self._create_footer_section(main_layout)

    def _create_header_section(self, parent_layout):
        """Create header"""
        header_label = QLabel("🎬 YouTube Downloader Pro")
        header_label.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setStyleSheet("""
            QLabel {
                padding: 15px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 10px;
                color: white;
            }
        """)
        parent_layout.addWidget(header_label)

    def _create_url_input_section(self, parent_layout):
        """Create URL input section"""
        url_group = QGroupBox("📎 Video URL")
        url_group.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        url_layout = QHBoxLayout()
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste YouTube URL here (video or playlist)...")
        self.url_input.setFont(QFont("Segoe UI", 10))
        self.url_input.setMinimumHeight(40)
        self.url_input.returnPressed.connect(self._fetch_video_info)

        self.fetch_info_button = QPushButton("🔍 Get Info")
        self.fetch_info_button.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.fetch_info_button.setMinimumHeight(40)
        self.fetch_info_button.setMinimumWidth(120)
        self.fetch_info_button.clicked.connect(self._fetch_video_info)
        self.fetch_info_button.setCursor(Qt.CursorShape.PointingHandCursor)

        url_layout.addWidget(self.url_input, 4)
        url_layout.addWidget(self.fetch_info_button, 1)
        url_group.setLayout(url_layout)
        parent_layout.addWidget(url_group)
        
    def _create_video_info_section(self, parent_layout):
        """Create video info section with thumbnail"""
        info_group = QGroupBox("📺 Video Information")
        info_group.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        info_layout = QHBoxLayout()
        
        # Thumbnail container
        thumbnail_container = QWidget()
        thumbnail_layout = QVBoxLayout(thumbnail_container)
        
        self.thumbnail_label = QLabel()
        self.thumbnail_label.setMinimumSize(320, 180)
        self.thumbnail_label.setMaximumSize(320, 180)
        self.thumbnail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thumbnail_label.setStyleSheet("""
            QLabel {
                background-color: #34495e;
                border-radius: 8px;
                color: #ecf0f1;
                font-size: 14px;
            }
        """)
        self.thumbnail_label.setText("No thumbnail\n\nPaste URL and click\n'Get Info'")
        thumbnail_layout.addWidget(self.thumbnail_label)
        
        # Info text container
        info_text_container = QWidget()
        info_text_layout = QVBoxLayout(info_text_container)
        
        self.title_label = QLabel("Title: -")
        self.title_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.title_label.setWordWrap(True)

        self.duration_label = QLabel("Duration: -")
        self.duration_label.setFont(QFont("Segoe UI", 10))

        self.uploader_label = QLabel("Uploader: -")
        self.uploader_label.setFont(QFont("Segoe UI", 10))

        self.views_label = QLabel("Views: -")
        self.views_label.setFont(QFont("Segoe UI", 10))

        self.type_label = QLabel("Type: -")
        self.type_label.setFont(QFont("Segoe UI", 10))

        info_text_layout.addWidget(self.title_label)
        info_text_layout.addWidget(self.duration_label)
        info_text_layout.addWidget(self.uploader_label)
        info_text_layout.addWidget(self.views_label)
        info_text_layout.addWidget(self.type_label)
        info_text_layout.addStretch()
        
        info_layout.addWidget(thumbnail_container)
        info_layout.addWidget(info_text_container, 1)
        info_group.setLayout(info_layout)
        
        # Initially hidden
        info_group.setMaximumHeight(0)
        self.video_info_group = info_group
        parent_layout.addWidget(info_group)
        
    def _create_download_options_section(self, parent_layout):
        """Create download options section"""
        options_group = QGroupBox("⚙️ Download Options")
        options_group.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        options_layout = QVBoxLayout()
        
        # Download type
        type_layout = QHBoxLayout()
        type_label = QLabel("Download Type:")
        type_label.setFont(QFont("Segoe UI", 10))
        
        self.download_type_button_group = QButtonGroup()
        self.video_radio = QRadioButton("🎬 Video")
        self.video_radio.setFont(QFont("Segoe UI", 10))
        self.video_radio.setChecked(True)
        self.video_radio.toggled.connect(self._on_download_type_changed)

        self.audio_radio = QRadioButton("🎵 Audio (MP3)")
        self.audio_radio.setFont(QFont("Segoe UI", 10))

        self.download_type_button_group.addButton(self.video_radio)
        self.download_type_button_group.addButton(self.audio_radio)

        type_layout.addWidget(type_label)
        type_layout.addWidget(self.video_radio)
        type_layout.addWidget(self.audio_radio)
        type_layout.addStretch()
        
        # Quality selection
        quality_layout = QHBoxLayout()
        quality_label = QLabel("Quality:")
        quality_label.setFont(QFont("Segoe UI", 10))
        
        self.quality_selector = QComboBox()
        self.quality_selector.setFont(QFont("Segoe UI", 10))
        self.quality_selector.setMinimumHeight(35)
        self.quality_selector.addItems([
            "Best Available",
            "2160p (4K)",
            "1440p (2K)",
            "1080p (Full HD)",
            "720p (HD)",
            "480p",
            "360p",
            "240p"
        ])
        
        quality_layout.addWidget(quality_label)
        quality_layout.addWidget(self.quality_selector, 1)

        options_layout.addLayout(type_layout)
        options_layout.addLayout(quality_layout)
        options_group.setLayout(options_layout)
        parent_layout.addWidget(options_group)
        
    def _create_progress_section(self, parent_layout):
        """Create progress section"""
        progress_group = QGroupBox("📊 Download Progress")
        progress_group.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        progress_layout = QVBoxLayout()
        
        # Download button
        self.download_button = QPushButton("⬇️ Start Download")
        self.download_button.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.download_button.setMinimumHeight(50)
        self.download_button.clicked.connect(self._start_download)
        self.download_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.download_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #11998e, stop:1 #38ef7d);
                color: white;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0f8675, stop:1 #2ecc71);
            }
            QPushButton:pressed {
                background: #0a5f4f;
            }
            QPushButton:disabled {
                background: #95a5a6;
            }
        """)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumHeight(30)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        
        # Status label
        self.status_label = QLabel("Ready to download")
        self.status_label.setFont(QFont("Segoe UI", 10))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        progress_layout.addWidget(self.download_button)
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.status_label)
        progress_group.setLayout(progress_layout)
        parent_layout.addWidget(progress_group)
        
    def _create_activity_log_section(self, parent_layout):
        """Create activity log section"""
        log_group = QGroupBox("📝 Activity Log")
        log_group.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        log_layout = QVBoxLayout()
        
        self.activity_log = QTextEdit()
        self.activity_log.setReadOnly(True)
        self.activity_log.setFont(QFont("Consolas", 9))
        self.activity_log.setMaximumHeight(120)

        log_layout.addWidget(self.activity_log)
        log_group.setLayout(log_layout)
        parent_layout.addWidget(log_group)
        
        # Initial log messages
        self._log_message("Welcome to YouTube Downloader Pro! 🎉")
        self._log_message(f"Download directory: {self.downloader.get_download_directory()}")

    def _create_footer_section(self, parent_layout):
        """Create footer with directory selection"""
        footer_layout = QHBoxLayout()
        
        directory_label = QLabel("📁 Save to:")
        directory_label.setFont(QFont("Segoe UI", 9))

        self.directory_path_label = QLabel(self.downloader.get_download_directory())
        self.directory_path_label.setFont(QFont("Segoe UI", 9))
        self.directory_path_label.setStyleSheet("color: #3498db;")

        change_directory_button = QPushButton("Change")
        change_directory_button.setFont(QFont("Segoe UI", 9))
        change_directory_button.setMaximumWidth(80)
        change_directory_button.clicked.connect(self._change_directory)
        change_directory_button.setCursor(Qt.CursorShape.PointingHandCursor)

        footer_layout.addWidget(directory_label)
        footer_layout.addWidget(self.directory_path_label, 1)
        footer_layout.addWidget(change_directory_button)

        parent_layout.addLayout(footer_layout)
        
    def _apply_modern_theme(self):
        """Apply modern theme"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ecf0f1;
            }
            QGroupBox {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                margin-top: 15px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 5px 10px;
                background-color: white;
                border-radius: 5px;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                background-color: white;
                selection-background-color: #3498db;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
            QComboBox {
                padding: 6px;
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                background-color: white;
            }
            QComboBox:focus {
                border: 2px solid #3498db;
            }
            QProgressBar {
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                text-align: center;
                background-color: #ecf0f1;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 4px;
            }
            QTextEdit {
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                background-color: #f8f9fa;
                padding: 8px;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
        """)
        
    def _on_download_type_changed(self):
        """Handle download type change"""
        is_video_mode = self.video_radio.isChecked()
        self.quality_selector.setEnabled(is_video_mode)

    def _fetch_video_info(self):
        """Fetch video information"""
        url = self.url_input.text().strip()
        
        if not url:
            QMessageBox.warning(self, "Warning", "Please enter a YouTube URL")
            return
            
        self._log_message("\n🔍 Fetching video information...")
        self.fetch_info_button.setEnabled(False)
        self.fetch_info_button.setText("Loading...")

        # Start info thread
        self.info_thread = VideoInfoThread(self.downloader, url)
        self.info_thread.finished.connect(self._on_video_info_received)
        self.info_thread.start()
        
    def _on_video_info_received(self, video_info):
        """Handle received video info"""
        self.fetch_info_button.setEnabled(True)
        self.fetch_info_button.setText("🔍 Get Info")

        if video_info['status'] == 'error':
            self._log_message(f"❌ Error: {video_info['message']}")
            QMessageBox.critical(self, "Error", video_info['message'])
            return
            
        self.video_info = video_info

        # Animate info section
        self._animate_height(self.video_info_group, 0, 250)

        # Update info display
        if video_info['type'] == 'playlist':
            self.title_label.setText(f"📁 {video_info['title']}")
            self.duration_label.setText(f"Videos: {video_info['count']}")
            self.uploader_label.setText(f"Uploader: {video_info['uploader']}")
            self.views_label.setText("")
            self.type_label.setText("Type: Playlist")
            self.thumbnail_label.setText("Playlist\n\n(No thumbnail)")
            self._log_message(f"✓ Playlist: {video_info['title']} ({video_info['count']} videos)")
        else:
            self.title_label.setText(f"🎬 {video_info['title']}")
            duration_min = video_info['duration'] // 60
            duration_sec = video_info['duration'] % 60
            self.duration_label.setText(f"Duration: {duration_min}:{duration_sec:02d}")
            self.uploader_label.setText(f"Uploader: {video_info['uploader']}")
            self.views_label.setText(f"Views: {video_info['view_count']:,}")
            self.type_label.setText("Type: Single Video")
            self._log_message(f"✓ Video: {video_info['title']}")

            # Load thumbnail
            self._load_thumbnail()

    def _load_thumbnail(self):
        """Load video thumbnail"""
        try:
            url = self.url_input.text().strip()

            # Extract video ID
            if 'youtube.com/watch?v=' in url:
                video_id = url.split('watch?v=')[1].split('&')[0]
            elif 'youtu.be/' in url:
                video_id = url.split('youtu.be/')[1].split('?')[0]
            else:
                return
                
            thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
            
            # Download and display thumbnail
            response = requests.get(thumbnail_url, timeout=5)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                image = image.resize((320, 180), Image.Resampling.LANCZOS)
                
                # Convert to QPixmap
                image_bytes = BytesIO()
                image.save(image_bytes, format='PNG')
                qimage = QImage()
                qimage.loadFromData(image_bytes.getvalue())
                pixmap = QPixmap.fromImage(qimage)
                
                self.thumbnail_label.setPixmap(pixmap)
                self.thumbnail_label.setScaledContents(True)
        except Exception as error:
            self._log_message(f"⚠️ Could not load thumbnail: {str(error)}")

    def _animate_height(self, widget, start_height, end_height):
        """Animate widget height"""
        self.height_animation = QPropertyAnimation(widget, b"maximumHeight")
        self.height_animation.setDuration(300)
        self.height_animation.setStartValue(start_height)
        self.height_animation.setEndValue(end_height)
        self.height_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.height_animation.start()

    def _start_download(self):
        """Start download process"""
        if self.is_downloading:
            QMessageBox.warning(self, "Warning", "A download is already in progress")
            return
            
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Warning", "Please enter a YouTube URL")
            return
            
        download_type = "video" if self.video_radio.isChecked() else "audio"
        quality = self.quality_selector.currentText()

        self.is_downloading = True
        self.download_button.setEnabled(False)
        self.download_button.setText("⏳ Downloading...")
        self.progress_bar.setValue(0)
        self.status_label.setText("Initializing download...")
        
        if download_type == "video":
            self._log_message(f"\n📥 Starting video download ({quality})...")
        else:
            self._log_message("\n🎵 Starting audio download (MP3)...")

        # Start download thread
        self.download_thread = DownloadThread(
            self.downloader, url, download_type, quality
        )
        self.download_thread.progress.connect(self._on_download_progress)
        self.download_thread.finished.connect(self._on_download_finished)
        self.download_thread.start()
        
    def _on_download_progress(self, progress_data):
        """Handle download progress"""
        if progress_data['status'] == 'downloading':
            percentage = progress_data['percentage']
            speed = progress_data['speed']

            self.progress_bar.setValue(int(percentage))
            self.status_label.setText(f"Downloading: {percentage:.1f}% | Speed: {speed}")
        elif progress_data['status'] == 'finished':
            self.status_label.setText("Processing... Please wait")
            
    def _on_download_finished(self, result):
        """Handle download completion"""
        self.is_downloading = False
        self.download_button.setEnabled(True)
        self.download_button.setText("⬇️ Start Download")

        if result['status'] == 'success':
            self.progress_bar.setValue(100)
            self.status_label.setText("✓ Download completed!")
            self._log_message(f"✓ {result['message']}")
            self._log_message(f"📂 Saved to: {self.downloader.get_download_directory()}")

            QMessageBox.information(
                self, "Success",
                f"{result['message']}\n\nSaved to:\n{self.downloader.get_download_directory()}"
            )
        else:
            self.progress_bar.setValue(0)
            self.status_label.setText("❌ Download failed")
            self._log_message(f"❌ {result['message']}")
            QMessageBox.critical(self, "Error", result['message'])
            
    def _change_directory(self):
        """Change download directory"""
        new_directory = QFileDialog.getExistingDirectory(
            self, "Select Download Directory",
            self.downloader.get_download_directory()
        )
        
        if new_directory:
            self.downloader.set_download_directory(new_directory)
            self.directory_path_label.setText(new_directory)
            self._log_message(f"\n📁 Directory changed to: {new_directory}")

    def _log_message(self, message):
        """Add message to activity log"""
        self.activity_log.append(message)
