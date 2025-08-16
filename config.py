"""
Configuration file for Smart Attendance System
Contains all system settings and parameters
"""

import os

# Database Configuration
DATABASE_CONFIG = {
    'default_path': 'attendance_system.db',
    'backup_path': 'backup/',
    'max_connections': 10,
    'timeout': 30
}

# GUI Configuration
GUI_CONFIG = {
    'window_width': 1200,
    'window_height': 800,
    'theme': 'clam',
    'refresh_rate': 1000,  # Status refresh rate in milliseconds
    'max_students_display': 100,
    'max_attendance_display': 50,
    'background_color': '#FFFFFF',  # Pure White
    'primary_color': '#1E3A8A',     # Deep Blue
    'secondary_color': '#3B82F6',   # Bright Blue
    'accent_color': '#F59E0B',      # Gold
    'success_color': '#10B981',     # Green
    'error_color': '#EF4444',       # Red
    'warning_color': '#F59E0B',     # Gold
    'text_color': '#1F2937',        # Dark Gray
    'light_text_color': '#6B7280',  # Light Gray
    'border_color': '#E5E7EB',      # Light Gray Border
    'card_background': '#F8FAFC',   # Very Light Blue-Gray
    'font_family': 'Segoe UI',
    'font_size': 10,
    'title_font_size': 18,
    'header_font_size': 14,
    'button_padding': 10,
    'card_padding': 20,
    'border_radius': 8
}

# Attendance Configuration
ATTENDANCE_CONFIG = {
    'auto_timeout': 300,  # Auto-logout after 5 minutes of inactivity
    'late_threshold': 15,  # Minutes after class start to mark as late
    'absent_threshold': 30,  # Minutes after class start to mark as absent
    'allow_duplicate_checkin': False,
    'require_verification': True,
    'default_verification_method': 'id_pass'
}

# Reporting Configuration
REPORT_CONFIG = {
    'default_date_format': '%Y-%m-%d',
    'default_time_format': '%H:%M:%S',
    'export_formats': ['csv', 'xlsx', 'pdf'],
    'max_report_rows': 10000,
    'auto_backup_reports': True
}

# Security Configuration
SECURITY_CONFIG = {
    'encrypt_biometric_data': False,
    'hash_passwords': True,
    'session_timeout': 3600,  # 1 hour
    'max_login_attempts': 3,
    'require_admin_for_deletion': True
}

# Logging Configuration
LOGGING_CONFIG = {
    'log_level': 'INFO',
    'log_file': 'attendance_system.log',
    'max_log_size': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5,
    'log_format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
}

# Notification Configuration
NOTIFICATION_CONFIG = {
    'enable_email_notifications': False,
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email_username': '',
    'email_password': '',
    'notification_recipients': [],
    'attendance_alerts': True,
    'system_alerts': True
}

# Backup Configuration
BACKUP_CONFIG = {
    'auto_backup': True,
    'backup_interval': 24 * 60 * 60,  # 24 hours in seconds
    'backup_retention_days': 30,
    'backup_path': 'backups/',
    'include_attachments': True
}

# Performance Configuration
PERFORMANCE_CONFIG = {
    'max_threads': 4,
    'cache_size': 1000,
    'database_pool_size': 5,
    'enable_caching': True
}

# Development Configuration
DEVELOPMENT_CONFIG = {
    'debug_mode': False,
    'mock_hardware': False,
    'test_mode': False,
    'verbose_logging': False,
    'auto_save_interval': 60  # seconds
}

# File Paths
PATHS = {
    'base_dir': os.path.dirname(os.path.abspath(__file__)),
    'data_dir': 'data/',
    'logs_dir': 'logs/',
    'backups_dir': 'backups/',
    'exports_dir': 'exports/',
    'temp_dir': 'temp/',
    'config_dir': 'config/'
}

# Create necessary directories
def create_directories():
    """Create necessary directories if they don't exist"""
    for path_name, path_value in PATHS.items():
        if path_name != 'base_dir':
            full_path = os.path.join(PATHS['base_dir'], path_value)
            if not os.path.exists(full_path):
                os.makedirs(full_path)
                print(f"Created directory: {full_path}")

# System Information
SYSTEM_INFO = {
    'name': 'Smart Attendance System',
    'version': '2.0.0',
    'author': 'Your Name',
    'description': 'A comprehensive attendance system using ID Pass Authentication',
    'license': 'MIT',
    'python_version': '3.7+'
}

# Default Values
DEFAULTS = {
    'student_id_format': 'S{year}{sequence:03d}',
    'course_id_format': 'C{year}{sequence:03d}',
    'default_department': 'General',
    'default_course_duration': 60,  # minutes
    'default_attendance_status': 'present',
    'verification_method': 'id_pass'
}

# Validation Rules
VALIDATION_RULES = {
    'student_id': {
        'min_length': 3,
        'max_length': 20,
        'pattern': r'^[A-Z0-9_-]+$'
    },
    'student_name': {
        'min_length': 2,
        'max_length': 100,
        'pattern': r'^[A-Za-z\s\-\.]+$'
    },
    'email': {
        'pattern': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    },
    'phone': {
        'pattern': r'^[\+]?[1-9][\d]{0,15}$'
    }
}

# Error Messages
ERROR_MESSAGES = {
    'database_connection': 'Failed to connect to database',
    'student_not_found': 'Student not found in database',
    'invalid_student_id': 'Invalid student ID format',
    'attendance_already_recorded': 'Attendance already recorded for today',
    'verification_failed': 'ID verification failed',
    'permission_denied': 'Permission denied for this operation'
}

# Success Messages
SUCCESS_MESSAGES = {
    'student_added': 'Student added successfully',
    'attendance_recorded': 'Attendance recorded successfully',
    'report_generated': 'Report generated successfully',
    'backup_created': 'Backup created successfully',
    'system_updated': 'System updated successfully'
}

# Initialize system
def initialize_system():
    """Initialize the system with default configuration"""
    create_directories()
    print("System configuration initialized successfully!")

