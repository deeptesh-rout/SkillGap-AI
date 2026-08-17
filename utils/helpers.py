import json
import os


def load_json_file(file_path):

    if not os.path.exists(file_path):

        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    with open(file_path,"r",encoding="utf-8") as file:
        return json.load(file)


def save_json_file(file_path,data):
    with open(file_path,"w",encoding="utf-8") as file:
        json.dump(data,file,indent=4,ensure_ascii=False)


def normalize_skill_name(skill):

    return (skill.strip().lower())


def format_percentage(value):
    return f"{value * 100:.0f}%"