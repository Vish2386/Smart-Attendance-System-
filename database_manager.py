import sqlite3
import threading
from datetime import datetime, date, timedelta
from config import DATABASE_CONFIG, ERROR_MESSAGES, SUCCESS_MESSAGES

class DatabaseManager:
    """
    Database Manager for Smart Attendance System
    Handles all database operations with thread safety
    """
    
    def __init__(self, db_path="attendance_system.db"):
        """
        Initialize database manager
        
        Args:
            db_path (str): Path to the database file
        """
        self.db_path = db_path
        self.lock = threading.Lock()
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create students table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    student_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT,
                    phone TEXT,
                    department TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create attendance table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT NOT NULL,
                    date DATE NOT NULL,
                    time_in TIMESTAMP,
                    time_out TIMESTAMP,
                    verification_method TEXT NOT NULL,
                    course_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES students (student_id),
                    UNIQUE(student_id, date)
                )
            ''')
            
            # Create courses table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS courses (
                    course_id TEXT PRIMARY KEY,
                    course_name TEXT NOT NULL,
                    instructor TEXT,
                    schedule TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create course_attendance table for detailed course tracking
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS course_attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT NOT NULL,
                    course_id TEXT NOT NULL,
                    date DATE NOT NULL,
                    time_in TIMESTAMP,
                    time_out TIMESTAMP,
                    verification_method TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES students (student_id),
                    FOREIGN KEY (course_id) REFERENCES courses (course_id),
                    UNIQUE(student_id, course_id, date)
                )
            ''')
            
            conn.commit()
            conn.close()
    
    def add_student(self, student_id, name, email="", phone="", department=""):
        """
        Add a new student to the database
        
        Args:
            student_id (str): Unique student identifier
            name (str): Student's full name
            email (str): Student's email address
            phone (str): Student's phone number
            department (str): Student's department
            
        Returns:
            bool: True if successful, False otherwise
        """
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO students (student_id, name, email, phone, department)
                    VALUES (?, ?, ?, ?, ?)
                ''', (student_id, name, email, phone, department))
                
                conn.commit()
                conn.close()
                return True
                
            except sqlite3.IntegrityError:
                # Student ID already exists
                return False
            except Exception as e:
                print(f"Error adding student: {e}")
                return False
    
    def get_student(self, student_id):
        """
        Get student information by ID
        
        Args:
            student_id (str): Student ID
            
        Returns:
            tuple: Student data (id, name, email, phone, department, created_at)
                  or None if not found
        """
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT student_id, name, email, phone, department, created_at
                    FROM students 
                    WHERE student_id = ?
                ''', (student_id,))
                
                result = cursor.fetchone()
                conn.close()
                return result
                
            except Exception as e:
                print(f"Error getting student: {e}")
                return None
    
    def get_all_students(self):
        """
        Get all students from database
        
        Returns:
            list: List of student tuples
        """
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT student_id, name, email, phone, department, created_at
                    FROM students 
                    ORDER BY name
                ''')
                
                results = cursor.fetchall()
                conn.close()
                return results
                
            except Exception as e:
                print(f"Error getting all students: {e}")
                return []
    
    def record_attendance(self, student_id, verification_method="id_pass", course_id=None):
        """
        Record student attendance
        
        Args:
            student_id (str): Student ID
            verification_method (str): Method used for verification (id_pass)
            course_id (str): Optional course ID
            
        Returns:
            bool: True if attendance recorded, False if already recorded today
        """
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                today = date.today()
                current_time = datetime.now()
                
                # Check if attendance already recorded for today
                cursor.execute('''
                    SELECT id FROM attendance 
                    WHERE student_id = ? AND date = ?
                ''', (student_id, today))
                
                existing_record = cursor.fetchone()
                
                if existing_record:
                    # Update time_out for existing record
                    cursor.execute('''
                        UPDATE attendance 
                        SET time_out = ?
                        WHERE id = ?
                    ''', (current_time, existing_record[0]))
                    
                    # Also update course attendance if course_id provided
                    if course_id:
                        cursor.execute('''
                            UPDATE course_attendance 
                            SET time_out = ?
                            WHERE student_id = ? AND course_id = ? AND date = ?
                        ''', (current_time, student_id, course_id, today))
                    
                    conn.commit()
                    conn.close()
                    return False  # Already recorded today
                
                else:
                    # Create new attendance record
                    cursor.execute('''
                        INSERT INTO attendance (student_id, date, time_in, verification_method, course_id)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (student_id, today, current_time, verification_method, course_id))
                    
                    # Also create course attendance record if course_id provided
                    if course_id:
                        cursor.execute('''
                            INSERT INTO course_attendance (student_id, course_id, date, time_in, verification_method)
                            VALUES (?, ?, ?, ?, ?)
                        ''', (student_id, course_id, today, current_time, verification_method))
                    
                    conn.commit()
                    conn.close()
                    return True
                
            except Exception as e:
                print(f"Error recording attendance: {e}")
                return False
    
    def get_attendance_report(self, start_date=None, end_date=None, student_id=None, course_id=None):
        """
        Get attendance report with filters
        
        Args:
            start_date (date): Start date for report
            end_date (date): End date for report
            student_id (str): Filter by specific student
            course_id (str): Filter by specific course
            
        Returns:
            list: List of attendance records
        """
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                # Build query
                query = '''
                    SELECT 
                        a.time_in,
                        a.student_id,
                        s.name,
                        a.date,
                        a.verification_method,
                        c.course_name
                    FROM attendance a
                    JOIN students s ON a.student_id = s.student_id
                    LEFT JOIN courses c ON a.course_id = c.course_id
                    WHERE 1=1
                '''
                
                params = []
                
                if start_date:
                    query += " AND a.date >= ?"
                    params.append(start_date)
                
                if end_date:
                    query += " AND a.date <= ?"
                    params.append(end_date)
                
                if student_id:
                    query += " AND a.student_id = ?"
                    params.append(student_id)
                
                if course_id:
                    query += " AND a.course_id = ?"
                    params.append(course_id)
                
                query += " ORDER BY a.time_in DESC"
                
                cursor.execute(query, params)
                results = cursor.fetchall()
                conn.close()
                return results
                
            except Exception as e:
                print(f"Error getting attendance report: {e}")
                return []
    
    def add_course(self, course_id, course_name, instructor="", schedule=""):
        """
        Add a new course to the database
        
        Args:
            course_id (str): Unique course identifier
            course_name (str): Course name
            instructor (str): Instructor name
            schedule (str): Course schedule
            
        Returns:
            bool: True if successful, False otherwise
        """
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO courses (course_id, course_name, instructor, schedule)
                    VALUES (?, ?, ?, ?)
                ''', (course_id, course_name, instructor, schedule))
                
                conn.commit()
                conn.close()
                return True
                
            except sqlite3.IntegrityError:
                # Course ID already exists
                return False
            except Exception as e:
                print(f"Error adding course: {e}")
                return False
    
    def get_all_courses(self):
        """
        Get all courses from database
        
        Returns:
            list: List of course tuples
        """
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT course_id, course_name, instructor, schedule, created_at
                    FROM courses 
                    ORDER BY course_name
                ''')
                
                results = cursor.fetchall()
                conn.close()
                return results
                
            except Exception as e:
                print(f"Error getting all courses: {e}")
                return []
    
    def delete_student(self, student_id):
        """
        Delete a student and all associated attendance records
        
        Args:
            student_id (str): Student ID to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                # Delete attendance records first (due to foreign key constraint)
                cursor.execute('DELETE FROM attendance WHERE student_id = ?', (student_id,))
                cursor.execute('DELETE FROM course_attendance WHERE student_id = ?', (student_id,))
                
                # Delete student
                cursor.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
                
                conn.commit()
                conn.close()
                return True
                
            except Exception as e:
                print(f"Error deleting student: {e}")
                return False
    
    def delete_course(self, course_id):
        """
        Delete a course and all associated attendance records
        
        Args:
            course_id (str): Course ID to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                # Delete course attendance records first (due to foreign key constraint)
                cursor.execute('DELETE FROM course_attendance WHERE course_id = ?', (course_id,))
                
                # Update attendance records to remove course_id reference
                cursor.execute('UPDATE attendance SET course_id = NULL WHERE course_id = ?', (course_id,))
                
                # Delete course
                cursor.execute('DELETE FROM courses WHERE course_id = ?', (course_id,))
                
                conn.commit()
                conn.close()
                return True
                
            except Exception as e:
                print(f"Error deleting course: {e}")
                return False
    
    def get_student_statistics(self, student_id):
        """
        Get attendance statistics for a specific student
        
        Args:
            student_id (str): Student ID
            
        Returns:
            dict: Statistics including total attendance, attendance rate, etc.
        """
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                # Get total attendance days
                cursor.execute('''
                    SELECT COUNT(*) FROM attendance 
                    WHERE student_id = ?
                ''', (student_id,))
                total_attendance = cursor.fetchone()[0]
                
                # Get attendance by method
                cursor.execute('''
                    SELECT verification_method, COUNT(*) 
                    FROM attendance 
                    WHERE student_id = ?
                    GROUP BY verification_method
                ''', (student_id,))
                method_stats = dict(cursor.fetchall())
                
                # Get recent attendance (last 30 days)
                thirty_days_ago = date.today() - timedelta(days=30)
                cursor.execute('''
                    SELECT COUNT(*) FROM attendance 
                    WHERE student_id = ? AND date >= ?
                ''', (student_id, thirty_days_ago))
                recent_attendance = cursor.fetchone()[0]
                
                conn.close()
                
                return {
                    'total_attendance': total_attendance,
                    'recent_attendance': recent_attendance,
                    'method_stats': method_stats
                }
                
            except Exception as e:
                print(f"Error getting student statistics: {e}")
                return {}
    
    def backup_database(self, backup_path):
        """
        Create a backup of the database
        
        Args:
            backup_path (str): Path for backup file
            
        Returns:
            bool: True if successful, False otherwise
        """
        with self.lock:
            try:
                import shutil
                shutil.copy2(self.db_path, backup_path)
                return True
            except Exception as e:
                print(f"Error backing up database: {e}")
                return False
    
    def restore_database(self, backup_path):
        """
        Restore database from backup
        
        Args:
            backup_path (str): Path to backup file
            
        Returns:
            bool: True if successful, False otherwise
        """
        with self.lock:
            try:
                import shutil
                shutil.copy2(backup_path, self.db_path)
                return True
            except Exception as e:
                print(f"Error restoring database: {e}")
                return False
    
    def close(self):
        """Close database connection"""
        # SQLite connections are automatically closed when the object goes out of scope
        # This method is provided for explicit cleanup if needed
        pass

