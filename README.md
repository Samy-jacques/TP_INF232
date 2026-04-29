# California Housing Analytics Platform

An interactive data collection and visualization platform built around the California Housing dataset. This application allows users to submit their own housing data, view dynamic charts, and perform live Machine Learning regression analysis to predict housing values.

## ✨ Features
* **Interactive Dashboard:** View rich data visualizations of the housing market (powered by Chart.js/Plotly).
* **Live Machine Learning:** Uses Scikit-Learn for real-time linear regression on the dataset.
* **Data Collection:** Securely submit and validate new housing data to expand the dataset.
* **REST API:** Fully documented `/docs` built-in using FastAPI.
* **Cloud Ready:** Setup for simple cloud deployment to Render.

## 🛠️ Tech Stack
* **Backend:** [FastAPI](https://fastapi.tiangolo.com/), Python 3.12 
* **Database:** SQLite (managed via SQLAlchemy)
* **Frontend:** Jinja2 Templates, HTML/Vanilla CSS (Tailwind)
* **Data Science:** Pandas, NumPy, Scikit-learn
* **Server:** Uvicorn

---

## 💻 How to Use (Local Development)

### 1. Prerequisites
Make sure you have **Python 3.12+** installed on your system.

### 2. Setup the Environment
Clone the repository and install the dependencies:
```bash
# Create a virtual environment (recommended)
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 3. Run the Application
Start the Uvicorn development server:
```bash
python3 main.py
# Or alternatively:
# uvicorn main:app --reload
```

### 4. Open the App
* **Web UI:** Visit [http://localhost:8000](http://localhost:8000) in your browser.
* **API Documentation:** Visit [http://localhost:8000/docs](http://localhost:8000/docs) to view and interact with the Swagger API endpoints.

---

## 🚀 Deployment (Render)
This project is configured right out of the box for deployment on Render.

1. Create a **New Web Service** on Render.
2. Connect this GitHub repository.
3. Use the following configuration:
   * **Language:** Python
   * **Build Command:** `pip install -r requirements.txt`
   * **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Deploy!

*(Note: The project includes a `.python-version` file specifying Python 3.12.3 to ensure clean build dependency resolution on Render's side).*
