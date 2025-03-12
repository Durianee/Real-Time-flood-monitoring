# Real-Time-flood-monitoring
Flood Monitoring System
Overview
This project is a Flood Monitoring System that retrieves and displays comprehensive monitoring station data from the UK Environment Agency's flood monitoring API. The system consists of:

Backend: A Flask-based service that fetches and caches station data and historical readings (24h and 7d) from the API.
Frontend: A Vue 3 application built with Vuetify and Chart.js that:
Displays a list of monitoring stations.
Provides filtering (by river name) and search functionality.
Shows detailed information for each station, including basic details and historical water level readings visualized as a line chart and in a data table.
Features
Station Information:
Retrieves comprehensive station data including:

Name (label)
Station reference
Town (if available)
River name
Date opened
Status
RLOIid, notation, and wiskiID
Geographical coordinates (latitude, longitude, easting, northing)
Catchment area name
Measurement indicators (e.g., Water Level) with details such as parameter name, period, qualifier, and unit name
Stage scale and downstage scale (quantitative limits)
Historical Data Visualization:
Users can view historical water level readings for:

24-hour period
7-day period
The readings are presented in a line chart (using Chart.js) and a data table for detailed analysis.
Search and Grouping:
On the station list page, users can filter the stations by name or group them by river name (with the option to group by town removed for simplicity).

Installation
Prerequisites
Backend: Python 3.8+ (using a virtual environment is recommended)
Frontend: Node.js and npm
Git
Backend Setup
Clone the repository:
bash
复制
git clone <repository-url>
cd water-monitoring-project/backend
Create and activate a virtual environment:
bash
复制
python3 -m venv venv
source venv/bin/activate   # (On Windows: venv\Scripts\activate)
Install the required Python packages:
bash
复制
pip install -r requirements.txt
The requirements.txt file should include:
nginx
复制
Flask
Flask-Caching
requests
Run the backend service:
bash
复制
python server.py
The backend will be available at http://127.0.0.1:5000/.
Frontend Setup
Navigate to the frontend folder:
bash
复制
cd ../frontend
Install npm dependencies:
bash
复制
npm install
Start the frontend development server:
bash
复制
npm run dev
The frontend will be available at http://localhost:5173/.
Usage
Station List Page:
The homepage displays a list of monitoring stations with a search field and grouping options (by river name). Clicking a station navigates to its detail page.

Station Detail Page:
The detail page shows the station's complete information along with a toggle to switch between 24-hour and 7-day historical reading data. The readings are visualized as a line chart and are also presented in a data table.

Screenshots
(Optional: You may add screenshots of the Station List, Station Detail with chart, and filtering functionality. Alternatively, instruct the reviewer to run the project locally to see the functionality in action.)

Future Improvements
Enhanced Filtering: Add additional filters (e.g., by town or status) to further improve search functionality.
UI Enhancements: Refine the user interface for a cleaner, more responsive design.
Error Handling: Implement more robust error handling and user feedback in case of API failures.
Additional Visualizations: Consider incorporating more statistical insights and additional charts.
Running the Application
After installation, run both backend and frontend services. The frontend communicates with the backend via a proxy (configured in vite.config.js), so ensure both are running.

Backend: http://127.0.0.1:5000/
Frontend: http://localhost:5173/
Contributing
Contributions and improvements are welcome. Please fork the repository and create a pull request with your changes.

License
This project is licensed under the Open Government Licence v3.0.
