# Directory Structure Image Description for Drone DSS Project

The directory structure of the Drone Decision Support System (DSS) project is organized to separate concerns and facilitate development and maintenance. The main folders and their purposes are:

- **backend/**  
  Contains the backend logic, including API services, data processing, configuration, and utility scripts.  
  - `app.py`: Main Flask application entry point.  
  - `utils.py`: Contains the core drone selection system, data cleaning, filtering, and ranking logic.  
  - `data/`: Stores CSV datasets for drones and ports.  
  - `models/`: Placeholder for future model implementations.  
  - `config.py`: Configuration settings for the backend.  
  - `README.md`: Backend-specific documentation.

- **frontend/**  
  Contains the frontend components, including HTML templates, static assets (CSS, JS), and view logic.  
  - `templates/`: HTML files for rendering the user interface (e.g., `index.html`, `results.html`).  
  - `static/`: Static files such as CSS stylesheets (`custom.css`).  
  - `views.py` and `forms.py`: (if present) handle frontend logic and form processing.

- **additional resources/**  
  Contains supplementary files such as documentation, diagrams, datasets, scripts, and images used in the project.  
  - Includes files like `diagramatic_representation.svg`, `dss_schematic_diagram.svg`, `final_image_representation.png`, and various CSV and PDF files.

- **docs/**  
  Documentation files related to the project, including research and analysis reports.

- **tests/**  
  Contains test cases for backend and frontend components to ensure code quality and correctness.

- **root files**  
  - `README.md`: Project overview and setup instructions.  
  - `.gitignore`: Git ignore rules.  
  - `run_flask_app.bat`: Batch script to start the Flask backend server.

This organized directory structure supports modular development, easy navigation, and clear separation between backend, frontend, data, and documentation components.

# End of Directory Image Description
