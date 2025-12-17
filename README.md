# ETL-LIVE_API

## Overview

ETL-LIVE_API is a production-ready **Extract-Transform-Load (ETL)** pipeline that automates the collection, processing, and storage of real-time weather data and astronomical imagery. Built with modern Python technologies, this project demonstrates industry best practices for data engineering, API integration, and cloud database management.

### Key Features

- **Multi-Source Data Integration**: Extracts data from NASA APOD and Open-Meteo weather APIs
- **Real-Time Data Processing**: Transforms raw API responses into structured, analyzable formats
- **Cloud Database Integration**: Loads processed data into Supabase (PostgreSQL-based)
- **Automated Pipeline**: Modular, reusable scripts for seamless data orchestration
- **Environment Configuration**: Secure credential management using `.env` files
- **Scalable Architecture**: Batch processing with configurable intervals

---

## Project Structure

```
ETL-LIVE_API/
├── scripts/               # ETL pipeline modules
│   ├── extract_nasa.py          # Extract NASA APOD (Astronomy Picture of the Day)
│   ├── extract_weather.py       # Extract weather data from Open-Meteo API
│   ├── transform_weather.py     # Clean and structure weather data
│   └── load_weather.py         # Load data to Supabase database
├── data/                  # Data storage
│   ├── raw/                   # Raw JSON responses from APIs
│   └── staged/                # Cleaned and transformed data (CSV)
├── .env                   # Environment variables (credentials)
└── README.md              # Project documentation
```

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| **Language** | Python 3.x |
| **APIs** | NASA APOD API, Open-Meteo Weather API |
| **Data Processing** | Pandas, JSON |
| **Database** | Supabase (PostgreSQL) |
| **Libraries** | requests, python-dotenv, glob |
| **Environment Management** | python-dotenv |

