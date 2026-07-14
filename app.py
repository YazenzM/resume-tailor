import streamlit as st
import json
import os
import base64
import datetime

try:
    from dotenv import load_dotenv, find_dotenv
    # find_dotenv() aggressively looks for the .env file in parent directories
    load_dotenv(find_dotenv())
except ImportError:
    st.warning("python-dotenv is not installed. To auto-load API keys from a .env file, run: pip install python-dotenv")
    pass

try:
    import typst
except ImportError:
    st.error("Please install typst: pip install typst")
try:
    import anthropic
except ImportError:
    st.error("Please install anthropic: pip install anthropic")

# ==========================================
# 1. DATA CONFIGURATION
# ==========================================
MASTER_DATA = {
    "basics": {
        "name": "Yaseen Mohammed",
        "title": "Data Engineer & Analyst",
        "location": "Plano, Texas, 75074",
        "contact": "469-512-0058 | Yaseenam3@gmail.com | linkedin.com/in/yaseenam"
    },
    "education": [
        {
            "school": "The University of Texas at Dallas",
            "degree": "Master of Science, Business Analytics and Artificial Intelligence",
            "date": "May 2026"
        },
        {
            "school": "The University of Texas at Dallas",
            "degree": "Bachelor of Science, Data Science",
            "date": "December 2023"
        }
    ],
    "skills": [
        {"category": "Certifications", "details": "AWS Certified Machine Learning, Microsoft Azure Data Scientist Associate."},
        {"category": "Analysis Tools", "details": "PowerBI, Tableau, MS Excel, RStudio, Scikit-learn"},
        {"category": "Programming", "details": "SQL, Python, R, Scala, Java, C++, HTML/CSS, JavaScript"},
        {"category": "Data Science", "details": "Business Analytics & Statistical Analysis, Machine Learning, Data Exploration, Feature Engineering, Data Transformation & Visualization, Recommender Systems, Natural Language Processing"},
        {"category": "Data Tools", "details": "Spark, Hadoop, MySQL, AWS infrastructure, MongoDB, Azure infrastructure"}
    ],
    "experience": [
        {
            "company": "Zinzu, Redmond, WA",
            "title": "Data Engineer",
            "date": "March 2024 - Present",
            "bullets": [
                "Engineered data infrastructure using Azure services (SQL, NoSQL, Cosmos DB, Blob Storage) to support 70% of operational data, improving efficiency and scalability.",
                "Automated frontend and backend server creation and maintenance, increasing operational efficiency by 60% through Bash scripts and Azure services for load balancing and GitHub integration.",
                "Developed RESTful APIs and implemented backend servers to support website and app functionality, enhancing user experience with streamlined UX designs.",
                "Integrated natural language analytics using GPT API for custom data insights, enabling user-friendly and adaptive analytics.",
                "Researched geospatial analytics features for the platform, compiling a detailed 21-page report on use cases, benefits, implementation strategies, and competitive analysis, presented to the CEO for strategic planning.",
                "Optimized big data processing by implementing Apache Spark, improving processing speed and reducing server latency issues.",
                "Reduced server manual task time by 70% through automated maintenance processes, leveraging Bash scripts, Azure Monitor, and GitHub for continuous deployment.",
                "Engineered SQL prompts in order to derive statistics and insight from web data."
            ]
        },
        {
            "company": "Standard Aero, Dallas, TX",
            "title": "Business Analyst",
            "date": "February 2025 - August 2025",
            "bullets": [
                "Developed and maintained Power BI dashboards to support cross-departmental reporting, enabling leads to monitor individual employee performance and managers to track department-level KPIs.",
                "Collaborated with multiple departments to gather business requirements and translate them into actionable reporting solutions.",
                "Enhanced financial visibility by updating the billing report with quarterly budgets and performance targets, delivering insights into company financial health through dynamic KPIs.",
                "Designed and implemented robust data pipelines between Snowflake and Oracle databases, using advanced SQL transformations to prepare data for reporting and analytics.",
                "Managed Power BI security roles to ensure secure access to role-based reports, allowing leads and managers to view only relevant performance metrics.",
                "Applied predictive statistical techniques to forecast KPIs and ensure alignment with company performance goals."
            ]
        },
        {
            "company": "Autix Automotive, Dallas, TX",
            "title": "Data Scientist Intern",
            "date": "August 2023 - December 2023",
            "bullets": [
                "Improved predictive ML model accuracy by 70%, using Scikit-learn, XGBoost, and ensemble methods to optimize car price prediction models.",
                "Developed NLP-based text extraction workflows using GPT API, converting unstructured car descriptions into structured data, boosting dataset predictive power by 30%, and saving $80k in external software costs.",
                "Built data pipelines for collecting and cleaning data from web scraping sources, storing results in Azure Blob Storage for scalability and reliability.",
                "Engineered custom ML models for different price points of cars, from luxury to affordable, ensuring targeted and precise predictions.",
                "Led a team through model development, data preprocessing, and pipeline creation, ensuring efficient collaboration and task execution."
            ]
        },
        {
            "company": "Vital Synapses, Dallas, TX",
            "title": "Data Science Intern",
            "date": "May 2023 – August 2023",
            "bullets": [
                "Created a data pipeline for processing healthcare insurance claims, automating data extraction, cleaning, and transformation for streamlined analytics.",
                "Developed 10+ dashboards in PowerBI, visualizing relationships between claim processing times and factors such as symptoms and diagnoses.",
                "Applied statistical methods (e.g., regression, hypothesis testing) to diagnose lead times for 70% of insurance claims, uncovering patterns and root causes of delays.",
                "Addressed incomplete and inconsistent data through tailored imputation techniques using linear regression, ensuring reliable and standardized datasets for analysis.",
                "Optimized insights from healthcare data by integrating statistical models and dynamic dashboards, enabling stakeholders to make informed decisions."
            ]
        },
        {
            "company": "Pricesenz, Dallas, TX",
            "title": "Research Analyst",
            "date": "May 2022 – August 2022",
            "bullets": [
                "Led a team of three interns to evaluate $10k+ worth of BI tools, including PowerBI, Tableau, Zapier, and AWS, compiling a detailed report on features, integration, pricing, and recommendations for stakeholders.",
                "Implemented a data pipeline from the company’s CRM to PowerBI, enabling seamless KPI dashboard creation with 40+ data points, providing actionable insights for multiple departments.",
                "Developed customized KPI dashboards aligned with business goals, visualizing key metrics and improving decision-making efficiency across teams.",
                "Negotiated with vendors for BI tools, securing cost-effective solutions tailored to company requirements.",
                "Resolved data inconsistencies between CRM and PowerBI by implementing robust data cleaning and transformation steps, ensuring reliable and accurate insights."
            ]
        }
    ],
    "projects": [
        {
            "title": "Rice Health Policy Hackathon",
            "subtitle": "Houston, TX | July 2023",
            "bullets": [
                "Co-authored an 8-page policy research paper on improving vaccine reporting by integrating ImmTrac2 into Texas’s Health Information Exchange (HIE), projecting a 30% increase in efficiency.",
                "Collaborated with healthcare professionals to identify inefficiencies in current immunization record-keeping processes, proposing technology-driven solutions.",
                "Analyzed immunization data to uncover bottlenecks, recommending streamlined record-sharing to reduce redundant vaccinations.",
                "Presented findings to district judges, showcasing actionable strategies and addressing questions from judges and peers among a competitive cohort of 100+ participants."
            ]
        },
        {
            "title": "ASA Data fest 2023",
            "subtitle": "SMU | March 2023",
            "bullets": [
                "Awarded 3rd place for analyzing 10GB of data across 8 datasets, uncovering trends in pro bono legal cases for the ABA Foundation.",
                "Performed exploratory data analysis (EDA) in R, using heat maps and distribution graphs to identify location-specific challenges, such as high failure rates in Mississippi.",
                "Built a multiple linear regression model using NLP-extracted features, achieving 90% accuracy in predicting pro bono case success based on response times and urgency indicators.",
                "Managed large datasets efficiently by segmenting data and leveraging R’s visualization tools, revealing critical insights to improve legal system outcomes."
            ]
        }
    ]
}

