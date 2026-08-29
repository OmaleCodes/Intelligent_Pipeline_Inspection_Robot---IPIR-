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

# 2. Log a handful of fake defects — same shape kratos.py logs in its loop.
# Includes roboflow_class / roboflow_confidence / is_trusted, mixing in
# some defects that were never classified (throttled that cycle) to
# match real behavior — those get None, same as kratos.py would send.
fake_defects = [
    # (defect_type, x, y, w, h, roboflow_class, roboflow_confidence, is_trusted)
    ("CRACK", 120, 80, 40, 15, "crack", 0.79, True),
    ("CRACK", 300, 210, 25, 25, None, None, None),          # not classified this cycle
    ("RUST", 60, 400, 60, 60, "hole", 0.41, True),
    ("RUST", 500, 150, 35, 35, None, None, None),            # not classified this cycle
    ("RUST", 220, 320, 50, 20, "rust", 0.35, False),          # classified, but untrusted class
]

for defect_type, x, y, w, h, roboflow_class, roboflow_confidence, is_trusted in fake_defects:
    db.log_defects(run_id, time.time(), defect_type, x, y, w, h,
                    roboflow_class, roboflow_confidence, is_trusted)
    print(f"Logged {defect_type} at ({x},{y}) — roboflow: {roboflow_class}, "
          f"conf: {roboflow_confidence}, trusted: {is_trusted}")

# 3. Close out the run — same call kratos.py makes when 'q' is pressed
db.end_run(run_id)
print(f"Run {run_id} marked COMPLETED")

# 4. Sanity check using the methods you already built
print("\nAll runs in DB:", db.get_inspection_runs())
print("Defects for this run:", db.get_defects_for_runs(run_id))