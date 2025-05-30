from flask import Flask, request, render_template
from utils import DroneSelectionSystem
import os

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'templates'))
app = Flask(__name__, template_folder=template_dir)

@app.route("/", methods=["GET"])
def home():
    """Render the homepage."""
    return render_template("index.html")

@app.route("/match-drones", methods=["POST"])
def match_drones():
    """Handles user input, filters drones using DroneSelectionSystem, and returns results."""
    
    # Get user input from frontend
    port_name = request.form.get("port")
    purposes = request.form.getlist("purpose")
    user_budget = float(request.form.get("budget"))
    max_maintenance_cost = float(request.form.get("maintenance_cost"))

    # Get AHP slider values from form
    slider_values = {
        "Battery Life (minutes)": float(request.form.get("battery_life_priority", 3)),
        "Wind Resistance (m/s)": float(request.form.get("wind_resistance_priority", 3)),
        "Camera Resolution (MP)": float(request.form.get("camera_resolution_priority", 3)),
        "Price (EUR)": float(request.form.get("price_priority", 3))
    }

    # Initialize drone selection system
    drone_system = DroneSelectionSystem()

    # Run selection pipeline
    results_df, summary = drone_system.select_drones(
        port_name=port_name,
        selected_purposes=purposes,
        slider_values=slider_values,
        budget=user_budget,
        max_maintenance_cost=max_maintenance_cost
    )

    # Convert results to dict for template
    drones = results_df.to_dict(orient="records") if not results_df.empty else []

    # Send matched drones and summary to frontend
    return render_template("results.html", drones=drones, summary=summary)

if __name__ == "__main__":
    app.run(debug=True)
