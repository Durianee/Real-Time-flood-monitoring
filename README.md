# Real-Time-flood-monitoring
# Flood Monitoring System

## Overview

This project is a Flood Monitoring System that retrieves and displays comprehensive monitoring station data from the UK Environment Agency's flood monitoring API. The system consists of:

- **Backend**: A Flask-based service that fetches and caches station data and historical readings (24-hour and 7-day periods) from the API.
- **Frontend**: A Vue 3 application built with Vuetify and Chart.js that:
  - Displays a list of monitoring stations with search and grouping (by river name) functionality.
  - Shows detailed information for each station including:
    - Basic station information (name, station reference, town, river name, date opened, status, etc.).
    - Measurement indicators (e.g., water level) with details (parameter, period, qualifier, unit).
    - Scale information (stageScale and downstageScale).
  - Visualizes historical water level readings as a line chart and displays the data in a table.
  - Provides a toggle to switch between 24-hour and 7-day historical data.

## Features

- **Station Information**  
  Retrieves comprehensive station data including:
  - Name (`label`), Station reference, Town, River name, Date opened, Status.
  - Additional identifiers such as RLOIid, notation, and wiskiID.
  - Geographical coordinates: latitude (`lat`), longitude (`long`), easting, and northing.
  - Catchment area name.
  
- **Measurement and Scale Data**  
  Displays measurement indicators for each station, including:
  - Measurement details (parameter, parameterName, period, qualifier, unitName).
  - Stage scale and downstage scale data for historical range information.

- **Historical Data Visualization**  
  Users can view historical water level readings for:
  - 24-hour period.
  - 7-day period.
  The data is visualized using a line chart (Chart.js) and also presented in a data table.

- **Search and Grouping**  
  The Station List page includes:
  - A search field to filter stations by name, town, or river.
  - Grouping options (currently by river name) to help users quickly locate a station.

## Installation

### Prerequisites

- **Backend**: Python 3.8+ (using a virtual environment is recommended)
- **Frontend**: Node.js and npm
- **Git**

### Backend Setup

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd water-monitoring-project/backend

2. **Create and Activate a Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
   
3. **Install Dependencies:** 
    ```nginx
    Flask
    Flask-Caching
    requests
Then run:
    ```bash
    pip install -r requirements.txt
    
4. **Run the Backend Service:**
    ```bash
    python server.py
The backend will be available at http://127.0.0.1:5000/.

### Frontend Setup
Navigate to the Frontend Folder:
    ```bash
    cd ../frontend
Install Dependencies:
    ```bash
    npm install
Start the Frontend Development Server:
    ```bash
    npm run dev
The frontend will be available at http://localhost:5173/.

### Usage
#### Station List Page:
The homepage displays a list of monitoring stations with a search field and grouping options (by river name). Users can filter the stations using the search box. Clicking on a station navigates to its detail page.
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/4d26c534-0a8c-4672-b263-82d43c0e6d6f" />


#### Station Detail Page:
The detail page shows the station's comprehensive information (name, town, river, date opened, status, etc.) along with:

A toggle to switch between 24-hour and 7-day historical reading data.
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/234f7fc2-457a-46f9-9613-03ca35f3d97e" />
<img width="1156" alt="image" src="https://github.com/user-attachments/assets/194d15ce-d878-49ae-a219-b540741d61df" />

A line chart displaying historical water level readings.
![1741748830743](https://github.com/user-attachments/assets/a322ebe8-4520-4080-b000-d332e186dc88)

A data table listing the historical readings with formatted date/time and water level values.
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/de95ca21-c9c0-4f4d-97cc-2993b71410ef" />

### Future Improvements
- **Map Functionality**: Reintroduce and enhance map features, such as:
  - Displaying interactive station markers on a map.
  - Pop-up details for each station when a marker is clicked.
  - Clustering of markers in densely populated areas.
  - Optional integration of a terrain view to provide context, especially for flood risk assessment.
- **Enhanced Filtering**: Add additional filters (e.g., by town or status) to further improve the station search functionality.
- **UI Enhancements**: Refine the user interface with improved layout, spacing, and responsive design.
- **Error Handling**: Implement more robust error handling and user feedback for failed API calls.


### Running the Application
After installation, run both the backend and frontend services. The frontend communicates with the backend via a proxy (configured in vite.config.js), so ensure both are running:

Backend: http://127.0.0.1:5000/
Frontend: http://localhost:5173/

### License
This uses Environment Agency flood and river level data from the real-time data API (Beta)

