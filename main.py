#!/usr/bin/env python3
"""
Smart Attendance System - Main Entry Point
ID Pass Authentication System

This module serves as the main entry point for the Smart Attendance System.
It initializes all components and provides a command-line interface for various operations.
"""

import sys
import os
import signal
import argparse
from datetime import datetime

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database_manager import DatabaseManager
from gui_module import AttendanceGUI
from config import SYSTEM_INFO, DEFAULTS

class SmartAttendanceSystem:
    """
    Main system class that orchestrates all components
    """
    
    def __init__(self, db_path="attendance_system.db"):
        """
        Initialize the Smart Attendance System
        
        Args:
            db_path (str): Path to the database file
        """
        print("Initializing Smart Attendance System...")
        print(f"Version: {SYSTEM_INFO['version']}")
        print("Mode: ID Pass Authentication Only")
        
        # Initialize database manager
        self.db_manager = DatabaseManager(db_path)
        print("✓ Database manager initialized")
        
        # Initialize GUI
        self.gui = AttendanceGUI(self.db_manager)
        print("✓ GUI initialized")
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        print("✓ Smart Attendance System initialized successfully!")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"\nReceived signal {signum}, shutting down gracefully...")
        self.cleanup()
        sys.exit(0)
    
    def add_sample_data(self):
        """Add sample students and courses to the database"""
        print("Adding sample data...")
        
        # Add sample courses
        courses = [
            ("CS101", "Introduction to Computer Science", "Dr. Smith", "Mon/Wed 9:00-10:30"),
            ("MATH201", "Calculus II", "Prof. Johnson", "Tue/Thu 11:00-12:30"),
            ("ENG101", "English Composition", "Dr. Williams", "Mon/Wed 14:00-15:30"),
            ("PHYS101", "Physics I", "Prof. Brown", "Tue/Thu 13:00-14:30"),
            ("HIST101", "World History", "Dr. Davis", "Fri 10:00-12:00")
        ]
        
        for course_id, course_name, instructor, schedule in courses:
            try:
                self.db_manager.add_course(course_id, course_name, instructor, schedule)
                print(f"✓ Added course: {course_id} - {course_name}")
            except Exception as e:
                print(f"⚠ Warning: Could not add course {course_id}: {e}")
        
        # Add sample students
        students = [
            ("S001", "John Doe", "john.doe@university.edu", "555-0101", "Computer Science"),
            ("S002", "Jane Smith", "jane.smith@university.edu", "555-0102", "Mathematics"),
            ("S003", "Bob Johnson", "bob.johnson@university.edu", "555-0103", "Engineering"),
            ("S004", "Alice Brown", "alice.brown@university.edu", "555-0104", "Physics"),
            ("S005", "Charlie Wilson", "charlie.wilson@university.edu", "555-0105", "Computer Science"),
            ("S006", "Diana Davis", "diana.davis@university.edu", "555-0106", "Mathematics"),
            ("S007", "Edward Miller", "edward.miller@university.edu", "555-0107", "Engineering"),
            ("S008", "Fiona Garcia", "fiona.garcia@university.edu", "555-0108", "Physics"),
            ("S009", "George Martinez", "george.martinez@university.edu", "555-0109", "Computer Science"),
            ("S010", "Helen Taylor", "helen.taylor@university.edu", "555-0110", "Mathematics")
        ]
        
        for student_id, name, email, phone, department in students:
            try:
                self.db_manager.add_student(student_id, name, email, phone, department)
                print(f"✓ Added student: {student_id} - {name}")
            except Exception as e:
                print(f"⚠ Warning: Could not add student {student_id}: {e}")
        
        print("✓ Sample data added successfully!")
    
    def delete_all_data(self):
        """Delete all data from the database"""
        print("⚠️  WARNING: This will delete ALL data from the database!")
        print("This action cannot be undone.")
        
        try:
            response = input("Are you sure you want to continue? (yes/no): ").lower().strip()
            if response == 'yes':
                print("Deleting all data...")
                
                # Get all students and delete them (this will cascade to attendance records)
                students = self.db_manager.get_all_students()
                for student in students:
                    self.db_manager.delete_student(student[0])
                
                # Get all courses and delete them
                courses = self.db_manager.get_all_courses()
                for course in courses:
                    self.db_manager.delete_course(course[0])
                    print(f"Deleted course: {course[0]} - {course[1]}")
                
                # Clear attendance records
                print("Cleared all attendance records")
                
                print("✓ All data deleted successfully!")
                print("The database structure remains intact for future use.")
            else:
                print("Operation cancelled.")
                
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
        except Exception as e:
            print(f"❌ Error deleting data: {e}")
    
    def run_attendance_demo(self):
        """Run attendance recording demo"""
        print("\n=== Attendance Recording Demo ===")
        
        # Check if we have any students and courses
        students = self.db_manager.get_all_students()
        courses = self.db_manager.get_all_courses()
        
        if not students:
            print("No students found. Please add some students first.")
            return
        
        if not courses:
            print("No courses found. Please add some courses first.")
            return
        
        print(f"Found {len(students)} students and {len(courses)} courses")
        
        # Select first student and course for demo
        student = students[0]
        course = courses[0]
        
        student_id = student[0]
        student_name = student[1]
        course_id = course[0]
        course_name = course[1]
        
        print(f"Demo: Recording attendance for {student_id} - {student_name}")
        print(f"Course: {course_id} - {course_name}")
        
        # Test ID Pass Authentication
        print("\n1. Testing ID Pass Authentication...")
        try:
            result = self.db_manager.record_attendance(
                student_id, verification_method="id_pass", course_id=course_id
            )
            if result:
                print("✓ ID Pass Authentication successful!")
            else:
                print("⚠ Attendance already recorded for today")
        except Exception as e:
            print(f"✗ ID Pass Authentication error: {e}")
        
        # Show today's attendance
        print("\n2. Today's attendance records:")
        try:
            today = datetime.now().date()
            attendance_records = self.db_manager.get_attendance_report(
                start_date=today, end_date=today
            )
            
            if attendance_records:
                for record in attendance_records:
                    print(f"  • {record[0]} - {record[1]} ({record[2]}) - {record[4]}")
            else:
                print("  No attendance records for today")
        except Exception as e:
            print(f"✗ Error retrieving attendance: {e}")
        
        print("\n=== Demo completed ===")
    
    def run_system_test(self):
        """Run comprehensive system test"""
        print("\n=== System Test ===")
        
        # Test database operations
        print("1. Testing database operations...")
        try:
            # Test adding a test student
            test_student_id = "TEST001"
            self.db_manager.add_student(test_student_id, "Test Student", "test@test.com", "555-0000", "Test Dept")
            print("✓ Database add student: PASS")
            
            # Test retrieving student
            student = self.db_manager.get_student(test_student_id)
            if student:
                print("✓ Database get student: PASS")
            else:
                print("✗ Database get student: FAIL")
            
            # Test adding a test course
            test_course_id = "TEST101"
            self.db_manager.add_course(test_course_id, "Test Course", "Test Instructor", "Test Schedule")
            print("✓ Database add course: PASS")
            
            # Test attendance recording
            result = self.db_manager.record_attendance(test_student_id, "id_pass", test_course_id)
            if result:
                print("✓ Database record attendance: PASS")
            else:
                print("⚠ Database record attendance: Already recorded")
            
            # Clean up test data
            self.db_manager.delete_student(test_student_id)
            print("✓ Database cleanup: PASS")
            
        except Exception as e:
            print(f"✗ Database test failed: {e}")
        
        # Test GUI initialization
        print("\n2. Testing GUI initialization...")
        try:
            # GUI is already initialized in __init__, just test if it's working
            if self.gui and hasattr(self.gui, 'root'):
                print("✓ GUI initialization: PASS")
            else:
                print("✗ GUI initialization: FAIL")
        except Exception as e:
            print(f"✗ GUI test failed: {e}")
        
        print("\n=== System test completed ===")
    
    def show_help(self):
        """Show command-line help"""
        help_text = """
Smart Attendance System - Command Line Interface

Usage: python main.py [command] [options]

Commands:
    gui                 Launch the graphical user interface
    demo-attendance     Run attendance recording demo
    test               Run comprehensive system test
    add-sample-data    Add sample students and courses to database
    delete-data        Delete all data from database (⚠️ DANGEROUS)
    help               Show this help message

Options:
    --db-path PATH     Specify custom database path (default: attendance_system.db)

Examples:
    python main.py gui
    python main.py demo-attendance
    python main.py test
    python main.py add-sample-data
    python main.py delete-data

For more information, see the README.md file.
"""
        print(help_text)
    
    def run(self, command=None):
        """
        Run the specified command
        
        Args:
            command (str): Command to execute
        """
        if command == "gui":
            print("Launching GUI...")
            self.gui.run()
        
        elif command == "demo-attendance":
            self.run_attendance_demo()
        
        elif command == "test":
            self.run_system_test()
        
        elif command == "add-sample-data":
            self.add_sample_data()
        
        elif command == "delete-data":
            self.delete_all_data()
        
        elif command == "help":
            self.show_help()
        
        else:
            print("No command specified. Launching GUI...")
            self.gui.run()
    
    def cleanup(self):
        """Clean up resources"""
        print("Cleaning up resources...")
        
        try:
            if hasattr(self.gui, 'cleanup'):
                self.gui.cleanup()
                print("✓ GUI cleaned up")
        except Exception as e:
            print(f"⚠ Warning: Error cleaning up GUI: {e}")
        
        try:
            if hasattr(self.db_manager, 'close'):
                self.db_manager.close()
                print("✓ Database connection closed")
        except Exception as e:
            print(f"⚠ Warning: Error closing database: {e}")
        
        print("✓ Cleanup completed")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Smart Attendance System - ID Pass Authentication",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py gui                    # Launch GUI
  python main.py demo-attendance       # Run attendance demo
  python main.py test                   # Run system test
  python main.py add-sample-data        # Add sample data
  python main.py delete-data            # Delete all data (⚠️ DANGEROUS)
        """
    )
    
    parser.add_argument(
        'command',
        nargs='?',
        choices=['gui', 'demo-attendance', 'test', 'add-sample-data', 'delete-data', 'help'],
        default='gui',
        help='Command to execute (default: gui)'
    )
    
    parser.add_argument(
        '--db-path',
        default='attendance_system.db',
        help='Path to database file (default: attendance_system.db)'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize system
        system = SmartAttendanceSystem(db_path=args.db_path)
        
        # Run command
        system.run(args.command)
        
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(0)
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

