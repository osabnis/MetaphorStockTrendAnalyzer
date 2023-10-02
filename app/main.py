# IMPORTING PACKAGES
from fastapi import FastAPI
import uvicorn
from app.routers import trend_analysis

# INITIALIZATION OF THE FASTAPI APP OBJECT
app = FastAPI(title="Stock Trend Analyzer and Recommender API 😊",
              description="This API will host all the endpoints for you to make informed decisions about your Financial Portfolio!")

# INCLUDE THE TREND ANALYSIS ROUTER TO THE API
app.include_router(trend_analysis.router)

# MAIN FUNCTION
if __name__ == "__main__":
    # RUNNING THE APP - CAN BE FOUND AT http://localhost:8000/docs!
    uvicorn.run(app, host="0.0.0.0", port=8000)