# ==========================================
# 2. STATE MANAGEMENT & TRACKING
# ==========================================
TRACKER_FILE = "job_tracker.json"
RESUME_DIR = "saved_resumes"

def init_state():
    """Initializes Streamlit session state with master data."""
    if 'initialized' not in st.session_state:
        # Init basics
        st.session_state['basics_name'] = MASTER_DATA['basics']['name']
        st.session_state['basics_title'] = MASTER_DATA['basics']['title']
        st.session_state['basics_location'] = MASTER_DATA['basics']['location']
        st.session_state['basics_contact'] = MASTER_DATA['basics']['contact']
        
        # Init Job Tracking Fields
        st.session_state['job_description'] = ""
        st.session_state['company_name'] = ""
        st.session_state['job_title'] = ""

        # Init Education and Skills
        for i, edu in enumerate(MASTER_DATA['education']):
            st.session_state[f"edu_{i}_school"] = edu['school']
            st.session_state[f"edu_{i}_degree"] = edu['degree']
            st.session_state[f"edu_{i}_date"] = edu['date']

        for i, skill in enumerate(MASTER_DATA['skills']):
            st.session_state[f"orig_skill_{i}_category"] = skill['category']
            st.session_state[f"skill_{i}_category"] = skill['category']
            st.session_state[f"orig_skill_{i}_details"] = skill['details']
            st.session_state[f"skill_{i}_details"] = skill['details']

        # Init Experience
        for i, exp in enumerate(MASTER_DATA['experience']):
            st.session_state[f"exp_{i}_keep"] = True
            st.session_state[f"exp_{i}_company"] = exp['company']
            st.session_state[f"exp_{i}_title"] = exp['title']
            st.session_state[f"exp_{i}_date"] = exp['date']
            for j, b in enumerate(exp['bullets']):
                st.session_state[f"orig_exp_{i}_b_{j}"] = b
                st.session_state[f"exp_{i}_b_{j}"] = b
                st.session_state[f"exp_{i}_b_{j}_keep"] = True 

        # Init Projects
        for i, proj in enumerate(MASTER_DATA['projects']):
            st.session_state[f"proj_{i}_keep"] = True
            st.session_state[f"proj_{i}_title"] = proj['title']
            st.session_state[f"proj_{i}_subtitle"] = proj['subtitle']
            for j, b in enumerate(proj['bullets']):
                st.session_state[f"orig_proj_{i}_b_{j}"] = b
                st.session_state[f"proj_{i}_b_{j}"] = b
                st.session_state[f"proj_{i}_b_{j}_keep"] = True 
                
        # Top-level Section properties
        st.session_state['sec_edu_title'] = "EDUCATION"
        st.session_state['sec_edu_keep'] = True
        
        st.session_state['sec_skills_title'] = "SKILLS"
        st.session_state['sec_skills_keep'] = True
        
        st.session_state['sec_exp_title'] = "PROFESSIONAL EXPERIENCE"
        st.session_state['orig_sec_exp_title'] = "PROFESSIONAL EXPERIENCE"
        st.session_state['sec_exp_keep'] = True
        
        st.session_state['sec_proj_title'] = "EXTRACURRICULARS"
        st.session_state['orig_sec_proj_title'] = "EXTRACURRICULARS"
        st.session_state['sec_proj_keep'] = True

        st.session_state['ai_run'] = False
        st.session_state['initialized'] = True

    # APPLY ANY PENDING AI UPDATES FOR TOP-LEVEL FIELDS
    if "new_company_name" in st.session_state:
        st.session_state["company_name"] = st.session_state["new_company_name"]
        del st.session_state["new_company_name"]
        
    if "new_job_title" in st.session_state:
        st.session_state["job_title"] = st.session_state["new_job_title"]
        del st.session_state["new_job_title"]

