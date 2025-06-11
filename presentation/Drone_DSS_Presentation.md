# Drone Decision Support System (DSS) Presentation

---

## Slide 1: Title Slide
- **Project Name:** Drone Decision Support System (DSS)
- **Subtitle:** European Small Ports Implementation
- **Presenter:** [Your Name]
- **Date:** [Presentation Date]

---

## Slide 2: Introduction
- Purpose: Provide a decision support system for selecting drones tailored to specific port environments and operational purposes.
- Importance: Optimizes drone selection for efficient port operations and safety.

---

## Slide 3: Project Structure
- **backend/**: Backend logic, data processing, API services.
- **frontend/**: Frontend templates, static files, views.
- **additional resources/**: Supplementary data files and resources.
- **docs/**: Documentation files.
- **tests/**: Test cases for backend and frontend components.

---

## Slide 4: System Architecture
- Overview of the technical architecture.
- Frontend components: User Interface, HTML templates, Flask routes, static assets.
- Backend components: Flask API, configuration, decision logic, models, tests.
- Data layer: Drone specifications and port requirements datasets.
- Decision logic algorithms: Weighted Sum Model (WSM) and Analytic Hierarchy Process (AHP).
- System integration and data flow.

*Include architecture diagram (diagramatic_representation.svg)*

---

## Slide 5: Backend Logic
- Flask backend routes:
  - Homepage ("/")
  - Drone matching endpoint ("/match-drones")
- User inputs: port, purposes, budget, maintenance cost, AHP priorities.
- DroneSelectionSystem processes inputs and returns recommendations.

---

## Slide 6: Frontend Interface
- User input form includes:
  - Port selection (searchable list)
  - Drone purposes (multiple checkboxes)
  - Budget and maintenance cost inputs
  - AHP criteria sliders for Battery Life, Wind Resistance, Camera Resolution, Price
- User flow: Input → Submit → View Results

---

## Slide 7: Data Sources
- Drone specifications dataset (droneType.csv)
- Port requirements dataset (dataset.csv)
- Key data characteristics: flight radius, payload, battery life, weather resistance, etc.

---

## Slide 8: Decision Logic Algorithms
- Weighted Sum Model (WSM):
  - Assigns weights to criteria
  - Calculates weighted scores for drones
- Analytic Hierarchy Process (AHP):
  - Pairwise comparison matrix
  - Consistency checking
  - Priority vector calculation

---

## Slide 9: Deployment & Technical Specs
- Flask development server
- Python 3.8+ runtime
- CSV file-based data storage
- Real-time decision making
- Scalable and modular design
- Input validation and error handling

---

## Slide 10: Future Extensions
- Database integration
- Machine learning enhancements
- API expansion for external integrations

---

## Slide 11: Visuals and Diagrams
- Architecture diagram
- Additional images (final_image_representation.png)

---

## Slide 12: Conclusion
- Summary of project goals and achievements
- Potential impact on port operations
- Next steps and future work

---

## Notes:
- Replace placeholders like [Your Name] and [Presentation Date] before presenting.
- Use visuals from the additional resources folder to enhance slides.
