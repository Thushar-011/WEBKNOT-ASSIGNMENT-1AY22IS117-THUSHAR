Campus Event Reporting System Prototype

This repository houses my submission for the Webknot Technologies Campus Drive Assignment. Inside, you’ll find the design documentation, an operational Python prototype, and any other deliverables they listed.

Project Purpose
The main aim? Build the core reporting engine for a future Campus Event Management Platform. I wasn’t tasked with a full application, just a reliable backend that can handle data and answer the big questions about event performance and student activity.

Approach
I kicked things off with a comprehensive design document, mapping out the database schema, API endpoints, and user workflows before I touched any code. That “design-first” mindset helped me lock down critical architecture decisions early, like supporting multiple colleges with a multi-tenant model and using flexible VARCHAR IDs for scalability. For the prototype, I kept it simple: a lean Python script using SQLite. The whole point was to focus on SQL logic and data structure, meeting the assignment’s need for a working proof-of-concept instead of a half-finished app.

The prototype does what it’s supposed to: generates all the necessary reports, from event popularity and attendance rates to spotlighting the most active students. It’s a solid foundation for a future reporting system.

How to Run
Dependencies:
- Python 3.x

Steps:
1. Make sure Python is installed.
2. Open a terminal or command prompt.
3. Change directory to where you’ve saved prototype.py.
4. Run it with: `python prototype.py`
5. The script will create a campus_events.db file, populate it with sample data, and output all reports directly to your console.

