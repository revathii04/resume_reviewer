import re

def extract_bullet_points_from_resume(resume_text):
    sections = extract_sections(resume_text)
    bullet_points = []

    for section_title in ["projects", "experience", "work experience","related experience","project experience","academic projects","leadership experience","professional experience", "internship experience","internship"]:
        section_content = sections.get(section_title.lower())
        if section_content:
            entries = split_section_entries(section_content)
            for title, points in entries:
                for point in points:
                    bullet_points.append(point)

    return bullet_points

def extract_sections(text):
    sections = {}
    current_section = None
    lines = text.splitlines()

    for line in lines:
        stripped = line.strip().lower()
        if stripped in ["projects", "experience", "work experience","related experience","project experience","academic projects","leadership experience","professional experience", "internship experience"]:
            current_section = stripped
            sections[current_section] = []
        elif current_section:
            sections[current_section].append(line)

    # Join lines in each section back into text
    return {key: "\n".join(value) for key, value in sections.items()}

def split_section_entries(section_text):
    entries = []
    current_title = None
    current_points = []

    for line in section_text.splitlines():
        line = line.strip()
        if not line:
            continue
        if not line.startswith("-") and not line.startswith("•"):
            if current_title and current_points:
                entries.append((current_title, current_points))
                current_points = []
            current_title = line
        else:
            current_points.append(line.lstrip("-• "))

    if current_title and current_points:
        entries.append((current_title, current_points))

    return entries