def set_ai_choice(tk, choice):
    """Updates the state based on whether the user accepts or rejects an AI suggestion."""
    st.session_state[f"status_{tk}"] = choice
    if choice == "accepted":
        if tk.endswith("_keep"):
            st.session_state[tk] = False # AI suggests dropping the section
        else:
            sug_val = st.session_state.get(f"ai_sug_{tk}", "")
            # If bullet is suggested to be dropped
            if "_b_" in tk and sug_val == "":
                st.session_state[f"{tk}_keep"] = False
            else:
                st.session_state[tk] = sug_val
                if "_b_" in tk:
                    st.session_state[f"{tk}_keep"] = True
    else:
        if tk.endswith("_keep"):
            st.session_state[tk] = True # Keep the section
        else:
            st.session_state[tk] = st.session_state.get(f"orig_{tk}", "")
            if "_b_" in tk:
                st.session_state[f"{tk}_keep"] = True

def accept_all_category(groups_dict):
    """Accepts all AI suggestions within an entire category (like Experience)."""
    for keys in groups_dict.values():
        for tk in keys:
            set_ai_choice(tk, "accepted")

def init_tracker():
    """Ensures tracking folder and JSON log file exist."""
    if not os.path.exists(RESUME_DIR):
        os.makedirs(RESUME_DIR)
    if not os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE, "w") as f:
            json.dump([], f)

def save_application(company, title, job_desc, pdf_data):
    """Saves the compiled PDF locally and updates the job tracker JSON log."""
    init_tracker()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Clean strings for safe filenames
    safe_company = "".join(c for c in company if c.isalnum() or c in (' ', '-', '_')).strip().replace(' ', '_')
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip().replace(' ', '_')
    if not safe_company: safe_company = "UnknownCompany"
    if not safe_title: safe_title = "UnknownTitle"

    filename = f"{safe_company}_{safe_title}_{timestamp}.pdf"
    filepath = os.path.join(RESUME_DIR, filename)

    # Save PDF
    with open(filepath, "wb") as f:
        f.write(pdf_data)

    # Update Log
    with open(TRACKER_FILE, "r") as f:
        log = json.load(f)

    log.append({
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "company": company,
        "title": title,
        "job_description": job_desc,
        "resume_file": filepath
    })

    with open(TRACKER_FILE, "w") as f:
        json.dump(log, f, indent=4)

# ==========================================
# 3. AI SERVICE
# ==========================================
def build_ai_payload():
    """Extracts current active state into a payload for the AI to analyze."""
    resume_data = {
        "sec_exp_title": st.session_state['orig_sec_exp_title'],
        "sec_proj_title": st.session_state['orig_sec_proj_title'],
        "skills": [],
        "experience": [],
        "projects": []
    }
    
    for i in range(len(MASTER_DATA['skills'])):
        resume_data["skills"].append({
            "category": st.session_state[f"orig_skill_{i}_category"],
            "details": st.session_state[f"orig_skill_{i}_details"]
        })
        
    for i in range(len(MASTER_DATA['experience'])):
        resume_data["experience"].append({
            "company": st.session_state[f"exp_{i}_company"],
            "title": st.session_state[f"exp_{i}_title"],
            "bullets": [st.session_state[f"orig_exp_{i}_b_{j}"] for j in range(len(MASTER_DATA['experience'][i]['bullets']))]
        })
        
    for i in range(len(MASTER_DATA['projects'])):
        resume_data["projects"].append({
            "title": st.session_state[f"proj_{i}_title"],
            "bullets": [st.session_state[f"orig_proj_{i}_b_{j}"] for j in range(len(MASTER_DATA['projects'][i]['bullets']))]
        })
    return resume_data

