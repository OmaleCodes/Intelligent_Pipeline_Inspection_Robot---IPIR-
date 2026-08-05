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