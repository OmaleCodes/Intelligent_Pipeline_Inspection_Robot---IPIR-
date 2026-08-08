"Database initialization to log and store inspection data in mysqlite3 database"
import sqlite3
import os
import time


class InspectionDatabase:
    def __init__(self, db_path="database/database.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._create_Tables()


    def _create_Tables(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
             CREATE TABLE IF NOT EXISTS inspection_runs (
                run_id TEXT PRIMARY KEY,
                start_time REAL,
                pipeline_id TEXT,
                status TEXT)
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS defect_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id TEXT,
                timestamp REAL,
                defect_type TEXT,
                x INTEGER, y INTEGER, w INTEGER, h INTEGER)
        """)
        conn.commit()
        conn.close()

    def start_run(self, Pipeline_id = "PIPE_01"):
         run_id = f"RUN_{int(time.time())}"


         conn = sqlite3.connect(self.db_path)
         cursor = conn.cursor()
         cursor.execute("""
            INSERT INTO inspection_runs(
            run_id,
            start_time, 
            Pipeline_id, 
            status)
            VALUES(?,?,?,?) """, (run_id, time.time(), Pipeline_id, "IN_PROGRESS"))
       
         conn.commit()
         conn.close()
         return run_id


    def log_defects (self,run_id, timestamp, defect_type, x,y,w,h):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(""" 
            INSERT INTO defect_logs (
            run_id,
            timestamp,
            defect_type,
            x,y,w,h)
            VALUES(?,?,?,?,?,?,?)""", (run_id, timestamp, defect_type, x,y,w,h))
        
        conn.commit()
        conn.close()


    def end_run(self, run_id):
        """Mark an inspection run as COMPLETED when the session ends"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE inspection_runs
            SET status = ?
            WHERE run_id = ?""", ("COMPLETED", run_id))
        
        conn.commit()
        conn.close()

    #Connects to Database to fetch inspections runs
    def get_inspection_runs(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT run_id FROM inspection_runs ORDER BY start_time DESC")
            runs = [row[0] for row in cursor.fetchall()]
            return runs

    #Fetch defects for selected runs
    def get_defects_for_runs(self,selected_run):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, timestamp, defect_type, x, y, w, h FROM defect_logs WHERE run_id = ? ", (selected_run))
            defects = cursor.fetchall()
            return defects

    #feteches all defects as a single value
    def total_defect(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT run_id , COUNT(*) FROM defect_logs GROUP by run_id ORDER BY run_id ")
            count = cursor.fetchall()
            return count
