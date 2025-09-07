import sqlite3
import uuid
from datetime import datetime

# --- 1. DATABASE SETUP ---

def setup_database(db_name="campus_events.db"):
    """Creates the database and tables based on the design document."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Drop tables if they exist for a clean setup
    cursor.execute("DROP TABLE IF EXISTS AttendanceFeedback;")
    cursor.execute("DROP TABLE IF EXISTS Registrations;")
    cursor.execute("DROP TABLE IF EXISTS Events;")
    cursor.execute("DROP TABLE IF EXISTS Students;")
    cursor.execute("DROP TABLE IF EXISTS Colleges;")

    # Create Colleges Table
    cursor.execute("""
        CREATE TABLE Colleges (
            college_id VARCHAR(255) PRIMARY KEY,
            college_name VARCHAR(255) NOT NULL
        );
    """)

    # Create Students Table
    cursor.execute("""
        CREATE TABLE Students (
            student_id VARCHAR(255) PRIMARY KEY,
            student_name VARCHAR(255) NOT NULL,
            college_id VARCHAR(255),
            FOREIGN KEY (college_id) REFERENCES Colleges (college_id)
        );
    """)

    # Create Events Table
    cursor.execute("""
        CREATE TABLE Events (
            event_id VARCHAR(255) PRIMARY KEY,
            event_name VARCHAR(255) NOT NULL,
            event_type VARCHAR(50),
            event_date DATETIME NOT NULL,
            event_status VARCHAR(50) NOT NULL,
            college_id VARCHAR(255),
            FOREIGN KEY (college_id) REFERENCES Colleges (college_id)
        );
    """)

    # Create Registrations Table
    cursor.execute("""
        CREATE TABLE Registrations (
            reg_id VARCHAR(255) PRIMARY KEY,
            student_id VARCHAR(255),
            event_id VARCHAR(255),
            reg_date DATETIME NOT NULL,
            FOREIGN KEY (student_id) REFERENCES Students (student_id),
            FOREIGN KEY (event_id) REFERENCES Events (event_id),
            UNIQUE (student_id, event_id)
        );
    """)

    # Create AttendanceFeedback Table
    cursor.execute("""
        CREATE TABLE AttendanceFeedback (
            attendance_id VARCHAR(255) PRIMARY KEY,
            reg_id VARCHAR(255),
            is_present BOOLEAN NOT NULL,
            feedback_score INTEGER,
            FOREIGN KEY (reg_id) REFERENCES Registrations (reg_id)
        );
    """)

    print("Database and tables created successfully.")
    conn.commit()
    conn.close()

def populate_sample_data(db_name="campus_events.db"):
    """Populates the database with sample data for testing."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Sample Colleges
    colleges = [('col_01', 'Global Tech Institute'), ('col_02', 'National Arts University')]
    cursor.executemany("INSERT INTO Colleges VALUES (?, ?);", colleges)

    # Sample Students
    students = [
        (str(uuid.uuid4()), 'Alice Johnson', 'col_01'),
        (str(uuid.uuid4()), 'Bob Williams', 'col_01'),
        (str(uuid.uuid4()), 'Charlie Brown', 'col_01'),
        (str(uuid.uuid4()), 'Diana Miller', 'col_02'),
        (str(uuid.uuid4()), 'Ethan Davis', 'col_02')
    ]
    cursor.executemany("INSERT INTO Students VALUES (?, ?, ?);", students)

    # Sample Events
    events = [
        (str(uuid.uuid4()), 'AI Hackathon 2025', 'Workshop', datetime(2025, 10, 22), 'Scheduled', 'col_01'),
        (str(uuid.uuid4()), 'Annual Tech Fest', 'Fest', datetime(2025, 11, 15), 'Scheduled', 'col_01'),
        (str(uuid.uuid4()), 'Modern Art Exhibition', 'Seminar', datetime(2025, 10, 5), 'Scheduled', 'col_02'),
        (str(uuid.uuid4()), 'Cancelled Coding Contest', 'Workshop', datetime(2025, 9, 1), 'Cancelled', 'col_01')
    ]
    cursor.executemany("INSERT INTO Events VALUES (?, ?, ?, ?, ?, ?);", events)

    # Helper to get IDs for registrations
    students_dict = {name: sid for sid, name, _ in students}
    events_dict = {name: eid for eid, name, _, _, _, _ in events}
    
    # Sample Registrations and Attendance
    # Note: A real app would have separate functions for these actions.
    # We are populating directly for demonstration.
    
    # Alice registers for Hackathon and attends
    reg1_id = str(uuid.uuid4())
    cursor.execute("INSERT INTO Registrations VALUES (?, ?, ?, ?)", (reg1_id, students_dict['Alice Johnson'], events_dict['AI Hackathon 2025'], datetime.now()))
    cursor.execute("INSERT INTO AttendanceFeedback VALUES (?, ?, ?, ?)", (str(uuid.uuid4()), reg1_id, True, 5))

    # Bob registers for Hackathon and attends
    reg2_id = str(uuid.uuid4())
    cursor.execute("INSERT INTO Registrations VALUES (?, ?, ?, ?)", (reg2_id, students_dict['Bob Williams'], events_dict['AI Hackathon 2025'], datetime.now()))
    cursor.execute("INSERT INTO AttendanceFeedback VALUES (?, ?, ?, ?)", (str(uuid.uuid4()), reg2_id, True, 4))
    
    # Alice also registers for Tech Fest and attends
    reg3_id = str(uuid.uuid4())
    cursor.execute("INSERT INTO Registrations VALUES (?, ?, ?, ?)", (reg3_id, students_dict['Alice Johnson'], events_dict['Annual Tech Fest'], datetime.now()))
    cursor.execute("INSERT INTO AttendanceFeedback VALUES (?, ?, ?, ?)", (str(uuid.uuid4()), reg3_id, True, 5))

    # Charlie registers for Tech Fest but is absent
    reg4_id = str(uuid.uuid4())
    cursor.execute("INSERT INTO Registrations VALUES (?, ?, ?, ?)", (reg4_id, students_dict['Charlie Brown'], events_dict['Annual Tech Fest'], datetime.now()))
    cursor.execute("INSERT INTO AttendanceFeedback VALUES (?, ?, ?, ?)", (str(uuid.uuid4()), reg4_id, False, None))

    # Diana registers for Art Exhibition and attends
    reg5_id = str(uuid.uuid4())
    cursor.execute("INSERT INTO Registrations VALUES (?, ?, ?, ?)", (reg5_id, students_dict['Diana Miller'], events_dict['Modern Art Exhibition'], datetime.now()))
    cursor.execute("INSERT INTO AttendanceFeedback VALUES (?, ?, ?, ?)", (str(uuid.uuid4()), reg5_id, True, 3))


    print("Sample data populated successfully.")
    conn.commit()
    conn.close()

