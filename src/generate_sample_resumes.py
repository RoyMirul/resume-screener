"""
Generates 8 varied sample resume PDFs for testing our screener.
Run once: python src/generate_sample_resumes.py
"""
from fpdf import FPDF
import os

os.makedirs("resumes", exist_ok=True)

RESUMES = {
    "01_strong_match": """Sarah Chen
Junior AI Engineer
Email: sarah.chen@email.com | Location: Kuala Lumpur

SUMMARY
Recent computer science graduate with 1.5 years of experience building AI automation
tools using Python and LLM APIs. Passionate about prompt engineering and workflow automation.

SKILLS
Python, REST APIs, Google Gemini API, OpenAI API, Prompt Engineering, Git, JSON, Streamlit

EXPERIENCE
AI Automation Intern - TechStart (2023-2024)
- Built Python scripts that automated report generation using the OpenAI API
- Developed a Streamlit prototype to summarize customer feedback with an LLM
- Used Git for version control in a team of 4

PROJECTS
- Resume parser using Python and Gemini API
- Personal chatbot project integrating REST APIs

EDUCATION
BSc Computer Science, University of Malaya (2022)
""",

    "02_good_junior": """Ahmad Faizal
Software Developer (Entry Level)
Email: ahmad.faizal@email.com

SUMMARY
Entry-level developer with strong Python fundamentals and a growing interest in AI.
1 year of experience. Eager to learn and contribute to automation projects.

SKILLS
Python, Git, REST APIs, JSON, basic machine learning, SQL

EXPERIENCE
Junior Developer - WebSolutions (2024-present)
- Wrote Python automation scripts for internal data processing
- Consumed REST APIs to integrate third-party services
- Collaborated using Git

PROJECTS
- Built a weather-data automation script using a public API
- Completed an online course on generative AI basics

EDUCATION
BSc Information Technology (2023)
""",

    "03_overqualified_senior": """Dr. Rajesh Kumar
Senior Machine Learning Engineer
Email: rajesh.kumar@email.com

SUMMARY
Senior ML engineer with 9 years of experience leading AI teams and deploying
production machine learning systems at scale.

SKILLS
Python, TensorFlow, PyTorch, LLM fine-tuning, MLOps, Kubernetes, REST APIs,
Prompt Engineering, Git, distributed systems, team leadership

EXPERIENCE
Senior ML Engineer - BigTech Corp (2018-present)
- Led a team of 8 engineers building recommendation systems
- Deployed LLM-based products serving millions of users
- Architected MLOps pipelines

Lead Data Scientist - DataCorp (2015-2018)

EDUCATION
PhD Machine Learning (2015)
MSc Computer Science (2012)
""",

    "04_career_changer": """Nurul Huda
Data Analyst transitioning to AI Engineering
Email: nurul.huda@email.com

SUMMARY
Data analyst with 3 years of experience, now transitioning into AI automation.
Recently completed self-study in Python and LLM APIs.

SKILLS
Python (learning), SQL, Excel, Power BI, data visualization, basic REST APIs, JSON

EXPERIENCE
Data Analyst - RetailCo (2021-present)
- Analyzed sales data and built dashboards
- Automated weekly reports using Python scripts
- Started experimenting with the OpenAI API for text analysis

PROJECTS
- Personal project: sentiment analysis of reviews using an LLM API

EDUCATION
BSc Statistics (2020)
""",

    "05_adjacent_webdev": """Jason Lee
Web Developer
Email: jason.lee@email.com

SUMMARY
Full-stack web developer with 2 years of experience building web applications.
Interested in exploring AI integration.

SKILLS
JavaScript, React, Node.js, HTML, CSS, REST APIs, Git, some Python

EXPERIENCE
Web Developer - DigitalAgency (2022-present)
- Built responsive web apps with React and Node.js
- Integrated third-party REST APIs
- Used Git in a team environment

EDUCATION
Diploma in Web Development (2022)
""",

    "06_fresh_grad_thin": """Lim Wei Jie
Fresh Graduate
Email: lim.weijie@email.com

SUMMARY
Recent graduate seeking an entry-level role in technology. Enthusiastic and quick to learn.

SKILLS
Python (academic), Java (academic), basic Git

EXPERIENCE
No formal work experience.

PROJECTS
- Final year project: a simple inventory management system in Java
- Coursework in programming fundamentals

EDUCATION
BSc Computer Science (2024)
""",

    "07_wrong_field": """Michelle Tan
Senior Accountant
Email: michelle.tan@email.com

SUMMARY
Experienced accountant with 7 years in financial reporting and auditing.

SKILLS
Accounting, financial reporting, auditing, Excel, SAP, tax compliance, budgeting

EXPERIENCE
Senior Accountant - FinanceFirm (2017-present)
- Prepared financial statements and managed audits
- Ensured tax compliance for corporate clients

EDUCATION
BAcc Accounting (2016)
Professional accounting certification (ACCA)
""",

    "08_keyword_stuffer": """Kevin Rodriguez
AI Expert
Email: kevin.rodriguez@email.com

SUMMARY
AI professional.

SKILLS
Python, Machine Learning, Deep Learning, AI, LLM, Prompt Engineering, Gemini,
OpenAI, TensorFlow, PyTorch, REST APIs, Git, JSON, Streamlit, Automation,
Neural Networks, Data Science, NLP, Computer Vision, MLOps

EXPERIENCE
Various roles.

EDUCATION
Self-taught.
"""
}


def make_pdf(name, content):
    pdf = FPDF()
    pdf.set_margins(15, 15, 15)      # left, top, right margins
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)

    # Usable width = page width minus left+right margins
    usable_width = pdf.w - pdf.l_margin - pdf.r_margin

    for line in content.split("\n"):
        if line.strip() == "":
            pdf.ln(6)                # blank line -> just add vertical space
        else:
            pdf.multi_cell(usable_width, 6, line)

    path = f"resumes/{name}.pdf"
    pdf.output(path)
    print(f"Created {path}")


if __name__ == "__main__":
    for name, content in RESUMES.items():
        make_pdf(name, content)
    print(f"\nDone! Generated {len(RESUMES)} resume PDFs in the resumes/ folder.")