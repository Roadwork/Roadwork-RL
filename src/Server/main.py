"""
server start
uvicorn --port 3000 main:app
"""

from fastapi import FastAPI
from dapr.ext.fastapi import DaprActor

# Import our servers
from OpenAI.server import ActorOpenAI


app = FastAPI(title=f'{ActorOpenAI.__name__}Service')

# Add Dapr Actor Extension
actor = DaprActor(app)

@app.on_event("startup")
async def startup_event():
    # Register DemoActor
    await actor.register_actor(ActorOpenAI)