# --- 2. REPORTING QUERIES ---

def get_event_popularity(db_name="campus_events.db", event_type=None):
    """Generates a report on event popularity, sorted by registration count."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    query = """
        SELECT
            e.event_name,
            e.event_type,
            COUNT(r.reg_id) AS registration_count
        FROM Events e
        LEFT JOIN Registrations r ON e.event_id = r.event_id
        WHERE e.event_status = 'Scheduled'
    """
    params = ()
    if event_type:
        query += " AND e.event_type = ?"
        params = (event_type,)
        
    query += """
        GROUP BY e.event_id
        ORDER BY registration_count DESC;
    """
    
    cursor.execute(query, params)
    report = cursor.fetchall()
    conn.close()
    return report

def get_student_participation(student_name, db_name="campus_events.db"):
    """Generates a report of all events a specific student attended."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    query = """
        SELECT
            s.student_name,
            e.event_name,
            e.event_date
        FROM Students s
        JOIN Registrations r ON s.student_id = r.student_id
        JOIN Events e ON r.event_id = e.event_id
        JOIN AttendanceFeedback af ON r.reg_id = af.reg_id
        WHERE s.student_name = ? AND af.is_present = 1 AND e.event_status = 'Scheduled';
    """
    
    cursor.execute(query, (student_name,))
    report = cursor.fetchall()
    conn.close()
    return report
    
def get_top_active_students(limit=3, db_name="campus_events.db"):
    """(Bonus) Generates a report of the top N most active students."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    query = """
        SELECT
            s.student_name,
            c.college_name,
            COUNT(af.attendance_id) as attended_events_count
        FROM Students s
        JOIN Registrations r ON s.student_id = r.student_id
        JOIN AttendanceFeedback af ON r.reg_id = af.reg_id
        JOIN Colleges c ON s.college_id = c.college_id
        WHERE af.is_present = 1
        GROUP BY s.student_id
        ORDER BY attended_events_count DESC
        LIMIT ?;
    """
    
    cursor.execute(query, (limit,))
    report = cursor.fetchall()
    conn.close()
    return report

def get_event_attendance_report(db_name="campus_events.db"):
    """Generates a report on attendance percentage per event."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    query = """
        SELECT
            e.event_name,
            COUNT(r.reg_id) AS registration_count,
            SUM(CASE WHEN af.is_present THEN 1 ELSE 0 END) AS attendance_count
        FROM Events e
        LEFT JOIN Registrations r ON e.event_id = r.event_id
        LEFT JOIN AttendanceFeedback af ON r.reg_id = af.reg_id
        WHERE e.event_status = 'Scheduled'
        GROUP BY e.event_id
        ORDER BY e.event_name;
    """
    
    cursor.execute(query)
    report = cursor.fetchall()
    conn.close()
    return report

def get_event_feedback_report(db_name="campus_events.db"):
    """Generates a report on the average feedback score per event."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    query = """
        SELECT
            e.event_name,
            AVG(af.feedback_score) AS average_score
        FROM Events e
        LEFT JOIN Registrations r ON e.event_id = r.event_id
        LEFT JOIN AttendanceFeedback af ON r.reg_id = af.reg_id
        WHERE e.event_status = 'Scheduled' AND af.feedback_score IS NOT NULL
        GROUP BY e.event_id
        ORDER BY average_score DESC;
    """
    
    cursor.execute(query)
    report = cursor.fetchall()
    conn.close()
    return report


# --- 3. MAIN EXECUTION ---

if __name__ == "__main__":
    DB_FILE = "campus_events.db"
    
    # Step 1: Initialize the database and add sample data
    setup_database(DB_FILE)
    populate_sample_data(DB_FILE)
    
    # Step 2: Generate and print reports
    print("\n--- Event Popularity Report ---")
    popularity = get_event_popularity(DB_FILE)
    for event in popularity:
        print(f"Event: {event[0]} ({event[1]}) - Registrations: {event[2]}")
        
    print("\n--- Event Popularity Report (Filtered for 'Workshop') ---")
    popularity_filtered = get_event_popularity(DB_FILE, event_type="Workshop")
    for event in popularity_filtered:
        print(f"Event: {event[0]} ({event[1]}) - Registrations: {event[2]}")

    print("\n--- Student Participation Report for 'Alice Johnson' ---")
    participation = get_student_participation("Alice Johnson", DB_FILE)
    for row in participation:
        print(f"Student: {row[0]} - Attended: {row[1]} on {row[2]}")

    print("\n--- Top 3 Most Active Students Report ---")
    top_students = get_top_active_students(3, DB_FILE)
    for student in top_students:
        print(f"Student: {student[0]} ({student[1]}) - Attended Events: {student[2]}")

    print("\n--- Event Attendance Report ---")
    attendance_report = get_event_attendance_report(DB_FILE)
    for row in attendance_report:
        event_name, reg_count, att_count = row
        # Handle case where there are no registrations to avoid division by zero
        percentage = (att_count / reg_count * 100) if reg_count > 0 else 0
        print(f"Event: {event_name} - Registrations: {reg_count}, Attended: {att_count} ({percentage:.2f}%)")

    print("\n--- Average Feedback Score Report ---")
    feedback_report = get_event_feedback_report(DB_FILE)
    for row in feedback_report:
        print(f"Event: {row[0]} - Average Feedback: {row[1]:.2f}")

