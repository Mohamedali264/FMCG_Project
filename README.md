# FMCG Data Analysis Dashboard

A comprehensive data analysis and visualization dashboard built with Dash and Plotly, designed for FMCG (Fast-Moving Consumer Goods) data analysis. This application provides powerful tools for data exploration, visualization, and automated analysis.

## Features

### Home Page
- Main landing page with an overview of the dashboard
- Quick access to all features
- Modern and responsive design

### Visualization Page
- Interactive data visualizations using Plotly
- Customizable charts and graphs
- Real-time data updates

### YData Profiling
- Automated data profiling reports
- Comprehensive statistical analysis
- Data quality assessment
- Correlation analysis
- Distribution analysis

### Pygwalker Integration
- Interactive data exploration
- Drag-and-drop visualization creation
- Real-time data analysis
- Three main functions:
  - Display: Show current data
  - Clear: Reset the view
  - Generate: Create new visualizations

### Upload CSV
- Easy CSV file upload functionality
- Automatic data validation
- Seamless integration with other features
- Automatic data synchronization with YData Profiling and Pygwalker

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Mohamedali264/FMCG_Project.git
cd FMCG_Project
```

2. Create a virtual environment:
```bash
python -m venv .venv
```

3. Activate the virtual environment:
- Windows:
```bash
.venv\Scripts\activate
```
- Unix/MacOS:
```bash
source .venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Make sure your virtual environment is activated
2. Run the application:
```bash
python app.py
```
3. Open your web browser and navigate to `http://localhost:8050`

## Project Structure

```
├── app.py                 # Main application file
├── requirements.txt       # Project dependencies
├── config.py             # Configuration settings
├── assets/              # Static assets (images, CSS)
├── data/               # Data storage directory
├── pages/              # Page layouts
│   ├── home.py
│   └── upload_layout.py
├── visualizations/     # Visualization components
│   ├── charts.py
│   └── layout.py
├── profiling/         # Data profiling components
├── utils/            # Utility functions
└── exports/         # Export directory for reports
```

## Dependencies

The project uses several key libraries:
- Dash and Plotly for the web interface and visualizations
- YData Profiling for automated data analysis
- Pygwalker for interactive data exploration
- Pandas for data manipulation
- Various other supporting libraries (see requirements.txt)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Dash and Plotly for the visualization framework
- YData Profiling for automated data analysis
- Pygwalker for interactive data exploration 
# FMCG_Project
