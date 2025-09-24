# IAGOS Atmospheric Data Download Tool - ENVRI-ID Token Introspection Demo

A Python demonstration tool showing ENVRI-ID token introspection by the AERIS SSO system through downloading and analyzing IAGOS (In-service Aircraft for a Global Observing System) atmospheric data from the SEDOO API.

## Purpose

This code demonstrates **ENVRI-ID token introspection** by the **AERIS SSO** system. It shows how ENVRI-ID tokens are validated and used to access protected AERIS resources through the SEDOO API.

## Features

- **Token Introspection Demo**: Shows ENVRI-ID token validation by AERIS SSO
- **Dual Authentication**: Manual token input or OAuth2 device flow for ENVRI-ID
- **AERIS API Integration**: Demonstrates token-based access to SEDOO backend
- **Data Download**: Retrieve NetCDF files as proof of successful authentication
- **Data Analysis**: Jupyter notebook for ozone timeseries visualization

## Project Structure

```
iagos-envri-introspection/
├── src/iagos_envri/          # Main package
│   ├── __init__.py           # Package initialization
│   └── iagos_introspection.py # Core introspection module
├── examples/                 # Example notebooks and scripts
│   └── iagos_ozone_analysis.ipynb
├── docs/                     # Documentation
├── tests/                    # Test suite (optional)
├── pyproject.toml           # Modern Python packaging
├── environment.yml          # Conda environment
├── README.md               # This file
└── CLAUDE.md               # Development guidance
```

## Installation

### Development Installation

```bash
# Clone and install in development mode
git clone <repo-url>
cd iagos-envri-introspection
conda env create -f environment.yml
conda activate iagos-envri
pip install -e .
```

### Using Conda Only

```bash
conda env create -f environment.yml
conda activate iagos-envri
```

### Manual Installation

```bash
pip install -e .
# or for minimal install:
pip install requests numpy pandas matplotlib xarray netcdf4 jupyter
```

## Usage

### Command Line Interface

```bash
# Using the installed script
iagos-download

# Or running the module directly
python -m iagos_envri.iagos_introspection

# Or running from src directory
python src/iagos_envri/iagos_introspection.py
```

The script will prompt for authentication and download sample flight data to `/tmp/`.

### Jupyter Notebook

Launch the analysis notebook:

```bash
jupyter notebook examples/iagos_ozone_analysis.ipynb
```

The notebook demonstrates:
- OAuth2 authentication flow
- NetCDF data loading with xarray
- Ozone timeseries visualization
- Statistical analysis of atmospheric data

## Authentication & Token Introspection

This demonstration shows how AERIS SSO performs ENVRI-ID token introspection:

### Manual Token (getHeader)
- Prompts for ENVRI-ID token input
- Token is validated by AERIS SSO when accessing SEDOO API
- Demonstrates direct bearer token introspection

### OAuth2 Device Flow (getHeaderOAuth)
- Browser-based ENVRI-ID authentication
- Device authorization grant flow via ENVRI staging environment
- Shows full OAuth2 token lifecycle and introspection by AERIS

## API Details

- **Service URL**: `https://api.sedoo.fr/iagos-backend-test/v2.0/downloads`
- **Authentication**: ENVRI-ID OAuth2
- **Data Format**: NetCDF level 2 timeseries
- **Output**: `{flight_id}.nc` files

## Key Files

- `src/iagos_envri/iagos_introspection.py` - Main download script
- `examples/iagos_ozone_analysis.ipynb` - Data analysis notebook
- `pyproject.toml` - Modern Python packaging configuration
- `environment.yml` - Conda environment specification
- `CLAUDE.md` - Development guidance

## Example

```python
from iagos_envri import downloadOneFlight

# Download with OAuth2
downloadOneFlight("2023050203041714", "/tmp/", use_oauth=True)
```

## Data Variables

The NetCDF files contain atmospheric measurements including:
- Ozone mixing ratio (O3_P1)
- Carbon monoxide (CO_P1)
- Air temperature and pressure
- Wind speed and direction
- Aircraft altitude and position

## Requirements

- Python ≥ 3.8
- Active ENVRI-ID account for authentication
- Internet connection for API access