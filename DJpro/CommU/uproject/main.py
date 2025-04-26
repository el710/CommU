# --- file: main.py ---
import logging
import os
from models.skill import USkill
from models.project import UProject
from CommU.uproject.storage.filestorage import FileStorage

def create_and_save_skill():
    print("Create a new skill")
    name = input("Skill name: ")
    description = input("Description: ")
    resources = input("Resources: ")
    goal = input("Goal: ")

    skill = USkill(name, description, resources, goal)
    skill.sign(author="Me", geosocium="Local")

    storage = FileStorage()
    saved = storage.save(skill, overwrite=True)

    if saved:
        print(f"Skill '{skill.name}' saved as template.")
    else:
        print("Failed to save skill (already exists and overwrite=False).")

def load_and_display_project():
    project_name = input("Enter project name to load: ")
    project = UProject(starter_user="Me", project_name=project_name)
    storage = FileStorage()

    if storage.load(project):
        print("Project loaded:")
        print(project.to_dict())
    else:
        print("Project not found.")

def list_templates(extension):
    print(f"\nAvailable .{extension} templates:")
    for file in os.listdir():
        if file.endswith(f".{extension}"):
            print("-", file)

def delete_template():
    name = input("Enter the skill name to delete: ")
    skill = USkill(name)
    storage = FileStorage()
    if storage.delete(skill):
        print(f"Template '{skill.get_file_name()}' deleted.")
    else:
        print("Failed to delete template (maybe it doesn't exist).")

def add_skill_to_project():
    skill_name = input("Enter skill name to load: ")
    project_name = input("Enter project name to load: ")

    skill = USkill(skill_name)
    project = UProject(starter_user="Me", project_name=project_name)
    storage = FileStorage()

    if not storage.load(skill):
        print("Skill not found.")
        return
    if not storage.load(project):
        print("Project not found.")
        return

    project.add_skill(skill)
    storage.save(project, overwrite=True)
    print(f"Skill '{skill_name}' linked to project '{project_name}'.")

def menu():
    while True:
        print("\n--- UProject CLI ---")
        print("1. Create and Save Skill")
        print("2. Load and Display Project")
        print("3. List Skill Templates")
        print("4. Delete Skill Template")
        print("5. Link Skill to Project")
        print("6. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            create_and_save_skill()
        elif choice == "2":
            load_and_display_project()
        elif choice == "3":
            list_templates("stp")
        elif choice == "4":
            delete_template()
        elif choice == "5":
            add_skill_to_project()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    menu()
