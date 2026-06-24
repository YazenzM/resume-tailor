from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Mock AI function targeting specific HTML nodes and assigning unique Edit IDs
def mock_ai_html_edit(html_content: str) -> str:
    # 1. Change a Section Header (Edit ID: 1)
    html_content = html_content.replace(
        "<h2>Skills</h2>",
        "<h2><del data-edit-id='1' class='ai-remove'>Skills</del><ins data-edit-id='1' class='ai-add'>Core Competencies</ins></h2>"
    )
    
    # 2. Change a Job Title Header (Edit ID: 2)
    html_content = html_content.replace(
        "<h3>Data Engineer | Zinzu</h3>",
        "<h3><del data-edit-id='2' class='ai-remove'>Data Engineer</del><ins data-edit-id='2' class='ai-add'>Backend Data Engineer</ins> | Zinzu</h3>"
    )
    
    # 3. Change a specific bullet point (Edit ID: 3)
    html_content = html_content.replace(
        "<li>Develop and maintain backend scripts and data infrastructure to support core business operations.</li>",
        "<li><del data-edit-id='3' class='ai-remove'>Develop and maintain backend scripts and data infrastructure to support core business operations.</del><ins data-edit-id='3' class='ai-add'>Architected scalable backend pipelines using Python to optimize core business operations.</ins></li>"
    )
    
    return html_content

@app.get("/", response_class=HTMLResponse)
async def editor_ui(request: Request):
    initial_document = """
    <h1 style="text-align: center;">Yaseen Mohammed</h1>
    <p style="text-align: center;">Richardson, TX | Data Engineer</p>

    <h2>Skills</h2>
    <ul>
        <li>Python, PySpark, SQL, BigQuery</li>
    </ul>

    <h2>Experience</h2>
    <h3>Data Engineer | Zinzu</h3>
    <ul>
        <li>Develop and maintain backend scripts and data infrastructure to support core business operations.</li>
    </ul>

    <h2>Projects</h2>
    <h3>GA4 Conversion Predictor</h3>
    <ul>
        <li>Built predictive models to forecast user conversion based on behavioral navigation paths.</li>
    </ul>
    """
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"content": initial_document}
    )

@app.post("/tailor")
async def tailor_document(request: Request, document: str = Form(...), job_description: str = Form(...)):
    tailored_html = mock_ai_html_edit(document)
    return {"html": tailored_html}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)