import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
from datetime import datetime, date
import os
from config import GUI_CONFIG, ATTENDANCE_CONFIG, SUCCESS_MESSAGES, ERROR_MESSAGES

class AttendanceGUI:
    def __init__(self, database_manager):
        self.database_manager = database_manager
        
        # Initialize main window
        self.root = tk.Tk()
        self.root.title("Smart Attendance System - ID Pass Authentication")
        self.root.geometry(f"{GUI_CONFIG['window_width']}x{GUI_CONFIG['window_height']}")
        self.root.configure(bg=GUI_CONFIG['background_color'])
        
        # Center the window
        self.center_window()
        
        # Setup styles
        self.setup_styles()
        
        # Create main container
        self.create_main_container()
        
        # Status variables
        self.recognition_running = False
        
        # Update status periodically
        self.update_status()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_styles(self):
        """Configure ttk styles for modern appearance"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Main.TFrame', background=GUI_CONFIG['background_color'])
        style.configure('Card.TFrame', background=GUI_CONFIG['card_background'])
        
        # Title styles
        style.configure('Title.TLabel', 
                       font=(GUI_CONFIG['font_family'], GUI_CONFIG['title_font_size'], 'bold'),
                       foreground=GUI_CONFIG['primary_color'],
                       background=GUI_CONFIG['background_color'])
        
        style.configure('Subtitle.TLabel', 
                       font=(GUI_CONFIG['font_family'], GUI_CONFIG['header_font_size']),
                       foreground=GUI_CONFIG['text_color'],
                       background=GUI_CONFIG['background_color'])
        
        # Header styles
        style.configure('Header.TLabel', 
                       font=(GUI_CONFIG['font_family'], GUI_CONFIG['header_font_size'], 'bold'),
                       foreground=GUI_CONFIG['primary_color'],
                       background=GUI_CONFIG['card_background'])
        
        # Status styles
        style.configure('Status.TLabel', 
                       font=(GUI_CONFIG['font_family'], GUI_CONFIG['font_size']),
                       background=GUI_CONFIG['card_background'])
        
        style.configure('Success.TLabel', 
                       foreground=GUI_CONFIG['success_color'],
                       background=GUI_CONFIG['card_background'])
        
        style.configure('Error.TLabel', 
                       foreground=GUI_CONFIG['error_color'],
                       background=GUI_CONFIG['card_background'])
        
        style.configure('Warning.TLabel', 
                       foreground=GUI_CONFIG['warning_color'],
                       background=GUI_CONFIG['card_background'])
        
        # Button styles
        style.configure('Primary.TButton', 
                       font=(GUI_CONFIG['font_family'], GUI_CONFIG['font_size'], 'bold'),
                       background=GUI_CONFIG['primary_color'],
                       foreground='white',
                       padding=(GUI_CONFIG['button_padding'], 8))
        
        style.configure('Secondary.TButton', 
                       font=(GUI_CONFIG['font_family'], GUI_CONFIG['font_size']),
                       background=GUI_CONFIG['secondary_color'],
                       foreground='white',
                       padding=(GUI_CONFIG['button_padding'], 8))
        
        style.configure('Accent.TButton', 
                       font=(GUI_CONFIG['font_family'], GUI_CONFIG['font_size'], 'bold'),
                       background=GUI_CONFIG['accent_color'],
                       foreground='white',
                       padding=(GUI_CONFIG['button_padding'], 8))
        
        # Notebook style
        style.configure('TNotebook', 
                       background=GUI_CONFIG['background_color'],
                       borderwidth=0)
        
        style.configure('TNotebook.Tab', 
                       font=(GUI_CONFIG['font_family'], GUI_CONFIG['font_size']),
                       padding=(20, 10),
                       background=GUI_CONFIG['card_background'])
        
        style.map('TNotebook.Tab',
                 background=[('selected', GUI_CONFIG['primary_color'])],
                 foreground=[('selected', 'white')])
        
    def create_main_container(self):
        """Create the main container with header and notebook"""
        # Main container
        main_frame = ttk.Frame(self.root, style='Main.TFrame')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_frame)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True, pady=(20, 0))
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_student_management_tab()
        self.create_attendance_tab()
        self.create_reports_tab()
        self.create_settings_tab()
        
    def create_header(self, parent):
        """Create the header section"""
        header_frame = ttk.Frame(parent, style='Card.TFrame')
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Title and subtitle
        title_frame = ttk.Frame(header_frame, style='Card.TFrame')
        title_frame.pack(side='left', padx=GUI_CONFIG['card_padding'], pady=GUI_CONFIG['card_padding'])
        
        title_label = ttk.Label(title_frame, text="Smart Attendance System", style='Title.TLabel')
        title_label.pack(anchor='w')
        
        subtitle_label = ttk.Label(title_frame, text="ID Pass Authentication System", style='Subtitle.TLabel')
        subtitle_label.pack(anchor='w')
        
        # Status indicators
        status_frame = ttk.Frame(header_frame, style='Card.TFrame')
        status_frame.pack(side='right', padx=GUI_CONFIG['card_padding'], pady=GUI_CONFIG['card_padding'])
        
        self.db_status_label = ttk.Label(status_frame, text="Database: Checking...", style='Status.TLabel')
        self.db_status_label.pack(anchor='e')
        
    def create_dashboard_tab(self):
        """Create the main dashboard tab"""
        dashboard_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(dashboard_frame, text="📊 Dashboard")
        
        # Welcome section
        welcome_frame = ttk.Frame(dashboard_frame, style='Card.TFrame')
        welcome_frame.pack(fill='x', padx=20, pady=(20, 10))
        
        welcome_label = ttk.Label(welcome_frame, 
                                text="Welcome to Smart Attendance System", 
                                style='Header.TLabel')
        welcome_label.pack(pady=GUI_CONFIG['card_padding'])
        
        # Statistics cards
        stats_frame = ttk.Frame(dashboard_frame, style='Main.TFrame')
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        # Create statistics cards
        self.create_stat_card(stats_frame, "Total Students", "0", 0, 0)
        self.create_stat_card(stats_frame, "Total Courses", "0", 0, 1)
        self.create_stat_card(stats_frame, "Today's Attendance", "0", 0, 2)
        self.create_stat_card(stats_frame, "System Status", "Active", 0, 3)
        
        # Quick actions section
        actions_frame = ttk.Frame(dashboard_frame, style='Card.TFrame')
        actions_frame.pack(fill='x', padx=20, pady=10)
        
        actions_label = ttk.Label(actions_frame, text="Quick Actions", style='Header.TLabel')
        actions_label.pack(pady=(GUI_CONFIG['card_padding'], 10))
        
        # Action buttons
        button_frame = ttk.Frame(actions_frame, style='Card.TFrame')
        button_frame.pack(pady=(0, GUI_CONFIG['card_padding']))
        
        ttk.Button(button_frame, text="📝 Take Attendance", 
                  style='Primary.TButton',
                  command=self.quick_attendance).pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="👥 View Today's Attendance", 
                  style='Secondary.TButton',
                  command=self.quick_view_attendance).pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="➕ Add New Student", 
                  style='Accent.TButton',
                  command=self.quick_add_student).pack(side='left', padx=5)
        
        # Recent activity section
        activity_frame = ttk.Frame(dashboard_frame, style='Card.TFrame')
        activity_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        activity_label = ttk.Label(activity_frame, text="Recent Activity", style='Header.TLabel')
        activity_label.pack(pady=(GUI_CONFIG['card_padding'], 10))
        
        # Activity text widget
        self.activity_text = tk.Text(activity_frame, height=8, width=60, 
                                   font=(GUI_CONFIG['font_family'], GUI_CONFIG['font_size']),
                                   bg=GUI_CONFIG['background_color'],
                                   fg=GUI_CONFIG['text_color'],
                                   relief='flat', borderwidth=0)
        self.activity_text.pack(fill='both', expand=True, padx=GUI_CONFIG['card_padding'], 
                              pady=(0, GUI_CONFIG['card_padding']))
        
        # Scrollbar for activity
        activity_scrollbar = ttk.Scrollbar(activity_frame, orient='vertical', command=self.activity_text.yview)
        activity_scrollbar.pack(side='right', fill='y')
        self.activity_text.configure(yscrollcommand=activity_scrollbar.set)
        
    def create_stat_card(self, parent, title, value, row, col):
        """Create a statistics card"""
        card_frame = ttk.Frame(parent, style='Card.TFrame')
        card_frame.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
        
        title_label = ttk.Label(card_frame, text=title, style='Subtitle.TLabel')
        title_label.pack(pady=(10, 5))
        
        value_label = ttk.Label(card_frame, text=value, style='Title.TLabel')
        value_label.pack(pady=(0, 10))
        
        # Store reference for updating
        if not hasattr(self, 'stat_cards'):
            self.stat_cards = {}
        self.stat_cards[title] = value_label
        
        # Configure grid weights
        parent.grid_columnconfigure(col, weight=1)
        
    def create_student_management_tab(self):
        """Create the student management tab"""
        student_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(student_frame, text="👥 Student Management")
        
        # Left frame for adding students
        left_frame = ttk.Frame(student_frame, style='Main.TFrame')
        left_frame.pack(side='left', fill='both', expand=True, padx=(20, 10), pady=20)
        
        # Add student card
        add_card = ttk.Frame(left_frame, style='Card.TFrame')
        add_card.pack(fill='x', pady=(0, 20))
        
        add_label = ttk.Label(add_card, text="Add New Student", style='Header.TLabel')
        add_label.pack(pady=(GUI_CONFIG['card_padding'], 10))
        
        # Student input fields
        input_frame = ttk.Frame(add_card, style='Card.TFrame')
        input_frame.pack(fill='x', padx=GUI_CONFIG['card_padding'], pady=(0, GUI_CONFIG['card_padding']))
        
        # Student ID
        ttk.Label(input_frame, text="Student ID:", style='Subtitle.TLabel').pack(anchor='w', pady=(0, 5))
        self.student_id_entry = ttk.Entry(input_frame, width=30, font=(GUI_CONFIG['font_family'], GUI_CONFIG['font_size']))
        self.student_id_entry.pack(fill='x', pady=(0, 10))
        
        # Name
        ttk.Label(input_frame, text="Name:", style='Subtitle.TLabel').pack(anchor='w', pady=(0, 5))
        self.name_entry = ttk.Entry(input_frame, width=30, font=(GUI_CONFIG['font_family'], GUI_CONFIG['font_size']))
        self.name_entry.pack(fill='x', pady=(0, 10))
        
        # Email
        ttk.Label(input_frame, text="Email:", style='Subtitle.TLabel').pack(anchor='w', pady=(0, 5))
        self.email_entry = ttk.Entry(input_frame, width=30, font=(GUI_CONFIG['font_family'], GUI_CONFIG['font_size']))
        self.email_entry.pack(fill='x', pady=(0, 10))
        
        # Phone
        ttk.Label(input_frame, text="Phone:", style='Subtitle.TLabel').pack(anchor='w', pady=(0, 5))
        self.phone_entry = ttk.Entry(input_frame, width=30, font=(GUI_CONFIG['font_family'], GUI_CONFIG['font_size']))
        self.phone_entry.pack(fill='x', pady=(0, 10))
        
        # Department
        ttk.Label(input_frame, text="Department:", style='Subtitle.TLabel').pack(anchor='w', pady=(0, 5))
        self.department_entry = ttk.Entry(input_frame, width=30, font=(GUI_CONFIG['font_family'], GUI_CONFIG['font_size']))
        self.department_entry.pack(fill='x', pady=(0, 15))
        
        # Add button
        ttk.Button(input_frame, text="Add Student", 
                  style='Primary.TButton',
                  command=self.add_student).pack(fill='x')
        
        # Right frame for viewing students
        right_frame = ttk.Frame(student_frame, style='Main.TFrame')
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 20), pady=20)
        
        # Students list card
        list_card = ttk.Frame(right_frame, style='Card.TFrame')
        list_card.pack(fill='both', expand=True)
        
        list_label = ttk.Label(list_card, text="Registered Students", style='Header.TLabel')
        list_label.pack(pady=(GUI_CONFIG['card_padding'], 10))
        
        # Student list
        list_frame = ttk.Frame(list_card, style='Card.TFrame')
        list_frame.pack(fill='both', expand=True, padx=GUI_CONFIG['card_padding'], 
                       pady=(0, GUI_CONFIG['card_padding']))
        
        self.student_tree = ttk.Treeview(list_frame, columns=('ID', 'Name', 'Email', 'Phone', 'Department'), 
                                       show='headings', height=15)
        self.student_tree.heading('ID', text='Student ID')
        self.student_tree.heading('Name', text='Name')
        self.student_tree.heading('Email', text='Email')
        self.student_tree.heading('Phone', text='Phone')
        self.student_tree.heading('Department', text='Department')
        
        self.student_tree.column('ID', width=100)
        self.student_tree.column('Name', width=150)
        self.student_tree.column('Email', width=200)
        self.student_tree.column('Phone', width=120)
        self.student_tree.column('Department', width=120)
        
        self.student_tree.pack(side='left', fill='both', expand=True)
        
        # Scrollbar for student list
        student_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.student_tree.yview)
        student_scrollbar.pack(side='right', fill='y')
        self.student_tree.configure(yscrollcommand=student_scrollbar.set)
        
        # Refresh button
        ttk.Button(list_card, text="🔄 Refresh List", 
                  style='Secondary.TButton',
                  command=self.refresh_student_list).pack(pady=10)
        
    def create_attendance_tab(self):
        """Create the attendance tab with ID Pass Authentication"""
        attendance_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(attendance_frame, text="📝 Attendance")
        
        # Course selection card
        course_card = ttk.Frame(attendance_frame, style='Card.TFrame')
        course_card.pack(fill='x', padx=20, pady=(20, 10))
        
        course_label = ttk.Label(course_card, text="Course Selection", style='Header.TLabel')
        course_label.pack(pady=(GUI_CONFIG['card_padding'], 10))
        
        course_frame = ttk.Frame(course_card, style='Card.TFrame')
        course_frame.pack(fill='x', padx=GUI_CONFIG['card_padding'], pady=(0, GUI_CONFIG['card_padding']))
        
        ttk.Label(course_frame, text="Select Course:", style='Subtitle.TLabel').pack(side='left')
        self.course_var = tk.StringVar()
        self.course_combo = ttk.Combobox(course_frame, textvariable=self.course_var, width=30,
                                       font=(GUI_CONFIG['font_family'], GUI_CONFIG['font_size']))
        self.course_combo.pack(side='left', padx=10)
        
        ttk.Button(course_frame, text="🔄 Refresh Courses", 
                  style='Secondary.TButton',
                  command=self.refresh_courses).pack(side='left', padx=10)
        
        # ID Pass Authentication card
        auth_card = ttk.Frame(attendance_frame, style='Card.TFrame')
        auth_card.pack(fill='x', padx=20, pady=10)
        
        auth_label = ttk.Label(auth_card, text="ID Pass Authentication", style='Header.TLabel')
        auth_label.pack(pady=(GUI_CONFIG['card_padding'], 10))
        
        auth_frame = ttk.Frame(auth_card, style='Card.TFrame')
        auth_frame.pack(fill='x', padx=GUI_CONFIG['card_padding'], pady=(0, GUI_CONFIG['card_padding']))
        
        ttk.Label(auth_frame, text="Enter Student ID:", style='Subtitle.TLabel').pack(anchor='w', pady=(0, 10))
        self.attendance_id_entry = ttk.Entry(auth_frame, width=30, 
                                           font=(GUI_CONFIG['font_family'], 14))
        self.attendance_id_entry.pack(fill='x', pady=(0, 15))
        
        # Authentication button
        ttk.Button(auth_frame, text="✅ Verify ID & Record Attendance", 
                  style='Primary.TButton',
                  command=self.verify_id_attendance).pack(fill='x')
        
        # Status display
        self.attendance_status_label = ttk.Label(auth_frame, text="", style='Status.TLabel')
        self.attendance_status_label.pack(pady=10)
        
        # Today's attendance card
        today_card = ttk.Frame(attendance_frame, style='Card.TFrame')
        today_card.pack(fill='both', expand=True, padx=20, pady=10)
        
        today_label = ttk.Label(today_card, text="Today's Attendance", style='Header.TLabel')
        today_label.pack(pady=(GUI_CONFIG['card_padding'], 10))
        
        # Attendance list
        list_frame = ttk.Frame(today_card, style='Card.TFrame')
        list_frame.pack(fill='both', expand=True, padx=GUI_CONFIG['card_padding'], 
                       pady=(0, GUI_CONFIG['card_padding']))
        
        self.attendance_tree = ttk.Treeview(list_frame, 
                                          columns=('Time', 'Student ID', 'Name', 'Method', 'Course'), 
                                          show='headings', height=12)
        self.attendance_tree.heading('Time', text='Time')
        self.attendance_tree.heading('Student ID', text='Student ID')
        self.attendance_tree.heading('Name', text='Name')
        self.attendance_tree.heading('Method', text='Method')
        self.attendance_tree.heading('Course', text='Course')
        
        self.attendance_tree.column('Time', width=150)
        self.attendance_tree.column('Student ID', width=100)
        self.attendance_tree.column('Name', width=150)
        self.attendance_tree.column('Method', width=100)
        self.attendance_tree.column('Course', width=150)
        
        self.attendance_tree.pack(side='left', fill='both', expand=True)
        
        # Scrollbar for attendance list
        attendance_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.attendance_tree.yview)
        attendance_scrollbar.pack(side='right', fill='y')
        self.attendance_tree.configure(yscrollcommand=attendance_scrollbar.set)
        
        # Refresh button
        ttk.Button(today_card, text="🔄 Refresh Attendance", 
                  style='Secondary.TButton',
                  command=self.refresh_attendance_list).pack(pady=10)
        
    def create_reports_tab(self):
        """Create the reports tab"""
        reports_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(reports_frame, text="📊 Reports")
        
        # Filters card
        filters_card = ttk.Frame(reports_frame, style='Card.TFrame')
        filters_card.pack(fill='x', padx=20, pady=(20, 10))
        
        filters_label = ttk.Label(filters_card, text="Report Filters", style='Header.TLabel')
        filters_label.pack(pady=(GUI_CONFIG['card_padding'], 10))
        
        filters_frame = ttk.Frame(filters_card, style='Card.TFrame')
        filters_frame.pack(fill='x', padx=GUI_CONFIG['card_padding'], pady=(0, GUI_CONFIG['card_padding']))
        
        # Date range
        date_frame = ttk.Frame(filters_frame, style='Card.TFrame')
        date_frame.pack(fill='x', pady=10)
        
        ttk.Label(date_frame, text="Start Date:", style='Subtitle.TLabel').pack(side='left')
        self.start_date_entry = ttk.Entry(date_frame, width=15, 
                                        font=(GUI_CONFIG['font_family'], GUI_CONFIG['font_size']))
        self.start_date_entry.pack(side='left', padx=5)
        self.start_date_entry.insert(0, date.today().strftime('%Y-%m-%d'))
        
        ttk.Label(date_frame, text="End Date:", style='Subtitle.TLabel').pack(side='left', padx=(20, 0))
        self.end_date_entry = ttk.Entry(date_frame, width=15, 
                                      font=(GUI_CONFIG['font_family'], GUI_CONFIG['font_size']))
        self.end_date_entry.pack(side='left', padx=5)
        self.end_date_entry.insert(0, date.today().strftime('%Y-%m-%d'))
        
        # Student and course filters
        filter_frame = ttk.Frame(filters_frame, style='Card.TFrame')
        filter_frame.pack(fill='x', pady=10)
        
        ttk.Label(filter_frame, text="Student ID:", style='Subtitle.TLabel').pack(side='left')
        self.report_student_entry = ttk.Entry(filter_frame, width=15, 
                                            font=(GUI_CONFIG['font_family'], GUI_CONFIG['font_size']))
        self.report_student_entry.pack(side='left', padx=5)
        
        ttk.Label(filter_frame, text="Course ID:", style='Subtitle.TLabel').pack(side='left', padx=(20, 0))
        self.report_course_entry = ttk.Entry(filter_frame, width=15, 
                                           font=(GUI_CONFIG['font_family'], GUI_CONFIG['font_size']))
        self.report_course_entry.pack(side='left', padx=5)
        
        # Generate and export buttons
        button_frame = ttk.Frame(filters_frame, style='Card.TFrame')
        button_frame.pack(fill='x', pady=15)
        
        ttk.Button(button_frame, text="📊 Generate Report", 
                  style='Primary.TButton',
                  command=self.generate_report).pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="📥 Export to CSV", 
                  style='Accent.TButton',
                  command=self.export_report).pack(side='left', padx=5)
        
        # Report display card
        report_card = ttk.Frame(reports_frame, style='Card.TFrame')
        report_card.pack(fill='both', expand=True, padx=20, pady=10)
        
        report_label = ttk.Label(report_card, text="Report Results", style='Header.TLabel')
        report_label.pack(pady=(GUI_CONFIG['card_padding'], 10))
        
        # Report text widget
        report_frame = ttk.Frame(report_card, style='Card.TFrame')
        report_frame.pack(fill='both', expand=True, padx=GUI_CONFIG['card_padding'], 
                         pady=(0, GUI_CONFIG['card_padding']))
        
        self.report_text = tk.Text(report_frame, height=20, 
                                 font=(GUI_CONFIG['font_family'], GUI_CONFIG['font_size']),
                                 bg=GUI_CONFIG['background_color'],
                                 fg=GUI_CONFIG['text_color'],
                                 relief='flat', borderwidth=0)
        self.report_text.pack(side='left', fill='both', expand=True)
        
        # Scrollbar for report
        report_scrollbar = ttk.Scrollbar(report_frame, orient='vertical', command=self.report_text.yview)
        report_scrollbar.pack(side='right', fill='y')
        self.report_text.configure(yscrollcommand=report_scrollbar.set)
        
    def create_settings_tab(self):
        """Create the settings tab"""
        settings_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        # System settings card
        system_card = ttk.Frame(settings_frame, style='Card.TFrame')
        system_card.pack(fill='x', padx=20, pady=(20, 10))
        
        system_label = ttk.Label(system_card, text="System Settings", style='Header.TLabel')
        system_label.pack(pady=(GUI_CONFIG['card_padding'], 10))
        
        system_frame = ttk.Frame(system_card, style='Card.TFrame')
        system_frame.pack(fill='x', padx=GUI_CONFIG['card_padding'], pady=(0, GUI_CONFIG['card_padding']))
        
        ttk.Button(system_frame, text="💾 Backup Database", 
                  style='Primary.TButton',
                  command=self.backup_database).pack(side='left', padx=5)
        
        ttk.Button(system_frame, text="📂 Restore Database", 
                  style='Secondary.TButton',
                  command=self.restore_database).pack(side='left', padx=5)
        
        # Status display
        self.settings_status_label = ttk.Label(system_card, text="", style='Status.TLabel')
        self.settings_status_label.pack(pady=20)
        
    def update_status(self):
        """Update system status display"""
        try:
            # Database status
            students = self.database_manager.get_all_students()
            self.db_status_label.config(text=f"Database: Connected ({len(students)} students)", 
                                       style='Success.TLabel')
        except Exception as e:
            self.db_status_label.config(text=f"Database: Error - {str(e)}", 
                                       style='Error.TLabel')
        
        # Update statistics
        self.update_statistics()
        
        # Schedule next update
        self.root.after(5000, self.update_status)
        
    def update_statistics(self):
        """Update statistics display"""
        try:
            students = self.database_manager.get_all_students()
            courses = self.database_manager.get_all_courses()
            
            # Get today's attendance
            today = date.today()
            today_attendance = self.database_manager.get_attendance_report(
                start_date=today, end_date=today
            )
            
            # Update stat cards
            if hasattr(self, 'stat_cards'):
                self.stat_cards['Total Students'].config(text=str(len(students)))
                self.stat_cards['Total Courses'].config(text=str(len(courses)))
                self.stat_cards['Today\'s Attendance'].config(text=str(len(today_attendance)))
                self.stat_cards['System Status'].config(text="Active")
            
            # Update activity text
            activity_text = f"System Statistics:\n"
            activity_text += f"• Total Students: {len(students)}\n"
            activity_text += f"• Total Courses: {len(courses)}\n"
            activity_text += f"• Today's Attendance: {len(today_attendance)} records\n\n"
            
            activity_text += "Recent Activity:\n"
            
            # Show recent attendance
            for record in today_attendance[-5:]:  # Last 5 records
                activity_text += f"• {record[1]} - {record[2]} ({record[4]})\n"
            
            if hasattr(self, 'activity_text'):
                self.activity_text.config(state='normal')
                self.activity_text.delete(1.0, tk.END)
                self.activity_text.insert(1.0, activity_text)
                self.activity_text.config(state='disabled')
            
        except Exception as e:
            if hasattr(self, 'activity_text'):
                self.activity_text.config(state='normal')
                self.activity_text.delete(1.0, tk.END)
                self.activity_text.insert(1.0, f"Error loading statistics: {str(e)}")
                self.activity_text.config(state='disabled')
    
    def add_student(self):
        """Add a new student to the database"""
        student_id = self.student_id_entry.get().strip()
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        department = self.department_entry.get().strip()
        
        if not student_id or not name:
            messagebox.showerror("Error", "Student ID and Name are required!")
            return
        
        try:
            self.database_manager.add_student(student_id, name, email, phone, department)
            messagebox.showinfo("Success", f"Student {name} added successfully!")
            
            # Clear entries
            self.student_id_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            self.department_entry.delete(0, tk.END)
            
            # Refresh student list
            self.refresh_student_list()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add student: {str(e)}")
    
    def verify_id_attendance(self):
        """Verify student ID and record attendance"""
        student_id = self.attendance_id_entry.get().strip()
        course_id = self.course_var.get()
        
        if not student_id:
            messagebox.showerror("Error", "Please enter a Student ID!")
            return
        
        try:
            # Check if student exists
            student = self.database_manager.get_student(student_id)
            if not student:
                messagebox.showerror("Error", f"Student ID {student_id} not found!")
                return
            
            # Record attendance
            result = self.database_manager.record_attendance(
                student_id, verification_method="id_pass", course_id=course_id
            )
            
            if result:
                self.attendance_status_label.config(
                    text=f"✅ Attendance recorded for {student[1]} ({student_id})", 
                    style='Success.TLabel'
                )
                self.attendance_id_entry.delete(0, tk.END)
                self.refresh_attendance_list()
            else:
                self.attendance_status_label.config(
                    text="⚠️ Attendance already recorded for today", 
                    style='Warning.TLabel'
                )
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to record attendance: {str(e)}")
            self.attendance_status_label.config(text="❌ Error recording attendance", style='Error.TLabel')
    
    def generate_report(self):
        """Generate attendance report"""
        try:
            start_date = self.start_date_entry.get()
            end_date = self.end_date_entry.get()
            student_id = self.report_student_entry.get().strip() or None
            course_id = self.report_course_entry.get().strip() or None
            
            # Convert dates
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date() if start_date else None
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else None
            
            # Get report data
            report_data = self.database_manager.get_attendance_report(
                start_date=start_date, end_date=end_date, 
                student_id=student_id, course_id=course_id
            )
            
            # Display report
            report_text = f"📊 Attendance Report\n"
            report_text += f"Period: {start_date} to {end_date}\n"
            report_text += f"Student ID: {student_id or 'All'}\n"
            report_text += f"Course ID: {course_id or 'All'}\n"
            report_text += f"Total Records: {len(report_data)}\n\n"
            
            if report_data:
                report_text += "Date/Time | Student ID | Name | Method | Course\n"
                report_text += "-" * 60 + "\n"
                
                for record in report_data:
                    report_text += f"{record[0]} | {record[1]} | {record[2]} | {record[4]} | {record[5] or 'N/A'}\n"
            else:
                report_text += "No attendance records found for the specified criteria.\n"
            
            self.report_text.config(state='normal')
            self.report_text.delete(1.0, tk.END)
            self.report_text.insert(1.0, report_text)
            self.report_text.config(state='disabled')
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
    
    def export_report(self):
        """Export attendance report to CSV"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if filename:
                start_date = self.start_date_entry.get()
                end_date = self.end_date_entry.get()
                student_id = self.report_student_entry.get().strip() or None
                course_id = self.report_course_entry.get().strip() or None
                
                # Convert dates
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date() if start_date else None
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else None
                
                # Get report data
                report_data = self.database_manager.get_attendance_report(
                    start_date=start_date, end_date=end_date, 
                    student_id=student_id, course_id=course_id
                )
                
                # Write to CSV
                import csv
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Date/Time', 'Student ID', 'Name', 'Method', 'Course'])
                    
                    for record in report_data:
                        writer.writerow([record[0], record[1], record[2], record[4], record[5] or 'N/A'])
                
                messagebox.showinfo("Success", f"Report exported to {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {str(e)}")
    
    def backup_database(self):
        """Backup database"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".db",
                filetypes=[("Database files", "*.db"), ("All files", "*.*")]
            )
            
            if filename:
                import shutil
                shutil.copy2(self.database_manager.db_path, filename)
                messagebox.showinfo("Success", f"Database backed up to {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Backup failed: {str(e)}")
    
    def restore_database(self):
        """Restore database"""
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("Database files", "*.db"), ("All files", "*.*")]
            )
            
            if filename:
                if messagebox.askyesno("Confirm", "This will replace the current database. Continue?"):
                    import shutil
                    shutil.copy2(filename, self.database_manager.db_path)
                    messagebox.showinfo("Success", "Database restored successfully!")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Restore failed: {str(e)}")
    
    def refresh_student_list(self):
        """Refresh the student list display"""
        try:
            # Clear existing items
            for item in self.student_tree.get_children():
                self.student_tree.delete(item)
            
            # Get students from database
            students = self.database_manager.get_all_students()
            
            # Add to treeview
            for student in students:
                self.student_tree.insert('', 'end', values=student)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh student list: {str(e)}")
    
    def refresh_courses(self):
        """Refresh the course list"""
        try:
            courses = self.database_manager.get_all_courses()
            course_list = [f"{course[0]} - {course[1]}" for course in courses]
            self.course_combo['values'] = course_list
            if course_list:
                self.course_combo.set(course_list[0])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh courses: {str(e)}")
    
    def refresh_attendance_list(self):
        """Refresh the attendance list display"""
        try:
            # Clear existing items
            for item in self.attendance_tree.get_children():
                self.attendance_tree.delete(item)
            
            # Get today's attendance
            today = date.today()
            attendance_records = self.database_manager.get_attendance_report(
                start_date=today, end_date=today
            )
            
            # Add to treeview
            for record in attendance_records:
                self.attendance_tree.insert('', 'end', values=(
                    record[0], record[1], record[2], record[4], record[5] or 'N/A'
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh attendance list: {str(e)}")
    
    def quick_attendance(self):
        """Quick attendance action from dashboard"""
        self.notebook.select(2)  # Switch to attendance tab
        self.attendance_id_entry.focus()
    
    def quick_view_attendance(self):
        """Quick view attendance action from dashboard"""
        self.notebook.select(2)  # Switch to attendance tab
        self.refresh_attendance_list()
    
    def quick_add_student(self):
        """Quick add student action from dashboard"""
        self.notebook.select(1)  # Switch to student management tab
        self.student_id_entry.focus()
    
    def run(self):
        """Start the GUI application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        try:
            pass  # No hardware resources to clean up
        except Exception as e:
            print(f"Cleanup error: {e}")

