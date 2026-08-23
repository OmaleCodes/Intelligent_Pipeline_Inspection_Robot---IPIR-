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
                x INTEGER, y INTEGER, w INTEGER, h INTEGER,
                distance_meters REAL DEFAULT 0.0)
        """)

        # Migration check: Ensure distance_meters exists for existing databases
        cursor.execute("PRAGMA table_info(defect_logs)")
        columns = [column[1] for column in cursor.fetchall()]
        if "distance_meters" not in columns:
            cursor.execute("ALTER TABLE defect_logs ADD COLUMN distance_meters REAL DEFAULT 0.0")

        conn.commit()
        conn.close()

    def start_run(self, pipeline_id="PIPE_01"):
         run_id = f"RUN_{int(time.time() * 1000)}"


         conn = sqlite3.connect(self.db_path)
         cursor = conn.cursor()
         cursor.execute("""
            INSERT INTO inspection_runs(
            run_id,
            start_time, 
            pipeline_id, 
            status)
            VALUES(?,?,?,?) """, (run_id, time.time(), pipeline_id, "IN_PROGRESS"))
       
         conn.commit()
         conn.close()
         return run_id


    def log_defects (self, run_id, timestamp, defect_type, x, y, w, h, distance_meters=0.0):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(""" 
            INSERT INTO defect_logs (
            run_id,
            timestamp,
            defect_type,
            x,y,w,h,
            distance_meters)
            VALUES(?,?,?,?,?,?,?,?)""", (run_id, timestamp, defect_type, x, y, w, h, distance_meters))
        
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
    def get_defects_for_runs(self, selected_run):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, timestamp, defect_type, x, y, w, h, distance_meters FROM defect_logs WHERE run_id = ? ", (selected_run,))
            defects = cursor.fetchall()
            return defects

    #fetches defect counts for all runs including 0-defect runs
    def total_defect(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.run_id, COUNT(d.id)
                FROM inspection_runs r
                LEFT JOIN defect_logs d ON r.run_id = d.run_id
                GROUP BY r.run_id
                ORDER BY r.start_time ASC
            """)
            count = cursor.fetchall()
            return count