def run_anthropic_ai(api_key, job_desc):
    """Calls Claude to generate tailored bullet points."""
    # Clean up previous suggestions
    keys_to_delete = [k for k in st.session_state.keys() if k.startswith("ai_sug_") or k.startswith("status_")]
    for k in keys_to_delete:
        del st.session_state[k]
    
    resume_data = build_ai_payload()

    prompt = f"""
You are an expert resume writer. I will provide a candidate's current experience, projects, and skills, along with a job description. 
Your task is to tailor the candidate's resume to the job description.

Job Description:
{job_desc}

Current Resume Data:
{json.dumps(resume_data, indent=2)}

Instructions:
1. Extract the "company_name" and "job_title" from the job description if possible.
2. Rewrite bullet points to highlight relevant skills and align with the job description's keywords.
3. Keep the writing professional, impact-driven (use metrics where available), and concise. Use strong action verbs.
4. Optimize for a ONE-PAGE layout. Be ruthless with fluff.
5. CRITICAL RULE - STRICT MAXIMUM OF 4 BULLETS PER JOB/PROJECT: You must strictly limit each job or project to a maximum of 4 bullet points. Simply return an array of your chosen 3 or 4 tailored bullet points. You DO NOT need to match the original array length. The system will automatically drop the excess.
6. Edit the Skills section to reorder or emphasize relevant tools/technologies for the job, but do not hallucinate skills the candidate does not have.
7. If an entire job or project is completely irrelevant to the job description, set "keep": false.
8. Do NOT hallucinate metrics, new skills, or new jobs. Only use the provided facts.

Respond STRICTLY with a JSON object in this exact format:
{{
   "company_name": "(Extracted company name, or empty string)",
   "job_title": "(Extracted job title, or empty string)",
   "sec_exp_title": "(Suggest a better section title if needed, or keep original)",
   "sec_proj_title": "(Suggest a better section title if needed, or keep original)",
   "skills": [
      {{
         "category": "category name",
         "details": "tailored list of skills"
      }}
   ],
   "experience": [
      {{
         "keep": true,
         "bullets": ["tailored bullet 1", "tailored bullet 2", "tailored bullet 3"]
      }}
   ],
   "projects": [
      {{
         "keep": false,
         "bullets": []
      }}
   ]
}}
"""
    try:
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=3000,
            system="You are an expert resume writer. Output ONLY valid JSON, no markdown formatting.",
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.content[0].text.strip()
        if content.startswith("```json"):
            content = content[7:-3]
        elif content.startswith("```"):
            content = content[3:-3]
            
        result = json.loads(content)
        
        # Parse Metadata
        if "company_name" in result and result["company_name"]:
            st.session_state["new_company_name"] = result["company_name"]
        if "job_title" in result and result["job_title"]:
            st.session_state["new_job_title"] = result["job_title"]

        # Parse Title Suggestions
        if result.get("sec_exp_title") and result["sec_exp_title"] != st.session_state["orig_sec_exp_title"]:
            st.session_state["ai_sug_sec_exp_title"] = result["sec_exp_title"]
            st.session_state["status_sec_exp_title"] = "rejected"
            
        if result.get("sec_proj_title") and result["sec_proj_title"] != st.session_state["orig_sec_proj_title"]:
            st.session_state["ai_sug_sec_proj_title"] = result["sec_proj_title"]
            st.session_state["status_sec_proj_title"] = "rejected"
            
        # Parse Skills Suggestions
        for i, skill in enumerate(result.get("skills", [])):
            if i < len(MASTER_DATA['skills']):
                orig_cat = st.session_state[f"orig_skill_{i}_category"]
                if skill.get("category") and skill["category"] != orig_cat:
                    st.session_state[f"ai_sug_skill_{i}_category"] = skill["category"]
                    st.session_state[f"status_skill_{i}_category"] = "rejected"
                    
                orig_det = st.session_state[f"orig_skill_{i}_details"]
                if skill.get("details") and skill["details"] != orig_det:
                    st.session_state[f"ai_sug_skill_{i}_details"] = skill["details"]
                    st.session_state[f"status_skill_{i}_details"] = "rejected"
            
        # Parse Experience Suggestions (WITH HARD CAP ENFORCEMENT)
        for i, exp in enumerate(result.get("experience", [])):
            if not exp.get("keep", True):
                st.session_state[f"ai_sug_exp_{i}_keep"] = False
                st.session_state[f"status_exp_{i}_keep"] = "rejected"
                continue
            
            # Python forcibly trims the AI response to max 4 bullets just in case it breaks the rules
            ai_bullets = exp.get("bullets", [])[:4] 
            
            for j in range(len(MASTER_DATA['experience'][i]['bullets'])):
                orig_b = st.session_state[f"orig_exp_{i}_b_{j}"]
                
                # If the AI provided a bullet for this slot, use it. Otherwise, force a drop ("").
                b = ai_bullets[j] if j < len(ai_bullets) else ""
                
                if b != orig_b: 
                    st.session_state[f"ai_sug_exp_{i}_b_{j}"] = b
                    st.session_state[f"status_exp_{i}_b_{j}"] = "rejected"

        # Parse Project Suggestions (WITH HARD CAP ENFORCEMENT)
        for i, proj in enumerate(result.get("projects", [])):
            if not proj.get("keep", True):
                st.session_state[f"ai_sug_proj_{i}_keep"] = False
                st.session_state[f"status_proj_{i}_keep"] = "rejected"
                continue
                
            ai_bullets = proj.get("bullets", [])[:4]
            
            for j in range(len(MASTER_DATA['projects'][i]['bullets'])):
                orig_b = st.session_state[f"orig_proj_{i}_b_{j}"]
                
                b = ai_bullets[j] if j < len(ai_bullets) else ""
                
                if b != orig_b:
                    st.session_state[f"ai_sug_proj_{i}_b_{j}"] = b
                    st.session_state[f"status_proj_{i}_b_{j}"] = "rejected"
                        
        st.session_state['ai_run'] = True
    except json.JSONDecodeError:
        st.error("Failed to parse AI response. Ensure the API key is correct and try again.")
    except Exception as e:
        st.error(f"AI API Error: {e}")