---

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Supabase account and credentials
- NASA API key (free from [NASA API](https://api.nasa.gov/))

### Step 1: Clone the Repository

```bash
git clone https://github.com/Abhinav7301/ETL-LIVE_API.git
cd ETL-LIVE_API
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
```
pandas>=1.3.0
requests>=2.26.0
python-dotenv>=0.19.0
supabase>=1.0.0
```

### Step 4: Configure Environment Variables

Create a `.env` file in the root directory:

```env
NASA_KEY=your_nasa_api_key_here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_key_here
```

**Obtaining Credentials:**
- **NASA API Key**: Register at [https://api.nasa.gov/](https://api.nasa.gov/)
- **Supabase Credentials**: Create a project at [https://supabase.com](https://supabase.com)

---

## Pipeline Workflow

### 1. **Extract Phase**

#### `extract_nasa.py`
Fetches the Astronomy Picture of the Day from NASA API and saves as JSON.

```bash
python scripts/extract_nasa.py
```

**Output**: `data/raw/nasa_apod_YYYYMMDD_HHMMSS.json`

#### `extract_weather.py`
Retrieves hourly weather data for specified location (default: Hyderabad, India).

**Parameters:**
- `lat` (float): Latitude (default: 17.3850)
- `Lon` (float): Longitude (default: 78.486)
- `days` (int): Forecast days (default: 1)

```bash
python scripts/extract_weather.py
```

**Output**: `data/raw/weather_YYYYMMDD_HHMMSS.json`

### 2. **Transform Phase**

#### `transform_weather.py`
Cleans and structures weather JSON data into CSV format.

**Transformations:**
- Converts timestamps to standardized format
- Renames fields for clarity (e.g., `temperature_2m` → `temperature_C`)
- Adds metadata (city, extraction timestamp)
- Handles missing values

```bash
python scripts/transform_weather.py
```

**Output**: `data/staged/weather_cleaned.csv`

**Sample Output:**
```csv
time,temperature_C,humidity_percent,wind_speed_kmph,city,extracted_at
2025-12-17T00:00,18.5,65,12.3,Hyderabad,2025-12-17T21:30:45
2025-12-17T01:00,17.2,68,11.8,Hyderabad,2025-12-17T21:30:45
```

### 3. **Load Phase**

#### `load_weather.py`
Loads cleaned data into Supabase database with batch processing.

**Features:**
- Batch insert (default: 20 records per batch)
- Automatic timestamp conversion
- NULL value handling
- Rate limiting (0.5s between batches)

```bash
python scripts/load_weather.py
```

**Database Table Schema:**
```sql
CREATE TABLE weather_data (
    id BIGSERIAL PRIMARY KEY,
    time TIMESTAMP,
    temperature_c NUMERIC,
    humidity_percent NUMERIC,
    wind_speed_kmph NUMERIC,
    city VARCHAR(100),
    extracted_at TIMESTAMP
);
```

---

## Usage Examples

### Run Complete ETL Pipeline

```bash
# Extract
python scripts/extract_weather.py

# Transform
python scripts/transform_weather.py

# Load
python scripts/load_weather.py
```

### Extract NASA APOD Data

```bash
python scripts/extract_nasa.py
```

### Custom Weather Location

Modify parameters in `extract_weather.py`:

```python
extract_weather_data(lat=40.7128, Lon=-74.0060, days=7)  # New York, 7-day forecast
```

---

## Configuration

### Weather API Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `latitude` | float | 17.3850 | Location latitude |
| `longitude` | float | 78.486 | Location longitude |
| `hourly` | string | temperature_2m, relative_humidity_2m, wind_speed_10m | Metrics to fetch |
| `forecast_days` | int | 1 | Number of forecast days |
| `timezone` | string | "auto" | Timezone (auto-detect) |

### Batch Processing Settings

Edit `load_weather.py` to adjust batch size:

```python
batch_size = 20  # Records per batch (adjust as needed)
```

---

## Error Handling

### Common Issues & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `FileNotFoundError: Missing file: ...` | Missing data file | Run extract and transform steps |
| `ConnectionError: Failed to fetch API` | Network/API issue | Check internet connection and API credentials |
| `Invalid SUPABASE_URL` | Missing environment variable | Verify `.env` configuration |
| `INSERT statement failed` | Database constraint violation | Check table schema in Supabase |

---

## Performance & Optimization

- **Batch Processing**: Reduces database load with 20-record batches
- **Rate Limiting**: 0.5s delay between batches prevents server overload
- **Memory Efficiency**: Processes data without loading entire datasets into memory
- **Scalability**: Architecture supports hourly/daily automated runs via cron jobs or cloud schedulers

---

## Security Considerations

1. **Never commit `.env` file** to version control
2. **Use Supabase RLS (Row Level Security)** for production
3. **Rotate API keys** periodically
4. **Encrypt sensitive data** in transit (HTTPS/TLS)
5. **Monitor logs** for unauthorized access attempts

---

## Future Enhancements

- [ ] Add data quality validation and error logging
- [ ] Implement Apache Airflow for workflow orchestration
- [ ] Support multiple locations with geographic sharding
- [ ] Add data visualization dashboard (Grafana/Tableau)
- [ ] Implement CI/CD pipeline with GitHub Actions
- [ ] Add unit tests and integration tests
- [ ] Support incremental data loading
- [ ] Add backup and disaster recovery procedures

---

## Deployment

### Deploy to Cloud (Example: Heroku)

```bash
# Create Procfile
echo "worker: python scripts/load_weather.py" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

### Schedule with GitHub Actions

Create `.github/workflows/etl-schedule.yml`:

```yaml
name: ETL Pipeline
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
jobs:
  etl:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run ETL
        run: |
          pip install -r requirements.txt
          python scripts/extract_weather.py
          python scripts/transform_weather.py
          python scripts/load_weather.py
```

---

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the **MIT License** - see the LICENSE file for details.

---

## Contact & Support

- **Author**: Abhinav7301
- **GitHub**: [Abhinav7301/ETL-LIVE_API](https://github.com/Abhinav7301/ETL-LIVE_API)
- **Issues**: [Report a bug](https://github.com/Abhinav7301/ETL-LIVE_API/issues)
- **Discussions**: [Start a discussion](https://github.com/Abhinav7301/ETL-LIVE_API/discussions)

---

## Acknowledgments

- [NASA API](https://api.nasa.gov/) - Astronomy Picture of the Day
- [Open-Meteo](https://open-meteo.com/) - Free weather API
- [Supabase](https://supabase.com/) - PostgreSQL platform
- [Pandas](https://pandas.pydata.org/) - Data manipulation library

---

**Last Updated**: December 2025
