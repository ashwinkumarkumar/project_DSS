# Image Descriptions for Drone DSS Presentation

---

## 1. Flow Diagram Description
The flow diagram illustrates the overall architecture and workflow of the Drone Decision Support System (DSS). It is divided into three main sections:

- **Frontend (Flask Web UI):**
  - User Interface: Allows users to select ports, input drone selection criteria, and submit requests.
  - HTML Templates: Dynamic rendering of pages such as index.html and results.html.
  - Flask Routes: Handle navigation and form submissions.
  - Static Assets: CSS styling and other static files.

- **Backend (Flask API):**
  - Flask API: Receives user requests, processes inputs, and returns results.
  - Configuration: Contains settings for decision logic.
  - Decision Logic: Implements filtering, ranking, and optimization algorithms.
  - Models: Placeholder for future expansion.
  - Tests: Ensures logic correctness.

- **Data Layer:**
  - Drone Dataset: Contains drone specifications such as flight radius, payload, battery life, and camera resolution.
  - Port Dataset: Contains port environmental and operational requirements.
  - Data Characteristics: Includes thermal imaging, weather resistance, and communication capabilities.

The data flow starts with user input on the frontend, which is sent to the backend API. The backend queries the datasets, applies decision logic algorithms (WSM and AHP), and returns ranked drone recommendations to the frontend for display.

---

## 2. Data Cleaning Description
The data cleaning process involves loading drone data from CSV files and normalizing it for consistent analysis:

- Numeric columns such as flight radius, battery life, payload capacity, and price are converted to numeric types with error handling.
- Missing values in numeric columns are imputed adaptively:
  - Thermal camera resolution missing values are set to zero (indicating no thermal capability).
  - Camera resolution missing values are filled with the median.
  - Payload capacity missing values are set to a minimal default.
  - Other numeric columns use median imputation.
- Categorical columns like day/night operation, real-time data streaming, infrared capability, IP rating, and humidity resistance are filled with default values if missing.
- Categorical values are standardized for consistency (e.g., "Yes"/"No" formatting).

This cleaning ensures the drone dataset is complete and consistent for filtering and ranking.

---

## 3. Data Usage Description
The cleaned drone data and port environmental data are used in the selection process as follows:

- Port environmental constraints such as temperature range, humidity, wind speed, and coverage area are extracted from port datasets.
- Drones are filtered based on these constraints, ensuring compatibility with port conditions (e.g., wind resistance, temperature tolerance, flight radius).
- Additional filtering is applied based on user-selected drone purposes, matching drone capabilities to operational needs.
- Cost and maintenance constraints are applied to filter drones within budget.
- The filtered dataset is then ranked using decision logic algorithms.

---

## 4. Drone Selection Description
The drone selection pipeline includes:

- Loading and cleaning drone and port data.
- Extracting port environmental constraints.
- Filtering drones by port constraints (wind resistance, temperature range, coverage area, IP rating).
- Filtering drones by selected purposes using attribute matching.
- Filtering drones by budget and maintenance cost.
- Ranking drones using Weighted Sum Model (WSM) with priority weights derived from user input.
- Returning a ranked list of suitable drones with a summary of the filtering process.

---

## 5. AHP & WSM Algorithms Description
- **Analytic Hierarchy Process (AHP):**
  - Users assign priority values to criteria (battery life, wind resistance, camera resolution, price).
  - A pairwise comparison matrix is constructed from these priorities.
  - Priority weights are calculated using the geometric mean method.
  - Consistency of the matrix is checked to ensure reliable weights.

- **Weighted Sum Model (WSM):**
  - Drone attributes are normalized to a 0-1 scale.
  - Each attribute is multiplied by its corresponding AHP-derived weight.
  - Weighted scores are summed to produce an overall score for each drone.
  - An additional cost-effectiveness score is added to favor economical options.
  - Drones are ranked based on their total WSM score.

These algorithms provide a quantitative and consistent method to rank drones according to user preferences and operational requirements.

---

# End of Image Descriptions
