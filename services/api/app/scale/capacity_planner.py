# Capacity Planner & 100x Growth Scaling Model Engine

from typing import Dict, Any

class CapacityPlanner:
    """Models throughput capacity, connection pool scaling, and worker backpressure limits."""

    @staticmethod
    def calculate_scale_capacity(scale_factor: float = 10.0) -> Dict[str, Any]:
        baseline_api_rpm = 1500
        baseline_db_conn = 20
        baseline_workers = 4

        return {
            "scale_factor": scale_factor,
            "target_api_rpm": baseline_api_rpm * scale_factor,
            "recommended_db_connections": min(int(baseline_db_conn * scale_factor), 200),
            "recommended_workers": min(int(baseline_workers * scale_factor), 64),
            "use_pgbouncer": scale_factor >= 10.0,
            "backpressure_queue_threshold": 1000
        }

capacity_planner = CapacityPlanner()
