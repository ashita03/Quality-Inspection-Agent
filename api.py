import shutil
import uuid
from pathlib import Path

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from agent.db import init_db, get_connection
from agent.graph import build_graph

from fastapi.staticfiles import StaticFiles

app = FastAPI(title="QC Agent API")

# React's dev server runs on a different port than FastAPI, so the browser
# will block requests unless we explicitly allow that origin here.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default dev port
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploaded_images")
UPLOAD_DIR.mkdir(exist_ok=True)
app.mount("/images", StaticFiles(directory=UPLOAD_DIR), name="images")

graph = build_graph()


@app.on_event("startup")
def startup():
    init_db()


@app.post("/inspect")
async def inspect(file: UploadFile = File(...), part_id: str = "UNKNOWN"):
    # save the uploaded file to disk first, since our graph expects a path,
    # not raw bytes in memory
    ext = Path(file.filename).suffix or ".jpg"
    saved_path = UPLOAD_DIR / f"{uuid.uuid4().hex}{ext}"

    with open(saved_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    initial_state = {
        "image_path": str(saved_path),
        "part_id": part_id,
        "reasoning_trace": [],
    }

    result = graph.invoke(initial_state)

    return {
        "part_id": result["part_id"],
        "verdict": result["verdict"],
        "defect_type": result.get("defect_type"),
        "confidence": result.get("confidence"),
        "notes": result.get("notes"),
        "equipment_type": result.get("equipment_type"),
        "image_url": f"/images/{saved_path.name}",
        "reasoning_trace": result["reasoning_trace"],
    }


@app.get("/history")
def history(limit: int = 50):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM inspections ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()

    results = []
    for row in rows:
        item = dict(row)
        if item.get("image_path"):
            filename = Path(item["image_path"]).name
            item["image_url"] = f"/images/{filename}"
        results.append(item)
    return results


@app.get("/stats")
def stats():
    conn = get_connection()
    rows = conn.execute("SELECT verdict, defect_type FROM inspections").fetchall()
    conn.close()

    verdict_counts = {}
    defect_counts = {}

    for row in rows:
        verdict_counts[row["verdict"]] = verdict_counts.get(row["verdict"], 0) + 1
        if row["defect_type"] and row["defect_type"] != "none":
            defect_counts[row["defect_type"]] = defect_counts.get(row["defect_type"], 0) + 1

    return {
        "total_inspections": len(rows),
        "verdict_counts": verdict_counts,
        "defect_type_counts": defect_counts,
    }