# ml/

Standalone, dependency-light algorithms used across the backend, independent of the
YOLO image pipeline in `ai_model/` and `services/yolo_service.py`:

- **Pathfinding**: `graph_algorithms.py`, `dijkstra.py`, `astar.py`, `bfs.py`, `dfs.py`,
  `path_finder.py`, `safest_route.py` (hazard-aware routing), `route_prediction.py`
  (travel-time estimation)
- **Prediction models** (scikit-learn, with heuristic fallbacks — see `training/`):
  `severity_prediction.py`, `risk_assessment.py`, `disaster_forecasting.py`
- **Recommendation**: `shelter_recommendation.py`, `hospital_recommendation.py`,
  `rescue_team_assignment.py`, `location_optimizer.py`
- **Signals**: `traffic_analysis.py`, `weather_analysis.py`, `emergency_priority.py`

Run `python ml/evaluation/evaluate_models.py` to see which models are trained vs.
running on their heuristic fallback. Train any of them with the matching script in
`ml/training/` — each works out-of-the-box on synthetic data if you don't have a real
labeled CSV yet, e.g.:

```bash
python ml/training/train_severity.py         # synthetic data
python ml/training/train_severity.py my.csv  # real labeled data
```
