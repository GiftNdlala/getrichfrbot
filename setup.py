#!/usr/bin/env python3
"""
Setup script for XAUUSD Trading Signal Engine
"""

import subprocess
import sys
import os

def install_requirements():
    """
    Install required packages
    """
    print("Installing required packages...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def create_directories():
    """
    Create necessary directories
    """
    directories = ["data", "charts", "logs"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"📁 Directory already exists: {directory}")

def main():
    """
    Main setup function
    """
    print("=" * 50)
    print("XAUUSD TRADING SIGNAL ENGINE - SETUP")
    print("=" * 50)
    
    # Create directories
    print("\n1. Creating directories...")
    create_directories()
    
    # Install requirements
    print("\n2. Installing requirements...")
    if install_requirements():
        print("\n✅ Setup completed successfully!")
        print("\nYou can now run the engine with:")
        print("  python main.py")
        print("\nOr test it with:")
        print("  python test_engine.py")
    else:
        print("\n❌ Setup failed!")
        print("Please check the error messages above and try again.")

if __name__ == "__main__":
    main()
