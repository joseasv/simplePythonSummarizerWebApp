import random
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from typing import Annotated
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.summarizer import generate_summary
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:8888",
    "http://127.0.0.1:8888",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://localhost:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AIJob(BaseModel):
    fileParam: UploadFile = File(...)


@app.post("/process")
async def queue(job: Annotated[AIJob, Form()]):
    """
    Receives a text file and a question
    Returns random lines of a sustractive summarization of the text file
    """
    print("Queueing a job")
    print("fileParam", job.fileParam)

    contents = job.fileParam.file.read()
    try:
        with open(job.fileParam.filename, "wb") as f:
            f.write(contents)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")
    finally:
        job.fileParam.file.close()

    summary, original_length = generate_summary(str(contents), 5)
    print(summary)
    summary_lines = summary.strip().split(".")

    # pop last empty string
    summary_lines.pop()
    print(summary_lines)
    random_lines = random.randint(1, len(summary_lines) - 1)
    print("showing", random_lines, "random lines from", len(summary_lines), "lines")
    summary_random_lines = ".".join(random.sample(summary_lines, random_lines)).strip()
    # await fifo_queue.put(long_running_process2)
    print("task finished")

    return summary


def generate_openapi_schema():
    """
    Generate OpenAPI schema
    """
    return get_openapi(
        title="MiniLouie API",
        version="1.0.0",
        description="API for the MiniLoiue summarizer test",
        routes=app.routes,
    )


@app.get("/openapi.json")
def get_openapi_endpoint():
    """
    Retrieve the generated OpenAPI schema.
    """
    return JSONResponse(content=generate_openapi_schema())


app.mount("/", StaticFiles(directory="backend/dist", html=True))


@app.get("/")
async def read_root():
    """
    Returns the frontend
    """
    return FileResponse("dist/index.html")
