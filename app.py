from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import algo

templates = Jinja2Templates(directory="")
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test")
async def test(request: Request):
    weights, updates = algo.init_weights()
    return templates.TemplateResponse('index.html', {'request': request, 'weights': weights, 'updates': updates})

@app.post("/distributed_dijkstra")
async def distributed_dijkstra(request: Request):
    form = await request.form()
    start = form['start']
    goal = form['goal']
    updates = form['updates']
    weights, updates = algo.init_weights(updates)
    parent, distance = algo.distributed_dijkstra(weights, start, goal)
    return algo.path(parent, goal), distance