import os
class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://shilpishuklajp:0Q8oKpebO3TNBuwf@cluster0.118s8.mongodb.net/ats-db")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

config = Config()
