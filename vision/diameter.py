"""
diameter.py

Placeholder module for pipe diameter estimation.

STATUS: STUB — no IR/depth hardware is currently available.
This module exists to define the interface that the rest of the
pipeline (kratos.py, dashboard) will call, so that when real
hardware is available, only the internals of estimate_diameter()
need to change — nothing that calls it has to change.
"""


def estimate_diameter(frame, reference_object_width_px=None):
    """
    Estimate the pipe diameter in millimeters from a video frame.

    Args:
        frame: the current camera frame (numpy array), for future use.
        reference_object_width_px: optional known-size reference object
            in the frame, for future monocular estimation.

    Returns:
        dict with:
            "diameter_mm": float or None — the estimated diameter.
                None while this is a stub, since no real measurement
                is possible without hardware.
            "is_estimated": bool — True if this value is a real
                measurement, False if it's a stub/placeholder value.
                Callers (kratos.py, dashboard) should check this flag
                before trusting or displaying diameter_mm as real data.
    """
    return {
        "diameter_mm": None,
        "is_estimated": False,
    }