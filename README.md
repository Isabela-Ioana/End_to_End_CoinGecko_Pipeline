# 🛠️ Data Pipeline: Crypto Market Monitor

## 🎯 Project Objective

This project demonstrates the construction of a complete and robust **Time-Series Data Engineering Pipeline**, designed to be automated and fully containerized. The core goal is to continuously collect historical cryptocurrency market data and store it in a scalable **Data Mart**, effectively eliminating dependence on static files like csv and local desktop BI tools.

## ⚙️ Architecture (Technology Stack)

The project utilizes a modern and isolated technology stack, which is critical for production environments:

| Component | Technology | Role in the Pipeline |
| :--- | :-------------: | :--- |
| **Containerization** | `Docker` & `Docker Compose` | Isolates the database, ensures portability, and simplifies deployment. |
| **Ingestion/ETL** | `Python` (Pandas, SQLAlchemy) | Extracts data from the API, cleanses it, and continuously loads it. |
| **Storage (Data Mart)** | `PostgreSQL` | Provides a stable and scalable repository for collecting and querying the time-series history. |
| **Data Source** | CoinGecko API | Supplies real-time market data (price, market cap, etc.). |
| **Consumption** *in progress* | Streamlit | Dynamic frontend for visualizing the collected historical data. |

---



## 🚀 How to Run the Project Locally

### Prerequisites

1.  **Docker Desktop:** Installed and running.
2.  **Python 3.x:** Installed.

### 1. Configuration of Python environment and dependencies


1.  **Create and activate a virtual environment:**

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure the env (`.env`):**
    Copy the document `*.env.example*` and rename it in **`.env`** to upload environment variables.

### 2. Launching the Infrastructure (PostgreSQL)

```bash
# Stars the PostgreSQL container in detached mode (-d)
docker-compose up -d