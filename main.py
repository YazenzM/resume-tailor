from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import difflib
import uvicorn
import mammoth
import fitz

app = FastAPI()
templates = Jinja2Templates(directory="templates")

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
    <p style="text-align: center;">Richardson, TX | Data Engineer | M.S. Business Analytics & AI</p>

    <h2>Experience</h2>
    <h3>Data Engineer | Zinzu</h3>
    <p><em>Current</em></p>
    <ul>
        <li>Develop and maintain backend scripts and data infrastructure to support core business operations.</li>
        <li>Implement automated pipelines for data extraction, transformation, and loading.</li>
    </ul>

    <h2>Projects</h2>
    <h3>GA4 Conversion Predictor</h3>
    <ul>
        <li>Engineered BigQuery SQL and PySpark scripts to flatten Google Analytics 4 event data.</li>
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

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    filename = file.filename.lower()
    
    if filename.endswith(".docx"):
        # Use mammoth with basic style mapping to preserve some structure
        style_map = (
            "p[style-name='Heading 1'] => h1:fresh\n"
            "p[style-name='Heading 2'] => h2:fresh\n"
            "p[style-name='Heading 3'] => h3:fresh"
        )
        result = mammoth.convert_to_html(file.file, style_map=style_map)
        return {"html": result.value}
        
    elif filename.endswith(".pdf"):
        pdf_bytes = await file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        # More structured PDF extraction attempting to preserve basic blocks
        html_content = ""
        for page in doc:
            blocks = page.get_text("blocks")
            for block in blocks:
                text = block[4].strip()
                if not text:
                    continue
                # Very basic heuristic for headers vs body
                if len(text) < 50 and not text.startswith("•") and not text.startswith("-"):
                    html_content += f"<h3>{text}</h3>"
                else:
                    # Convert bullet characters to actual lists (very naive)
                    if "•" in text:
                        items = [t.strip() for t in text.split("•") if t.strip()]
                        html_content += "<ul>"
                        for item in items:
                            html_content += f"<li>{item}</li>"
                        html_content += "</ul>"
                    else:
                        html_content += f"<p>{text.replace(chr(10), '<br>')}</p>"
            
        return {"html": html_content}
        
    else:
        return {"error": "Unsupported file type."}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)