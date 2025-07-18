#!/usr/bin/env python
"""
Wrapper script to run the Nino Medical AI Demo via Streamlit
"""

import subprocess
import sys
import os

def main():
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(script_dir, "app.py")
    
    # Run streamlit with the app
    try:
        cmd = [sys.executable, "-m", "streamlit", "run", app_path, "--server.port", "8501"]
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Streamlit app: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        sys.exit(0)

if __name__ == "__main__":
    main()
