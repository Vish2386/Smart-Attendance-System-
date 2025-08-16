#!/usr/bin/env python3
"""
Test Suite for Smart Attendance System
ID Pass Authentication System

This module provides comprehensive testing for all system components.
"""

import unittest
import sys
import os
import tempfile
import shutil
from datetime import datetime, date

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database_manager import DatabaseManager
from config import SYSTEM_INFO, DEFAULTS

class TestSmartAttendanceSystem(unittest.TestCase):
    """Test cases for Smart Attendance System"""
    
    def setUp(self):
        """Set up test environment"""
        # Create temporary database for testing
        self.test_db_path = tempfile.mktemp(suffix='.db')
        self.db_manager = DatabaseManager(self.test_db_path)
    
    def tearDown(self):
        """Clean up test environment"""
        # Remove temporary database
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
    
    def test_database_initialization(self):
        """Test database initialization"""
        # Check if tables were created
        conn = self.db_manager.db_path
        self.assertTrue(os.path.exists(conn))
    
    def test_add_student(self):
        """Test adding a student"""
        # Add a test student
        result = self.db_manager.add_student(
            "TEST001", "Test Student", "test@test.com", "555-0000", "Test Dept"
        )
        self.assertTrue(result)
        
        # Try to add the same student again (should fail)
        result = self.db_manager.add_student(
            "TEST001", "Another Student", "another@test.com", "555-0001", "Another Dept"
        )
        self.assertFalse(result)
    
    def test_get_student(self):
        """Test retrieving student information"""
        # Add a test student
        self.db_manager.add_student(
            "TEST002", "John Doe", "john@test.com", "555-0002", "Computer Science"
        )
        
        # Retrieve student
        student = self.db_manager.get_student("TEST002")
        self.assertIsNotNone(student)
        self.assertEqual(student[0], "TEST002")  # student_id
        self.assertEqual(student[1], "John Doe")  # name
        self.assertEqual(student[2], "john@test.com")  # email
    
    def test_get_all_students(self):
        """Test retrieving all students"""
        # Add multiple students
        students_data = [
            ("S001", "Alice", "alice@test.com", "555-0001", "Math"),
            ("S002", "Bob", "bob@test.com", "555-0002", "Physics"),
            ("S003", "Charlie", "charlie@test.com", "555-0003", "Chemistry")
        ]
        
        for student_id, name, email, phone, dept in students_data:
            self.db_manager.add_student(student_id, name, email, phone, dept)
        
        # Get all students
        students = self.db_manager.get_all_students()
        self.assertEqual(len(students), 3)
        
        # Check if all students are present
        student_ids = [s[0] for s in students]
        self.assertIn("S001", student_ids)
        self.assertIn("S002", student_ids)
        self.assertIn("S003", student_ids)
    
    def test_record_attendance(self):
        """Test recording attendance"""
        # Add a test student
        self.db_manager.add_student("TEST003", "Test Student", "test@test.com")
        
        # Record attendance
        result = self.db_manager.record_attendance("TEST003", "id_pass")
        self.assertTrue(result)
        
        # Try to record attendance again for the same day (should return False)
        result = self.db_manager.record_attendance("TEST003", "id_pass")
        self.assertFalse(result)
    
    def test_attendance_with_course(self):
        """Test recording attendance with course"""
        # Add student and course
        self.db_manager.add_student("TEST004", "Course Student", "course@test.com")
        self.db_manager.add_course("CS101", "Computer Science", "Dr. Smith")
        
        # Record attendance with course
        result = self.db_manager.record_attendance("TEST004", "id_pass", "CS101")
        self.assertTrue(result)
    
    def test_get_attendance_report(self):
        """Test getting attendance report"""
        # Add student and record attendance
        self.db_manager.add_student("TEST005", "Report Student", "report@test.com")
        self.db_manager.record_attendance("TEST005", "id_pass")
        
        # Get today's attendance
        today = date.today()
        report = self.db_manager.get_attendance_report(start_date=today, end_date=today)
        
        self.assertEqual(len(report), 1)
        self.assertEqual(report[0][1], "TEST005")  # student_id
        self.assertEqual(report[0][4], "id_pass")  # verification_method
    
    def test_add_course(self):
        """Test adding a course"""
        result = self.db_manager.add_course(
            "TEST101", "Test Course", "Test Instructor", "Mon/Wed 9:00-10:30"
        )
        self.assertTrue(result)
        
        # Try to add the same course again (should fail)
        result = self.db_manager.add_course(
            "TEST101", "Another Course", "Another Instructor", "Tue/Thu 11:00-12:30"
        )
        self.assertFalse(result)
    
    def test_get_all_courses(self):
        """Test retrieving all courses"""
        # Add multiple courses
        courses_data = [
            ("C001", "Mathematics", "Dr. Math", "Mon/Wed 9:00-10:30"),
            ("C002", "Physics", "Dr. Physics", "Tue/Thu 11:00-12:30"),
            ("C003", "Chemistry", "Dr. Chemistry", "Fri 10:00-12:00")
        ]
        
        for course_id, name, instructor, schedule in courses_data:
            self.db_manager.add_course(course_id, name, instructor, schedule)
        
        # Get all courses
        courses = self.db_manager.get_all_courses()
        self.assertEqual(len(courses), 3)
        
        # Check if all courses are present
        course_ids = [c[0] for c in courses]
        self.assertIn("C001", course_ids)
        self.assertIn("C002", course_ids)
        self.assertIn("C003", course_ids)
    
    def test_delete_student(self):
        """Test deleting a student"""
        # Add a student and record attendance
        self.db_manager.add_student("TEST006", "Delete Student", "delete@test.com")
        self.db_manager.record_attendance("TEST006", "id_pass")
        
        # Delete student
        result = self.db_manager.delete_student("TEST006")
        self.assertTrue(result)
        
        # Verify student is deleted
        student = self.db_manager.get_student("TEST006")
        self.assertIsNone(student)
    
    def test_thread_safety(self):
        """Test database thread safety"""
        import threading
        import time
        
        # Add a test student
        self.db_manager.add_student("THREAD001", "Thread Student", "thread@test.com")
        
        # Create multiple threads that access the database simultaneously
        results = []
        errors = []
        
        def worker(thread_id):
            try:
                # Record attendance
                result = self.db_manager.record_attendance(f"THREAD001", "id_pass")
                results.append((thread_id, result))
                time.sleep(0.1)  # Simulate some work
            except Exception as e:
                errors.append((thread_id, str(e)))
        
        # Start multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Check for errors
        self.assertEqual(len(errors), 0, f"Thread safety errors: {errors}")
        
        # Only one attendance record should be created (the first one)
        today = date.today()
        report = self.db_manager.get_attendance_report(start_date=today, end_date=today)
        self.assertEqual(len(report), 1)
    
    def test_student_statistics(self):
        """Test student statistics"""
        # Add a student and record some attendance
        self.db_manager.add_student("STAT001", "Stats Student", "stats@test.com")
        
        # Record attendance multiple times (different days)
        self.db_manager.record_attendance("STAT001", "id_pass")
        self.db_manager.record_attendance("STAT001", "id_pass")
        
        # Get statistics
        stats = self.db_manager.get_student_statistics("STAT001")
        
        self.assertIn('total_attendance', stats)
        self.assertIn('recent_attendance', stats)
        self.assertIn('method_stats', stats)
        
        self.assertEqual(stats['total_attendance'], 2)
        self.assertIn('id_pass', stats['method_stats'])
    
    def test_database_backup_restore(self):
        """Test database backup and restore"""
        # Add some data
        self.db_manager.add_student("BACKUP001", "Backup Student", "backup@test.com")
        self.db_manager.record_attendance("BACKUP001", "id_pass")
        
        # Create backup
        backup_path = tempfile.mktemp(suffix='.db')
        result = self.db_manager.backup_database(backup_path)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(backup_path))
        
        # Create new database manager and restore
        new_db_path = tempfile.mktemp(suffix='.db')
        new_db_manager = DatabaseManager(new_db_path)
        
        result = new_db_manager.restore_database(backup_path)
        self.assertTrue(result)
        
        # Verify data was restored
        student = new_db_manager.get_student("BACKUP001")
        self.assertIsNotNone(student)
        
        # Clean up
        os.remove(backup_path)
        os.remove(new_db_path)


