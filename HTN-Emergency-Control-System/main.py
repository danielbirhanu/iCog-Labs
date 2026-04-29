from htn_engine import HTNPlanner
from domain import methods, operators
from visualization import generate_tree


initial_state = {
    "emergency_type": "fire",
    "fire_detected": True,
    "injuries_reported": False,
    "alarm_active": False,
    "building_locked": True,
    "people_evacuated": False,
    "fire_department_called": False,
    "ambulance_sent": False,
    "fire_extinguished": False,
    "injuries_treated": False,
    "security_available": True,
    "security_dispatched": False,
    "police_called": False
}


goal = [("handle_emergency",)]

planner = HTNPlanner(methods, operators)

success = planner.plan_tasks(initial_state, goal)

if success:
    print("\nHTN planning successful.\n")
    print("Final primitive plan:")

    for step, action in enumerate(planner.plan, start=1):
        print(f"{step}. {action[0]}")

    print("\nFinal state:")
    for key, value in initial_state.items():
        print(f"{key}: {value}")

    generate_tree(planner.tree_edges)

else:
    print("Planning failed. No valid decomposition found.")