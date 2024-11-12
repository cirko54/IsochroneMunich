IsochroneMunich

IsochroneMunich is a Flask-based application that visualizes isochrone maps for Munich's public transportation system. It uses precomputed data for optimal performance and modularized backend scripts for efficient functionality. The project also incorporates client-side clustering to display stops on a Leaflet map efficiently.
Table of Contents

    Project Overview
    Features
    Project Structure
    Installation
    Usage
    Modules
    Scripts
    Future Development
    Contributing
    License

Project Overview

The application aims to display isochrone maps that illustrate travel times from selected stops in Munich, considering various transportation modes (public transport, walking, biking, etc.). The project uses precomputed data to enhance real-time performance and clusters stops by name within a 500-meter radius for better map readability.
Features

    Isochrone Calculation: Real-time travel time calculations from selected stops.
    Efficient Marker Clustering: Stops with the same name are grouped within a 500-meter radius.
    Precomputed Data for Performance: Reduces runtime computation needs.
    Modular Design: Clear separation of responsibilities for easy maintenance and further development.

Project Structure

The project is organized into core modules and auxiliary scripts for optimal functionality and maintainability.

IsochroneMunich/
├── app.py                    # Main Flask app entry point
├── config.py                 # Configuration file for constants
├── data/                     # Contains original and processed data files
├── static/                   # Frontend assets (JavaScript, CSS, images)
├── templates/                # HTML templates (e.g., index.html)
├── modules/                  # Core modules for isochrone calculation and stop loading
└── scripts/                  # Auxiliary scripts for data pre-processing

Installation

    Clone the Repository:

git clone https://github.com/your-username/IsochroneMunich.git
cd IsochroneMunich

Create a Virtual Environment:

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install Dependencies:

    pip install -r requirements.txt

    Configure Data: Place the GTFS data in the data/ folder as stops.txt, following the GTFS format.

Usage

    Start the Flask Application:

    flask run

    Access the Application: Open a browser and navigate to http://127.0.0.1:5000 to view the map interface.

    Using the Application:
        Select a stop on the map and click "Calculate Isochrone" to view travel time isochrones based on the selected mode of transportation.

Modules

    stop_loader.py: Handles loading and grouping of stops based on proximity.
    isochrone_calculator.py: Performs isochrone calculations using network analysis.
    utils.py: Contains helper functions used by other modules, such as distance calculations.

Scripts

Auxiliary scripts for data pre-processing are located in the scripts/ directory:

    analyze_time_precision.py: Checks the precision of time data in the GTFS file.
    create_geojson.py and create_geojson_simplified.py: Convert stop data to GeoJSON format.
    precompute_travel_times.py: Precomputes travel times between stops, storing them for efficient real-time access.

Future Development

    Precomputed Data Storage: Implement a storage solution for precomputed stop clusters and travel times to improve real-time performance.
    Documentation: Add detailed documentation for each module and script.

Contributing

Contributions are welcome! To collaborate:

    Fork the repository.
    Create a new branch for your feature or bug fix.
    Commit your changes and push the branch to GitHub.
    Open a pull request for review.

Please follow best practices for coding and documentation, and keep each pull request focused on a single feature or fix.
License

This project is licensed under the MIT License. See the LICENSE file for details.