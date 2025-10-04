from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app as fastapi_app

handler = Mangum(fastapi_app, lifespan="off")

def handler_wrapper(event, context):
    return handler(event, context)
