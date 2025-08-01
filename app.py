import sys, os, certifi
from dotenv import load_dotenv
import pymongo
import pandas as pd

from networksecurity.logging_exception.exception import CustomException
from networksecurity.logging_exception.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils import main_utils, ml_utils

from networksecurity.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME, DATA_INGESTION_DATABASE_NAME

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

# Setting up database connection
ca = certifi.where()
load_dotenv()
mongo_db_url = os.getenv("MONGODB_URL_KEY")
client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

# Setting up FastAPI
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setting up routes 
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful!")
    except Exception as e:
            custom_err = CustomException(e, sys)
            logging.error(custom_err)
            raise custom_err
    
@app.post("/predict")
async def predict_route(request: Request,file: UploadFile = File(...)):
    try:
        df=pd.read_csv(file.file)
        network_model=main_utils.load_object("final_model/model.pkl")
        print(df.iloc[0])
        y_pred = network_model.predict(df)
        print(y_pred)
        df['predicted_column'] = y_pred
        print(df['predicted_column'])
        #df['predicted_column'].replace(-1, 0)
        #return df.to_json()
        
        # Save to local folder and S3 bucket
        ml_utils.sync_prediction_dir_to_s3(df)
        
        table_html = df.to_html(classes='table table-striped')
        #print(table_html)
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
        
    except Exception as e:
            custom_err = CustomException(e, sys)
            logging.error(custom_err)
            raise custom_err


#Running the app
if __name__ == "__main__":
    app_run(app,host="0.0.0.0", port=8000)