"""
classifier.py

Sends a cropped defect region to a custom-trained Roboflow model
(RF-DETR, trained on the "Pipe Defects" dataset) as a SECOND OPINION
on defects detector.py already found.

This is never a hard filter — detector.py's own findings should still
get logged regardless of what this returns. This module only adds
extra metadata (a second opinion + confidence) alongside them.

Only "crack", "hole", and "rupture" have a real, measured accuracy
score from training (51%, 65%, 87% respectively). "rust",
"copper corrosion", and "water rupture" exist as classes but had too
few labeled examples to trust yet — predictions of those classes are
marked is_trusted=False rather than being silently treated as equally
reliable.
"""

import os
from dotenv import load_dotenv
from inference_sdk import InferenceHTTPClient

load_dotenv()

# TODO: replace with your real model ID from Roboflow's "Model URL" field
# (the full string, e.g. "moses-philip/pipe-defects-ybzjr-spskb/1")
MODEL_ID = "moses-philip/pipe-defects-ybzjr-spskb-1-rfdetr-small-t1"


# Only these classes have a measured, trustworthy accuracy score.
TRUSTED_CLASSES = {"crack", "hole", "rupture"}

_client = None


def _get_client():
    """Create the Roboflow client once, reusing it on later calls."""
    global _client
    if _client is None:
        api_key = os.getenv("ROBOFLOW_API_KEY")
        if not api_key:
            return None
        _client = InferenceHTTPClient(
            api_url="https://detect.roboflow.com",
            api_key=api_key,
        )
    return _client


def classify_defect(cropped_region):
    """
    Send a cropped defect region to the Roboflow model for a second opinion.

    Args:
        cropped_region: a numpy array (BGR image) — the cropped defect
            area that detector.py already flagged.

    Returns:
        dict with:
            "defect_type": str or None — predicted class name, or None
                if the call failed or nothing was detected.
            "confidence": float or None — model confidence (0.0-1.0),
                or None if unavailable.
            "is_trusted": bool — True only if defect_type is one of
                the three measured classes (crack, hole, rupture).
                False for the thin-data classes, or on any failure.
    """
    client = _get_client()
    if client is None:
        # No API key found — fail safely, don't crash kratos.py
        return {"defect_type": None, "confidence": None, "is_trusted": False}

    try:
        result = client.infer(cropped_region, model_id=MODEL_ID)
        predictions = result.get("predictions", [])

        if not predictions:
            return {"defect_type": None, "confidence": None, "is_trusted": False}

        # take the single highest-confidence prediction
        best = max(predictions, key=lambda p: p.get("confidence", 0))
        defect_type = best.get("class")
        confidence = best.get("confidence")

        return {
            "defect_type": defect_type,
            "confidence": confidence,
            "is_trusted": defect_type in TRUSTED_CLASSES,
        }

    except Exception as e:
        # Network issue, bad key, timeout, etc. — fail safely
        print(f"[classifier] Roboflow call failed: {e}")
        return {"defect_type": None, "confidence": None, "is_trusted": False}