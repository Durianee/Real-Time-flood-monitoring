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
- Git

### Backend Setup

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd water-monitoring-project/backend
