"""
Scratch script to seed fake inspection data into the database,
so the dashboard can be tested without a working camera.
Run this from the project root: python3 seed_test_data.py
"""

from database.models import InspectionDatabase
import time

db = InspectionDatabase()

# 1. Start a fake inspection run (same call kratos.py makes)
run_id = db.start_run("PIPE_01")
print(f"Started run: {run_id}")

# 2. Log a handful of fake defects — same shape kratos.py logs in its loop
fake_defects = [
    ("CRACK", 120, 80, 40, 45),
    ("CRACK", 200, 102, 25, 25),
    ("RUST", 60, 400, 60, 60),
    ("RUST", 400, 510, 35, 35),
    ("RUST", 222, 320, 80, 20),
]

for defect_type, x, y, w, h in fake_defects:
    db.log_defects(run_id, time.time(), defect_type, x, y, w, h)
    print(f"Logged {defect_type} at ({x},{y})")

# 3. Close out the run — same call kratos.py makes when 'q' is pressed
db.end_run(run_id)
print(f"Run {run_id} marked COMPLETED")

# 4. Sanity check using the methods you already built
print("\nAll runs in DB:", db.get_inspection_runs())
print("Defects for this run:", db.get_defects_for_runs(run_id))
