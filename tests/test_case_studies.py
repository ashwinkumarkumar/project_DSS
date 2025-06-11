import pprint
import pytest
from backend.utils import DroneSelectionSystem

@pytest.mark.parametrize("case_num, port_name, selected_purposes, slider_values, budget, max_maintenance_cost", [
    (1, "Port of Hamburg", ["Port Security"], 
     {"Battery Life (minutes)": 4, "Wind Resistance (m/s)": 5, "Camera Resolution (MP)": 3, "Price (EUR)": 2}, 
     60000, 1500),
    (2, "Port of Rotterdam", ["Environmental Monitoring", "Search & Rescue"], 
     {"Battery Life (minutes)": 5, "Wind Resistance (m/s)": 5, "Camera Resolution (MP)": 2, "Price (EUR)": 1}, 
     80000, 2000),
    (3, "Port of Valencia", ["Agricultural"], 
     {"Battery Life (minutes)": 2, "Wind Resistance (m/s)": 2, "Camera Resolution (MP)": 4, "Price (EUR)": 5}, 
     40000, 1000)
])
def test_case_study(case_num, port_name, selected_purposes, slider_values, budget, max_maintenance_cost):
    print(f"Case Study {case_num}:")
    print(f"Port: {port_name}")
    print(f"Selected Purposes: {selected_purposes}")
    print(f"Slider Values: {slider_values}")
    print(f"Budget: {budget}")
    print(f"Max Maintenance Cost: {max_maintenance_cost}")
    print("-" * 40)
    
    system = DroneSelectionSystem()
    results, summary = system.select_drones(
        port_name=port_name,
        selected_purposes=selected_purposes,
        slider_values=slider_values,
        budget=budget,
        max_maintenance_cost=max_maintenance_cost
    )
    
    print(f"Summary: {summary}")
    if not results.empty:
        print("Top 3 Recommended Drones:")
        pprint.pprint(results[['Drone Name', 'Category', 'WSM Score', 'Price (EUR)']].head(3).to_dict(orient='records'))
    else:
        print("No suitable drones found.")
    print("\n\n")