def run_quick_test():
    """Run a quick system test"""
    print("Running quick system test...")
    
    try:
        # Test database operations
        db_manager = DatabaseManager(":memory:")  # Use in-memory database for testing
        
        # Test adding student
        result = db_manager.add_student("QUICK001", "Quick Test", "quick@test.com")
        print(f"✓ Add student: {'PASS' if result else 'FAIL'}")
        
        # Test getting student
        student = db_manager.get_student("QUICK001")
        print(f"✓ Get student: {'PASS' if student else 'FAIL'}")
        
        # Test recording attendance
        result = db_manager.record_attendance("QUICK001", "id_pass")
        print(f"✓ Record attendance: {'PASS' if result else 'FAIL'}")
        
        print("✓ Quick test completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Quick test failed: {e}")
        return False


def test_hardware_availability():
    """Test hardware availability"""
    print("Testing hardware availability...")
    
    # Test for required packages
    try:
        import numpy
        print("✓ NumPy: Available")
    except ImportError:
        print("✗ NumPy: Not available")
    
    try:
        from PIL import Image
        print("✓ Pillow: Available")
    except ImportError:
        print("✗ Pillow: Not available")
    
    print("✓ Hardware availability test completed!")


if __name__ == "__main__":
    print("Smart Attendance System - Test Suite")
    print(f"Version: {SYSTEM_INFO['version']}")
    print("=" * 50)
    
    # Run quick test
    quick_result = run_quick_test()
    print()
    
    # Test hardware availability
    test_hardware_availability()
    print()
    
    if quick_result:
        # Run full test suite
        print("Running full test suite...")
        unittest.main(verbosity=2)
    else:
        print("Skipping full test suite due to quick test failure.")
        sys.exit(1)

