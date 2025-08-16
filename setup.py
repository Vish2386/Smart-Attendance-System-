#!/usr/bin/env python3
"""
Setup Script for Smart Attendance System
ID Pass Authentication System

This script automates the installation and initial configuration of the system.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """Print welcome banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           Smart Attendance System v2.0.0                     ║
║           ID Pass Authentication System                      ║
║                                                              ║
║           Automated Setup Script                             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)

def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required!")
        print(f"   Current version: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} is compatible")
    return True

def install_dependencies():
    """Install Python dependencies from requirements.txt"""
    print("\nInstalling Python dependencies...")
    
    try:
        # Check if requirements.txt exists
        if not os.path.exists("requirements.txt"):
            print("❌ Error: requirements.txt not found!")
            return False
        
        # Install dependencies
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Python dependencies installed successfully!")
            return True
        else:
            print(f"❌ Error installing Python dependencies:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def install_system_dependencies():
    """Install system-specific dependencies"""
    print("\nInstalling system dependencies...")
    
    system = platform.system().lower()
    
    if system == "linux":
        return install_linux_dependencies()
    elif system == "darwin":  # macOS
        return install_macos_dependencies()
    elif system == "windows":
        return install_windows_dependencies()
    else:
        print(f"⚠️  Warning: Unsupported operating system: {system}")
        return True

def install_linux_dependencies():
    """Install Linux system dependencies"""
    print("Installing Linux dependencies...")
    
    try:
        # Update package list
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        
        # Install required packages
        packages = [
            "python3-dev",
            "python3-pip",
            "python3-venv",
            "build-essential",
            "libssl-dev",
            "libffi-dev",
            "pkg-config"
        ]
        
        for package in packages:
            print(f"Installing {package}...")
            subprocess.run(["sudo", "apt-get", "install", "-y", package], check=True)
        
        print("✅ Linux dependencies installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing Linux dependencies: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def install_macos_dependencies():
    """Install macOS system dependencies"""
    print("Installing macOS dependencies...")
    
    try:
        # Check if Homebrew is installed
        result = subprocess.run(["which", "brew"], capture_output=True)
        if result.returncode != 0:
            print("⚠️  Homebrew not found. Installing Homebrew...")
            install_script = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            subprocess.run(install_script, shell=True, check=True)
        
        # Install required packages
        packages = [
            "python3",
            "openssl",
            "pkg-config"
        ]
        
        for package in packages:
            print(f"Installing {package}...")
            subprocess.run(["brew", "install", package], check=True)
        
        print("✅ macOS dependencies installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing macOS dependencies: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def install_windows_dependencies():
    """Install Windows system dependencies"""
    print("Installing Windows dependencies...")
    
    try:
        # Windows typically doesn't need additional system dependencies
        # Most packages are available through pip
        
        # Check if Visual C++ Build Tools are needed
        print("⚠️  Note: If you encounter compilation errors, you may need to install:")
        print("   - Microsoft Visual C++ Build Tools")
        print("   - Windows 10 SDK")
        print("   Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/")
        
        print("✅ Windows dependencies check completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("\nCreating directories...")
    
    directories = [
        "logs",
        "backups", 
        "reports",
        "temp",
        "config"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"ℹ️  Directory already exists: {directory}")

def test_installation():
    """Test the installation"""
    print("\nTesting installation...")
    
    try:
        # Test imports
        print("Testing imports...")
        
        import sqlite3
        print("✅ sqlite3: OK")
        
        import numpy
        print("✅ numpy: OK")
        
        from PIL import Image
        print("✅ Pillow: OK")
        
        # Test database
        print("Testing database...")
        from database_manager import DatabaseManager
        db = DatabaseManager(":memory:")
        db.add_student("TEST001", "Test Student", "test@test.com")
        student = db.get_student("TEST001")
        if student:
            print("✅ Database: OK")
        else:
            print("❌ Database: FAILED")
            return False
        
        print("✅ All tests passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def create_sample_data():
    """Create sample data for testing"""
    print("\nCreating sample data...")
    
    try:
        # Run the main script to add sample data
        result = subprocess.run([
            sys.executable, "main.py", "add-sample-data"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Sample data created successfully!")
            return True
        else:
            print(f"⚠️  Warning: Could not create sample data: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"⚠️  Warning: Could not create sample data: {e}")
        return False

def show_next_steps():
    """Show next steps for the user"""
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETED SUCCESSFULLY!")
    print("="*60)
    
    print("\nNext steps:")
    print("1. Run the system:")
    print("   python main.py gui")
    print()
    print("2. Test the system:")
    print("   python main.py test")
    print()
    print("3. Run demos:")
    print("   python main.py demo-attendance")
    print()
    print("4. View help:")
    print("   python main.py help")
    print()
    print("System features:")
    print("✅ ID Pass Authentication")
    print("✅ Student Management")
    print("✅ Course Management")
    print("✅ Attendance Tracking")
    print("✅ Report Generation")
    print("✅ Database Backup/Restore")
    print()
    print("For more information, see README.md")
    print("="*60)

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install Python dependencies
    if not install_dependencies():
        print("❌ Failed to install Python dependencies!")
        sys.exit(1)
    
    # Install system dependencies
    if not install_system_dependencies():
        print("⚠️  Warning: Some system dependencies may not be installed correctly")
        print("   You can try installing them manually if needed")
    
    # Create directories
    create_directories()
    
    # Test installation
    if not test_installation():
        print("❌ Installation test failed!")
        print("   Please check the error messages above and try again")
        sys.exit(1)
    
    # Ask if user wants sample data
    try:
        response = input("\nWould you like to create sample data for testing? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            create_sample_data()
    except KeyboardInterrupt:
        print("\nSetup interrupted by user")
        sys.exit(0)
    
    # Show next steps
    show_next_steps()

if __name__ == "__main__":
    main()