# ==========================================
# 4. PDF COMPILATION SERVICE
# ==========================================
def write_typst_template():
    """Generates the static Typst template file defining the document layout."""
    template_content = """
#let data = json(bytes(sys.inputs.resume_data))

#set page(paper: "us-letter", margin: (x: 0.5in, y: 0.5in))
#set text(font: ("Helvetica Neue", "Arial", "sans-serif"), size: 9.5pt, fill: rgb("#333333"))
#set par(leading: 0.4em)
#set list(indent: 1em, body-indent: 0.5em, tight: true)

#show heading.where(level: 1): it => block(width: 100%, above: 0em, below: 0.5em)[
  #set align(center)
  #set text(size: 20pt, weight: "bold", fill: rgb("#2c3e50"))
  #it.body
]

#show heading.where(level: 2): it => block(width: 100%, above: 1.2em, below: 0.6em)[
  #set text(size: 12pt, weight: "bold", fill: rgb("#2c3e50"))
  #it.body
  #v(-0.4em)
  #line(length: 100%, stroke: 0.5pt + rgb("#bdc3c7"))
]

= #data.name

#align(center)[
  #text(size: 9.5pt, fill: rgb("#555555"))[
    #data.location | #data.title | #data.contact
  ]
]

#if data.sections.education.keep [
  == #data.sections.education.title
  #for edu in data.education [
    #block(width: 100%, breakable: false, above: 0.6em, below: 0.6em)[
      #grid(
        columns: (1fr, auto),
        gutter: 1em,
        [#text(weight: "bold")[#edu.school]],
        [#text(style: "italic", fill: rgb("#555555"))[#edu.date]]
      )
      #v(-0.4em)
      #text()[#edu.degree]
    ]
  ]
]

#if data.sections.skills.keep [
  == #data.sections.skills.title
  #block(width: 100%, breakable: false, above: 0.6em, below: 0.6em)[
    #for skill in data.skills [
      - *#skill.category:* #skill.details
    ]
  ]
]

#if data.sections.experience.keep [
  == #data.sections.experience.title
  #for job in data.experience [
    #block(width: 100%, breakable: false, above: 0.6em, below: 0.6em)[
      #grid(
        columns: (1fr, auto),
        gutter: 1em,
        [#text(weight: "bold")[#job.title | #job.company]],
        [#text(style: "italic", fill: rgb("#555555"))[#job.date]]
      )
      #if job.bullets.len() > 0 [
        #list(..job.bullets.map(b => [#b]))
      ]
    ]
  ]
]

#if data.sections.projects.keep [
  == #data.sections.projects.title
  #for proj in data.projects [
    #block(width: 100%, breakable: false, above: 0.6em, below: 0.6em)[
      #text(weight: "bold")[#proj.title]
      #if proj.subtitle != "" [ - #text(style: "italic")[#proj.subtitle] ]
      #if proj.bullets.len() > 0 [
        #list(..proj.bullets.map(b => [#b]))
      ]
    ]
  ]
]
"""
    with open("resume_template.typ", "w") as f:
        f.write(template_content)

def build_pdf_payload():
    """Constructs the structured JSON payload to inject into the Typst template."""
    final_data = {
        "name": st.session_state.get("basics_name", ""),
        "title": st.session_state.get("basics_title", ""),
        "location": st.session_state.get("basics_location", ""),
        "contact": st.session_state.get("basics_contact", ""),
        "sections": {
            "education": {
                "title": st.session_state.get("sec_edu_title", "EDUCATION"),
                "keep": st.session_state.get("sec_edu_keep", True)
            },
            "skills": {
                "title": st.session_state.get("sec_skills_title", "SKILLS"),
                "keep": st.session_state.get("sec_skills_keep", True)
            },
            "experience": {
                "title": st.session_state.get("sec_exp_title", "PROFESSIONAL EXPERIENCE"),
                "keep": st.session_state.get("sec_exp_keep", True)
            },
            "projects": {
                "title": st.session_state.get("sec_proj_title", "EXTRACURRICULARS"),
                "keep": st.session_state.get("sec_proj_keep", True)
            }
        },
        "education": [],
        "skills": [],
        "experience": [],
        "projects": []
    }
    
    for i in range(len(MASTER_DATA['education'])):
        final_data["education"].append({
            "school": st.session_state.get(f"edu_{i}_school", ""),
            "degree": st.session_state.get(f"edu_{i}_degree", ""),
            "date": st.session_state.get(f"edu_{i}_date", "")
        })
        
    for i in range(len(MASTER_DATA['skills'])):
        final_data["skills"].append({
            "category": st.session_state.get(f"skill_{i}_category", ""),
            "details": st.session_state.get(f"skill_{i}_details", "")
        })
    
    for i in range(len(MASTER_DATA['experience'])):
        if st.session_state.get(f"exp_{i}_keep", True):
            exp = {
                "company": st.session_state.get(f"exp_{i}_company", ""),
                "title": st.session_state.get(f"exp_{i}_title", ""),
                "date": st.session_state.get(f"exp_{i}_date", ""),
                "bullets": []
            }
            for j in range(len(MASTER_DATA['experience'][i]['bullets'])):
                if st.session_state.get(f"exp_{i}_b_{j}_keep", True):
                    txt = st.session_state.get(f"exp_{i}_b_{j}", "")
                    if txt.strip():
                        exp["bullets"].append(txt)
            final_data["experience"].append(exp)
            
    for i in range(len(MASTER_DATA['projects'])):
        if st.session_state.get(f"proj_{i}_keep", True):
            proj = {
                "title": st.session_state.get(f"proj_{i}_title", ""),
                "subtitle": st.session_state.get(f"proj_{i}_subtitle", ""),
                "bullets": []
            }
            for j in range(len(MASTER_DATA['projects'][i]['bullets'])):
                if st.session_state.get(f"proj_{i}_b_{j}_keep", True):
                    txt = st.session_state.get(f"proj_{i}_b_{j}", "")
                    if txt.strip():
                        proj["bullets"].append(txt)
            final_data["projects"].append(proj)
            
    return final_data

