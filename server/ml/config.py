"""Paths and shared constants for the ml/ package."""
from pathlib import Path

ML_DIR = Path(__file__).resolve().parent
MODELS_DIR = ML_DIR / "models"
DATASETS_DIR = ML_DIR / "datasets"

SEVERITY_MODEL_PATH = MODELS_DIR / "severity_model.pkl"
RISK_MODEL_PATH = MODELS_DIR / "risk_model.pkl"
ROUTE_MODEL_PATH = MODELS_DIR / "route_model.pkl"
FORECAST_MODEL_PATH = MODELS_DIR / "forecast_model.pkl"

RANDOM_STATE = 42
