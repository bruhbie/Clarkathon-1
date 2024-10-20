#site link: http://127.0.0.1:8000 or http://localhost:8000

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from surplus_tracker import Database  # Make sure this import works
from fastapi.responses import JSONResponse
import os

app = FastAPI(debug=True)

# Mount static files to access web dev stuff
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates for html rendering
templates = Jinja2Templates(directory="templates")

# Initialize database
db = Database()

shelters_data = [
    {
        "volunteering_orgs": "Posts on LinkedIn, individual interest groups (Nonprofit Volunteer Coordinators Community Outreach Programs, Local Worcester Area Groups), using hashtags: #volunteering, #nonprofit, #communityimpact, #worcesterma, #worcester, #tag orgs listed below+update data base+post free job postings for all listings",
        "names_of_shelters": "Abby's House",
        "contact_info": "52 High St. Worcester, MA 01609"
    },
    {
        "volunteering_orgs": "Rotary club",
        "names_of_shelters": "Net of Compassion",
        "contact_info": "674 Main St/674 Main St Worcester, MA 01610"
    },
    {

        "volunteering_orgs": "The center of hope",
        "names_of_shelters": "Shepherd's Place Willith Center",
        "contact_info": "44 Queen Street, Worcester, MA 01610"
    },
    {
        "volunteering_orgs": "Dismas house",
        "names_of_shelters": "The Salvation Army, Citadel Corps & Community Meal",
        "contact_info": "640 Main street, Worcester, MA 01608"
    },
    {
        "volunteering_orgs": "Worcester county food bank",
        "names_of_shelters": "Catholic Charities Worcester County",
        "contact_info": "10 Hammond Street, Worcester, MA 01610"
    },
    {
        "volunteering_orgs": "Rachel's Table",
        "names_of_shelters": "Rachel's Table",
        "contact_info": "(508) 799-7600"
    }
]

@app.exception_handler(Exception)
async def debug_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "detail": str(exc),
            "traceback": f"{exc.__class__.__name__}: {exc}"
        }
    )

@app.get("/test-image")
async def test_image():
    image_path = os.path.join("static", "images", "background.jpg")
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return Response(content=f.read(), media_type="image/jpeg")
    return {"error": "Image not found"}

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/data")
async def data(request: Request):
    alerts = db.get_active_alerts()
    return templates.TemplateResponse("data.html", {
        "request": request, 
        "shelters": shelters_data,
        "alerts": alerts
    })

@app.on_event("shutdown")
def shutdown_event():
    db.close()