# ==========================================
# 5. UI COMPONENTS
# ==========================================
def render_ai_review():
    """Renders the hierarchically grouped AI suggestions with side-by-side buttons."""
    st.subheader("Review AI Edits")
    if not st.session_state.get('ai_run', False):
        st.info("Paste a job description and click 'Generate' to see AI suggestions here.")
        return

    # Gather all AI suggestions
    target_keys = [k.replace("ai_sug_", "") for k in st.session_state.keys() if k.startswith("ai_sug_")]
    if not target_keys:
        st.success("No changes suggested by AI! Your resume is already a great match.")
        return

    # Group suggestions hierarchically
    groups = {
        "Section Headers": {},
        "Skills": {},
        "Experience": {},
        "Projects": {},
        "Other": {}
    }
    
    for tk in target_keys:
        if tk.startswith("sec_") and "_title" in tk:
            groups["Section Headers"].setdefault("Renames", []).append(tk)
        elif tk.startswith("skill_"):
            idx = tk.split('_')[1]
            cat = st.session_state.get(f"orig_skill_{idx}_category", f"Skill {idx}")
            groups["Skills"].setdefault(cat, []).append(tk)
        elif tk.startswith("exp_"):
            idx = tk.split('_')[1]
            comp = st.session_state.get(f"exp_{idx}_company", f"Experience {idx}")
            groups["Experience"].setdefault(comp, []).append(tk)
        elif tk.startswith("proj_"):
            idx = tk.split('_')[1]
            title = st.session_state.get(f"proj_{idx}_title", f"Project {idx}")
            groups["Projects"].setdefault(title, []).append(tk)
        else:
            groups["Other"].setdefault("Misc", []).append(tk)

    # Render groups
    for category_name, sub_groups in groups.items():
        if not sub_groups:
            continue
            
        total_changes = sum(len(keys) for keys in sub_groups.values())
        
        with st.expander(f"**{category_name}** 🟢 {total_changes}", expanded=True):
            st.button(f"Accept All {total_changes} Changes", key=f"btn_acc_all_{category_name}", on_click=accept_all_category, args=(sub_groups,), type="secondary")
            st.divider()
            
            for sub_cat, keys in sub_groups.items():
                st.markdown(f"##### {sub_cat}")
                
                for tk in keys:
                    c1, c2, c3 = st.columns([10, 1, 1])
                    status = st.session_state.get(f"status_{tk}", "rejected")
                    
                    with c1:
                        # 1. Section Title Modifications
                        if tk.startswith("sec_") and "_title" in tk:
                            orig = st.session_state.get(f"orig_{tk}", "")
                            sug = st.session_state[f"ai_sug_{tk}"]
                            st.markdown(f"<div style='font-size: 14px; margin-bottom: 5px;'><del style='opacity: 0.6;'>{orig}</del> &rarr; <span style='color:#10b981; font-weight:bold;'>{sug}</span></div>", unsafe_allow_html=True)
                            
                        # 2. Section Removal Suggestions
                        elif "_keep" in tk:
                            st.markdown(f"⚠️ **Remove Section** (AI determined this is not relevant to the job)")
                            
                        # 3. Text/Bullet Modifications
                        elif "_b_" in tk or "skill_" in tk:
                            orig = st.session_state.get(f"orig_{tk}", "")
                            sug = st.session_state[f"ai_sug_{tk}"]
                            
                            if sug == "":
                                st.markdown(f"""
                                <div style='font-size: 13.5px; line-height: 1.4; margin-bottom: 8px; padding-left: 10px; border-left: 3px solid #ef4444;'>
                                    <div style='text-decoration: line-through; margin-bottom: 4px; opacity: 0.6;'>{orig}</div>
                                    <div style='color: #ef4444; font-weight: 600;'>⚠️ AI suggests dropping this bullet</div>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.markdown(f"""
                                <div style='font-size: 13.5px; line-height: 1.4; margin-bottom: 8px; padding-left: 10px; border-left: 3px solid #10b981;'>
                                    <div style='opacity: 0.6; text-decoration: line-through; margin-bottom: 4px;'>{orig}</div>
                                    <div style='color: #10b981; font-weight: 600;'>{sug}</div>
                                </div>
                                """, unsafe_allow_html=True)
                    
                    with c2:
                        st.button("✅", key=f"acc_{tk}", type="primary" if status == "accepted" else "secondary", help="Accept AI Suggestion", on_click=set_ai_choice, args=(tk, "accepted"))
                    with c3:
                        st.button("❌", key=f"rej_{tk}", type="primary" if status == "rejected" else "secondary", help="Keep Original", on_click=set_ai_choice, args=(tk, "rejected"))
                        
                st.write("")

def render_manual_editor():
    """Renders the manual override tab."""
    st.subheader("Manual Document Editor")
    st.caption("Changes made here directly override AI suggestions and update the PDF.")
    
    with st.expander("Basics & Contact"):
        st.text_input("Name", key="basics_name")
        st.text_input("Title", key="basics_title")
        c1, c2 = st.columns(2)
        with c1: st.text_input("Location", key="basics_location")
        with c2: st.text_input("Contact/Degree", key="basics_contact")
        
    with st.expander("Education & Skills"):
        st.toggle("Include Education", key="sec_edu_keep")
        st.text_input("Education Header", key="sec_edu_title", disabled=not st.session_state.get("sec_edu_keep", True))
        
        disable_edu = not st.session_state.get("sec_edu_keep", True)
        for i in range(len(MASTER_DATA['education'])):
            c1, c2, c3 = st.columns(3)
            with c1: st.text_input("School", key=f"edu_{i}_school", disabled=disable_edu)
            with c2: st.text_input("Degree", key=f"edu_{i}_degree", disabled=disable_edu)
            with c3: st.text_input("Date", key=f"edu_{i}_date", disabled=disable_edu)
        
        st.divider()
        st.toggle("Include Skills", key="sec_skills_keep")
        st.text_input("Skills Header", key="sec_skills_title", disabled=not st.session_state.get("sec_skills_keep", True))
        
        disable_skills = not st.session_state.get("sec_skills_keep", True)
        for i in range(len(MASTER_DATA['skills'])):
            c1, c2 = st.columns([1,3])
            with c1: st.text_input("Category", key=f"skill_{i}_category", disabled=disable_skills)
            with c2: st.text_input("Details", key=f"skill_{i}_details", disabled=disable_skills)
        
    st.write("---")
    
    # Experience Section
    sc1, sc2 = st.columns([1, 3])
    with sc1: sec_exp_on = st.toggle("Include Entire Section", key="sec_exp_keep")
    with sc2: st.text_input("Section Header", key="sec_exp_title", disabled=not sec_exp_on)

    for i in range(len(MASTER_DATA['experience'])):
        comp = st.session_state.get(f"exp_{i}_company", MASTER_DATA['experience'][i]['company'])
        is_kept = st.session_state.get(f"exp_{i}_keep", True)
        title_text = comp if (is_kept and sec_exp_on) else f"~~{comp}~~ (Hidden)"
        
        with st.expander(title_text):
            item_kept = st.toggle("Include in Resume", key=f"exp_{i}_keep", disabled=not sec_exp_on)
            disable_inputs = (not item_kept) or (not sec_exp_on)
            
            c1, c2, c3 = st.columns([2, 2, 1])
            with c1: st.text_input("Company", key=f"exp_{i}_company", disabled=disable_inputs)
            with c2: st.text_input("Title", key=f"exp_{i}_title", disabled=disable_inputs)
            with c3: st.text_input("Date", key=f"exp_{i}_date", disabled=disable_inputs)
            
            st.write("*Bullet Points*")
            for j in range(len(MASTER_DATA['experience'][i]['bullets'])):
                bc1, bc2 = st.columns([1, 15])
                with bc1:
                    st.write("") # Margin spacing
                    st.checkbox("Keep", key=f"exp_{i}_b_{j}_keep", label_visibility="collapsed", disabled=disable_inputs)
                with bc2:
                    is_b_kept = st.session_state.get(f"exp_{i}_b_{j}_keep", True)
                    st.text_area(f"Bullet {j+1}", key=f"exp_{i}_b_{j}", height=68, label_visibility="collapsed", disabled=(disable_inputs or not is_b_kept))
                    
    st.write("---")
    
    # Projects Section
    pc1, pc2 = st.columns([1, 3])
    with pc1: sec_proj_on = st.toggle("Include Entire Section", key="sec_proj_keep")
    with pc2: st.text_input("Section Header", key="sec_proj_title", disabled=not sec_proj_on)

    for i in range(len(MASTER_DATA['projects'])):
        proj_title = st.session_state.get(f"proj_{i}_title", MASTER_DATA['projects'][i]['title'])
        is_kept = st.session_state.get(f"proj_{i}_keep", True)
        title_text = proj_title if (is_kept and sec_proj_on) else f"~~{proj_title}~~ (Hidden)"
        
        with st.expander(title_text):
            item_kept = st.toggle("Include in Resume", key=f"proj_{i}_keep", disabled=not sec_proj_on)
            disable_inputs = (not item_kept) or (not sec_proj_on)
            
            c1, c2 = st.columns(2)
            with c1: st.text_input("Title", key=f"proj_{i}_title", disabled=disable_inputs)
            with c2: st.text_input("Subtitle", key=f"proj_{i}_subtitle", disabled=disable_inputs)
            
            st.write("*Bullet Points*")
            for j in range(len(MASTER_DATA['projects'][i]['bullets'])):
                bc1, bc2 = st.columns([1, 15])
                with bc1:
                    st.write("")
                    st.checkbox("Keep", key=f"proj_{i}_b_{j}_keep", label_visibility="collapsed", disabled=disable_inputs)
                with bc2:
                    is_b_kept = st.session_state.get(f"proj_{i}_b_{j}_keep", True)
                    st.text_area(f"Bullet {j+1}", key=f"proj_{i}_b_{j}", height=68, label_visibility="collapsed", disabled=(disable_inputs or not is_b_kept))

def render_job_tracker():
    """Renders a log of saved applications."""
    st.subheader("Saved Applications Tracker")
    st.caption("A local history of generated resumes and job descriptions.")
    
    if os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE, "r") as f:
            log = json.load(f)
            
        if not log:
            st.info("No applications saved yet. Generate a resume and click 'Save Application' to start tracking.")
        else:
            for entry in reversed(log): # Show newest first
                with st.expander(f"📁 {entry['company']} - {entry['title']} ({entry['date']})"):
                    st.write(f"**Saved Resume Path:** `{entry['resume_file']}`")
                    
                    if os.path.exists(entry['resume_file']):
                        with open(entry['resume_file'], "rb") as pdf_file:
                            st.download_button(
                                "⬇️ Download Saved PDF", 
                                pdf_file, 
                                file_name=os.path.basename(entry['resume_file']), 
                                key=f"dl_{entry['date']}"
                            )
                    else:
                        st.error("Saved PDF file not found at path.")
                        
                    st.text_area("Job Description", entry['job_description'], height=150, disabled=True, key=f"desc_{entry['date']}")
    else:
        st.info("No applications saved yet. Generate a resume and click 'Save Application' to start tracking.")

def main():
    """Main Application Orchestrator"""
    st.set_page_config(layout="wide", page_title="AI Resume Editor")
    
    write_typst_template()
    init_state()
    init_tracker()
    
    st.title("Data-First Resume Tailor")

    editor_col, preview_col = st.columns([1.2, 1])

    with editor_col:
        with st.container(border=True):
            api_key_env = os.getenv("ANTHROPIC_API_KEY", "")
            api_key = st.text_input(
                "Anthropic API Key (Claude)", 
                value=api_key_env,
                type="password", 
                placeholder="sk-ant-...", 
                help="Automatically loaded from .env if available. Otherwise, paste it here."
            )
            
            # Application Details
            st.write("---")
            st.text_area("Paste Job Description", key="job_description", height=100, placeholder="Paste Job Description here to tailor and track...")
            
            c1, c2 = st.columns(2)
            with c1: st.text_input("Company Name", key="company_name", placeholder="Auto-fills from AI, or type manually")
            with c2: st.text_input("Job Title", key="job_title", placeholder="Auto-fills from AI, or type manually")

            if st.button("✨ Generate Tailored Resume", type="primary", use_container_width=True):
                if not api_key:
                    st.error("Please enter your Anthropic API key.")
                elif not st.session_state.job_description:
                    st.error("Please enter a job description.")
                else:
                    with st.spinner("Analyzing profile and generating tailored bullets..."):
                        run_anthropic_ai(api_key, st.session_state.job_description)
                    st.rerun()

        tab_ai, tab_manual, tab_tracker = st.tabs(["✨ Review AI Suggestions", "🛠️ Manual Editor", "📁 Job Tracker"])
        
        with tab_ai:
            render_ai_review()
        with tab_manual:
            render_manual_editor()
        with tab_tracker:
            render_job_tracker()

    with preview_col:
        st.subheader("Live PDF Preview")
        final_data = build_pdf_payload()
        
        try:
            json_str = json.dumps(final_data)
            typst.compile("resume_template.typ", output="resume.pdf", sys_inputs={"resume_data": json_str})
            
            with open("resume.pdf", "rb") as f:
                pdf_data = f.read()
                
            b64_pdf = base64.b64encode(pdf_data).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{b64_pdf}#toolbar=0&navpanes=0&scrollbar=0" width="100%" height="800px" type="application/pdf" style="border-radius: 8px; border: 1px solid #ccc;"></iframe>'
            
            st.markdown(pdf_display, unsafe_allow_html=True)
            
            # Action Buttons below the preview
            c1, c2 = st.columns(2)
            with c1:
                st.download_button("⬇️ Download Quick PDF", pdf_data, "Tailored_Resume.pdf", "application/pdf", use_container_width=True)
            with c2:
                if st.button("💾 Save Application to Tracker", type="primary", use_container_width=True):
                    if not st.session_state.company_name or not st.session_state.job_title:
                        st.warning("Please provide a Company Name and Job Title on the left side before saving to the tracker.")
                    else:
                        save_application(
                            st.session_state.company_name, 
                            st.session_state.job_title, 
                            st.session_state.job_description, 
                            pdf_data
                        )
                        st.success("Application successfully saved to Job Tracker!")
            
        except Exception as e:
            st.error(f"Failed to compile PDF. Ensure typst is installed. Error: {e}")

if __name__ == "__main__":
    main()