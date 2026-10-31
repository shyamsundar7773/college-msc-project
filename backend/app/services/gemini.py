"""Configuration boundary for future Gemini explanations.

Gemini should summarize verified model and explanation outputs. It must not
generate churn predictions or substitute for SHAP/LIME calculations.
"""

from app.core.config import get_settings


def gemini_is_configured() -> bool:
    """Return whether the backend has a Gemini key, without exposing its value."""
    return bool(get_settings().gemini_api_key.strip())
