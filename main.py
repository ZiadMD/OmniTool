"""
OmniTool - Multi-Tool Application Launcher
Main entry point for the application
"""

import sys
import argparse


def main():
    """Main entry point with argument parsing"""
    parser = argparse.ArgumentParser(
        description='OmniTool - Your All-in-One Toolkit',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python main.py                         # Launch main app with tool selector
  python main.py --tool youtube_downloader  # Launch YouTube Downloader directly
        '''
    )

    parser.add_argument(
        '--tool',
        type=str,
        help='Launch a specific tool directly by ID'
    )

    args = parser.parse_args()

    # Direct tool launch
    if args.tool:
        from core import AppManager
        app_manager = AppManager()

        from PyQt6.QtWidgets import QApplication
        app = QApplication(sys.argv)
        app.setStyle('Fusion')

        print(f"Launching {args.tool}...")
        app_manager.launch_tool(args.tool)
        sys.exit(app.exec())

    else:
        # Launch main app launcher
        from launcher import main as launcher_main
        print("Launching OmniTool Launcher...")
        launcher_main()


if __name__ == "__main__":
    main()
