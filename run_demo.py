#!/usr/bin/env python3
"""
Nino Medical AI Demo - Deployment Script
========================================

This script helps you run the medical AI demo with analytics tracking.
It provides options to run the main app, analytics dashboard, or both.

Usage:
    python run_demo.py --app            # Run main medical AI demo
    python run_demo.py --analytics      # Run analytics dashboard
    python run_demo.py --both           # Run both (recommended for development)
    python run_demo.py --help          # Show this help

Author: Nino Medical AI Team
License: Open Source
"""

import argparse
import subprocess
import sys
import time
import threading
import webbrowser
from pathlib import Path

def run_streamlit_app(script_name, port, open_browser=False):
    """Run a Streamlit app on specified port."""
    try:
        print(f"🚀 Starting {script_name} on port {port}...")
        
        # Build the command
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            script_name,
            "--server.port", str(port),
            "--server.headless", "true" if not open_browser else "false",
            "--browser.gatherUsageStats", "false"
        ]
        
        # Start the process
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Monitor the output
        def monitor_output(proc):
            for line in proc.stdout:
                if "You can now view your Streamlit app" in line:
                    print(f"✅ {script_name} is running at http://localhost:{port}")
                    if open_browser:
                        time.sleep(2)
                        webbrowser.open(f"http://localhost:{port}")
                elif "Stopping..." in line:
                    print(f"🛑 {script_name} stopped")
                elif line.strip():
                    print(f"📝 {script_name}: {line.strip()}")
        
        # Start monitoring in separate thread
        monitor_thread = threading.Thread(target=monitor_output, args=(process,))
        monitor_thread.daemon = True
        monitor_thread.start()
        
        return process
        
    except Exception as e:
        print(f"❌ Error starting {script_name}: {e}")
        return None

def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = {
        'streamlit': 'streamlit',
        'pandas': 'pandas', 
        'numpy': 'numpy', 
        'plotly': 'plotly',
        'sklearn': 'scikit-learn',
        'requests': 'requests'
    }
    
    missing_packages = []
    
    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print(f"📦 Install them with: pip install {' '.join(missing_packages)}")
        return False
    
    return True

def setup_analytics_dir():
    """Ensure analytics directory exists."""
    analytics_dir = Path("analytics")
    analytics_dir.mkdir(exist_ok=True)
    
    # Create initial analytics file if it doesn't exist
    analytics_file = analytics_dir / "usage_data.json"
    if not analytics_file.exists():
        import json
        initial_data = {
            "sessions": [],
            "features": {},
            "notifications": []
        }
        with open(analytics_file, 'w') as f:
            json.dump(initial_data, f, indent=2)
        print("📊 Created initial analytics data file")

def main():
    parser = argparse.ArgumentParser(
        description="Nino Medical AI Demo - Deployment Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_demo.py --app              # Run main medical AI demo
  python run_demo.py --analytics        # Run analytics dashboard  
  python run_demo.py --both             # Run both apps simultaneously
  python run_demo.py --both --browser   # Run both and open browser

For more information, visit: https://github.com/NinoF840/nino-medical-ai-demo
        """
    )
    
    parser.add_argument(
        '--app', action='store_true',
        help='Run the main medical AI demo application'
    )
    
    parser.add_argument(
        '--analytics', action='store_true',
        help='Run the visitor analytics dashboard'
    )
    
    parser.add_argument(
        '--both', action='store_true',
        help='Run both applications simultaneously (recommended)'
    )
    
    parser.add_argument(
        '--browser', action='store_true',
        help='Automatically open browser windows'
    )
    
    parser.add_argument(
        '--port-app', type=int, default=8501,
        help='Port for main application (default: 8501)'
    )
    
    parser.add_argument(
        '--port-analytics', type=int, default=8502,
        help='Port for analytics dashboard (default: 8502)'
    )
    
    args = parser.parse_args()
    
    # Show help if no arguments provided
    if not any([args.app, args.analytics, args.both]):
        parser.print_help()
        return
    
    print("🏥 Nino Medical AI Demo - Deployment Script")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Setup analytics directory
    setup_analytics_dir()
    
    processes = []
    
    try:
        if args.both or args.app:
            print(f"\n🚀 Starting Medical AI Demo on port {args.port_app}...")
            app_process = run_streamlit_app(
                "app.py", 
                args.port_app, 
                open_browser=args.browser
            )
            if app_process:
                processes.append(("Medical AI Demo", app_process))
        
        if args.both or args.analytics:
            print(f"\n📊 Starting Analytics Dashboard on port {args.port_analytics}...")
            analytics_process = run_streamlit_app(
                "visitor_dashboard.py", 
                args.port_analytics,
                open_browser=args.browser and not args.app
            )
            if analytics_process:
                processes.append(("Analytics Dashboard", analytics_process))
        
        if not processes:
            print("❌ No processes started successfully")
            sys.exit(1)
        
        print(f"\n✅ Started {len(processes)} application(s)")
        print("\n📋 Access URLs:")
        
        if args.both or args.app:
            print(f"   🏥 Medical AI Demo:     http://localhost:{args.port_app}")
        
        if args.both or args.analytics:
            print(f"   📊 Analytics Dashboard: http://localhost:{args.port_analytics}")
        
        print("\n💡 Tips:")
        print("   - Use Ctrl+C to stop all applications")
        print("   - Navigate between apps using the buttons in the UI")
        print("   - Analytics data is automatically collected and stored")
        print("   - Check the analytics dashboard to see usage patterns")
        
        # Wait for all processes
        print(f"\n🔄 Running {len(processes)} process(es). Press Ctrl+C to stop...")
        
        while True:
            # Check if any process has terminated
            active_processes = []
            for name, process in processes:
                if process.poll() is None:  # Still running
                    active_processes.append((name, process))
                else:
                    print(f"🛑 {name} has stopped")
            
            processes = active_processes
            
            if not processes:
                print("🏁 All processes have stopped")
                break
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print(f"\n🛑 Stopping {len(processes)} process(es)...")
        
        for name, process in processes:
            try:
                process.terminate()
                print(f"   ✅ Stopped {name}")
            except Exception as e:
                print(f"   ❌ Error stopping {name}: {e}")
        
        print("👋 Goodbye!")
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
