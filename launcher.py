"""
OmniTool - Clean Launcher Application
Refactored to use the new clean architecture
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QScrollArea, QFrame, QGridLayout,
    QButtonGroup, QRadioButton, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor

from core import AppManager, ToolCategory


class ToolCard(QFrame):
    """Modern card widget for displaying a tool"""
    clicked = pyqtSignal(str)

    def __init__(self, tool_metadata: dict, parent=None):
        super().__init__(parent)
        self.tool_metadata = tool_metadata
        self.setup_ui()

    def setup_ui(self):
        """Setup the card UI"""
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Icon
        icon_label = QLabel(self.tool_metadata['icon'])
        icon_label.setFont(QFont("Segoe UI", 36))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Name
        name_label = QLabel(self.tool_metadata['name'])
        name_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setWordWrap(True)

        # Description
        desc_label = QLabel(self.tool_metadata['description'])
        desc_label.setFont(QFont("Segoe UI", 9))
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #7f8c8d;")

        # Category badge
        category_label = QLabel(self.tool_metadata['category'])
        category_label.setFont(QFont("Segoe UI", 8))
        category_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        category_label.setStyleSheet("""
            QLabel {
                background-color: #3498db;
                color: white;
                padding: 4px 8px;
                border-radius: 10px;
            }
        """)

        layout.addWidget(icon_label)
        layout.addWidget(name_label)
        layout.addWidget(desc_label)
        layout.addStretch()
        layout.addWidget(category_label)

        self.setStyleSheet("""
            ToolCard {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 12px;
            }
            ToolCard:hover {
                border: 2px solid #3498db;
                background-color: #f8f9fa;
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 30))
        self.setGraphicsEffect(shadow)

        self.setFixedSize(220, 240)

    def mousePressEvent(self, event):
        """Handle mouse click"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.tool_metadata['id'])
        super().mousePressEvent(event)


class OmniToolLauncher(QMainWindow):
    """Main launcher application"""

    def __init__(self):
        super().__init__()
        self.app_manager = AppManager()
        self.current_category = None
        self.current_search = ""
        self.open_tool_windows = []

        self.init_ui()
        self.apply_theme()
        self.refresh_tools()

    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("OmniTool - Your Swiss Army Knife for Everything")
        self.setMinimumSize(1100, 700)
        self.resize(1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.create_header(main_layout)

        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        self.create_sidebar(content_layout)
        self.create_main_content(content_layout)

        main_layout.addWidget(content_widget)
        self.create_footer(main_layout)

    def create_header(self, parent_layout):
        """Create header"""
        header = QWidget()
        header.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
            }
        """)
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(30, 20, 30, 20)
        header_layout.setSpacing(15)

        title = QLabel("🛠️ OmniTool")
        title.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")

        subtitle = QLabel("Your All-in-One Toolkit")
        subtitle.setFont(QFont("Segoe UI", 14))
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.9);")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search tools... (e.g., 'youtube', 'pdf', 'calculator')")
        self.search_input.setFont(QFont("Segoe UI", 11))
        self.search_input.setMinimumHeight(45)
        self.search_input.textChanged.connect(self.on_search)
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.95);
                border: none;
                border-radius: 22px;
                padding: 12px 20px;
                color: #2c3e50;
            }
            QLineEdit:focus {
                background-color: white;
            }
        """)

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header_layout.addWidget(self.search_input)
        parent_layout.addWidget(header)

    def create_sidebar(self, parent_layout):
        """Create sidebar with categories"""
        sidebar = QWidget()
        sidebar.setMaximumWidth(250)
        sidebar.setStyleSheet("QWidget { background-color: #f8f9fa; border-radius: 10px; }")

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(15, 15, 15, 15)
        sidebar_layout.setSpacing(10)

        cat_title = QLabel("📂 Categories")
        cat_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        cat_title.setStyleSheet("color: #2c3e50;")
        sidebar_layout.addWidget(cat_title)

        self.category_group = QButtonGroup()

        all_btn = QRadioButton("All Tools")
        all_btn.setFont(QFont("Segoe UI", 10))
        all_btn.setChecked(True)
        all_btn.toggled.connect(lambda checked: self.filter_by_category(None) if checked else None)
        self.category_group.addButton(all_btn)
        sidebar_layout.addWidget(all_btn)

        categories_count = self.app_manager.get_categories_with_count()

        for category, count in categories_count.items():
            btn = QRadioButton(f"{category} ({count})")
            btn.setFont(QFont("Segoe UI", 10))
            btn.toggled.connect(
                lambda checked, cat=category: self.filter_by_category(cat) if checked else None
            )
            self.category_group.addButton(btn)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        stats_frame = QFrame()
        stats_frame.setStyleSheet("QFrame { background-color: white; border-radius: 8px; padding: 10px; }")
        stats_layout = QVBoxLayout(stats_frame)

        total_tools = len(self.app_manager.get_all_tools())
        stats_label = QLabel(f"📊 Total Tools: {total_tools}")
        stats_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        stats_label.setStyleSheet("color: #3498db;")

        stats_layout.addWidget(stats_label)
        sidebar_layout.addWidget(stats_frame)
        parent_layout.addWidget(sidebar)

    def create_main_content(self, parent_layout):
        """Create main content area"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(20)

        self.results_label = QLabel()
        self.results_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.results_label.setStyleSheet("color: #2c3e50;")
        self.content_layout.addWidget(self.results_label)

        self.tools_container = QWidget()
        self.tools_grid = QGridLayout(self.tools_container)
        self.tools_grid.setSpacing(20)
        self.tools_grid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.content_layout.addWidget(self.tools_container)
        self.content_layout.addStretch()

        scroll.setWidget(self.content_widget)
        parent_layout.addWidget(scroll)

    def create_footer(self, parent_layout):
        """Create footer"""
        footer = QWidget()
        footer.setStyleSheet("QWidget { background-color: #2c3e50; padding: 15px; }")
        footer.setMaximumHeight(60)

        footer_layout = QHBoxLayout(footer)
        footer_text = QLabel("OmniTool v1.0 | All you need in one place.")
        footer_text.setFont(QFont("Segoe UI", 9))
        footer_text.setStyleSheet("color: white;")

        footer_layout.addWidget(footer_text)
        footer_layout.addStretch()
        parent_layout.addWidget(footer)

    def refresh_tools(self):
        """Refresh tools display"""
        while self.tools_grid.count():
            item = self.tools_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if self.current_search:
            tools = self.app_manager.search_tools(self.current_search)
            self.results_label.setText(f"🔍 Search results for '{self.current_search}' ({len(tools)} found)")
        elif self.current_category:
            tools = self.app_manager.get_tools_by_category(self.current_category)
            self.results_label.setText(f"📁 {self.current_category} ({len(tools)} tools)")
        else:
            tools = self.app_manager.get_all_tools()
            self.results_label.setText(f"🛠️ All Tools ({len(tools)} available)")

        if tools:
            row, col = 0, 0
            max_cols = 4

            for tool in tools:
                card = ToolCard(tool)
                card.clicked.connect(self.launch_tool)
                self.tools_grid.addWidget(card, row, col)

                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1
        else:
            no_results = QLabel("😕 No tools found matching your search")
            no_results.setFont(QFont("Segoe UI", 14))
            no_results.setStyleSheet("color: #95a5a6; padding: 40px;")
            no_results.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tools_grid.addWidget(no_results, 0, 0)

    def on_search(self, text):
        """Handle search"""
        self.current_search = text.strip()
        self.refresh_tools()

    def filter_by_category(self, category):
        """Filter by category"""
        self.current_category = category
        self.current_search = ""
        self.search_input.clear()
        self.refresh_tools()

    def launch_tool(self, tool_id):
        """Launch a tool"""
        try:
            window = self.app_manager.launch_tool(tool_id)
            if window:
                self.open_tool_windows.append(window)
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            import traceback
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to launch tool:\n{str(e)}\n\n{traceback.format_exc()}"
            )

    def apply_theme(self):
        """Apply theme"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ecf0f1;
            }
            QRadioButton {
                padding: 8px;
                color: #2c3e50;
            }
            QRadioButton:hover {
                background-color: rgba(52, 152, 219, 0.1);
                border-radius: 4px;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
            }
            QRadioButton::indicator:checked {
                background-color: #3498db;
                border: 2px solid #3498db;
                border-radius: 8px;
            }
            QRadioButton::indicator:unchecked {
                background-color: white;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
            }
        """)


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    launcher = OmniToolLauncher()
    launcher.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

