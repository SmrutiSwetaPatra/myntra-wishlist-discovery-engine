import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.db_utils import get_dashboard_metrics, get_explorer_data

def test():
    try:
        print("Testing get_dashboard_metrics...")
        metrics = get_dashboard_metrics()
        print("Dashboard metrics success:", list(metrics.keys()))
    except Exception as e:
        print("Error in get_dashboard_metrics:", repr(e))

    try:
        print("Testing get_explorer_data...")
        data = get_explorer_data()
        print("Explorer data success, length:", len(data))
    except Exception as e:
        print("Error in get_explorer_data:", repr(e))

if __name__ == "__main__":
    test()
