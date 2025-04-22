# --- file: web_app.py ---
from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
import os
import sys
from models.skill import USkill
from models.project import UProject
from storage.storage import FileStorage

app = FastAPI()
storage = FileStorage()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/skills", response_class=HTMLResponse)
def list_skills(request: Request):
    skills = [f for f in os.listdir() if f.endswith(".stp")]
    return templates.TemplateResponse("skills.html", {"request": request, "skills": skills})


@app.get("/skills/new", response_class=HTMLResponse)
def new_skill_form(request: Request):
    return templates.TemplateResponse("new_skill.html", {"request": request})


@app.post("/skills")
def create_skill(name: str = Form(...), description: str = Form(""), resources: str = Form(""), goal: str = Form("")):
    skill = USkill(name, description, resources, goal)
    skill.sign(author="WebUser", geosocium="Internet")
    if not storage.save(skill, overwrite=True):
        raise HTTPException(status_code=400, detail="Skill could not be saved.")
    return RedirectResponse(url="/skills", status_code=303)


@app.get("/skills/{skill_name}", response_class=HTMLResponse)
def view_skill(request: Request, skill_name: str):
    skill = USkill(skill_name)
    if not storage.load(skill):
        raise HTTPException(status_code=404, detail="Skill not found")
    return templates.TemplateResponse("view_skill.html", {"request": request, "skill": skill.to_dict()})


@app.get("/skills/{skill_name}/edit", response_class=HTMLResponse)
def edit_skill_form(request: Request, skill_name: str):
    skill = USkill(skill_name)
    if not storage.load(skill):
        raise HTTPException(status_code=404, detail="Skill not found")
    return templates.TemplateResponse("edit_skill.html", {"request": request, "skill": skill.to_dict()})


@app.post("/skills/{skill_name}/edit")
def edit_skill(skill_name: str, description: str = Form(""), resources: str = Form(""), goal: str = Form("")):
    skill = USkill(skill_name)
    if not storage.load(skill):
        raise HTTPException(status_code=404, detail="Skill not found")

    skill.description = description
    skill.resources = resources
    skill.goal = goal
    storage.save(skill, overwrite=True)
    return RedirectResponse(url=f"/skills/{skill_name}", status_code=303)


@app.post("/skills/{skill_name}/delete")
def delete_skill(skill_name: str):
    skill = USkill(skill_name)
    if storage.delete(skill):
        return RedirectResponse(url="/skills", status_code=303)
    else:
        raise HTTPException(status_code=404, detail="Skill not found")


@app.get("/projects", response_class=HTMLResponse)
def list_projects(request: Request):
    projects = [f for f in os.listdir() if f.endswith(".ptp")]
    return templates.TemplateResponse("projects.html", {"request": request, "projects": projects})


@app.get("/projects/{project_name}", response_class=HTMLResponse)
def view_project(request: Request, project_name: str):
    project = UProject(starter_user="WebUser", project_name=project_name)
    if not storage.load(project):
        raise HTTPException(status_code=404, detail="Project not found")
    return templates.TemplateResponse("view_project.html", {"request": request, "project": project.to_dict()})


@app.post("/projects/{project_name}/skills/{skill_name}")
def add_skill_to_project(project_name: str, skill_name: str):
    project = UProject(starter_user="WebUser", project_name=project_name)
    skill = USkill(skill_name)

    if not storage.load(skill):
        raise HTTPException(status_code=404, detail="Skill not found")
    if not storage.load(project):
        raise HTTPException(status_code=404, detail="Project not found")

    project.add_skill(skill)
    storage.save(project, overwrite=True)
    return RedirectResponse(url=f"/projects/{project_name}", status_code=303)


if __name__ == "__main__":
    dir_name, file_name = os.path.split(sys.argv[0])
    name = os.path.splitext(file_name)[0]
 
    os.chdir(dir_name)
    os.system(f"python -m uvicorn {name}:app --reload")
