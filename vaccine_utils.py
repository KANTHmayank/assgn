import json
import re

def load_vaccine_data():
    with open("vaccine_schedule.json") as f:
        return json.load(f)

def extract_age(text):
    match = re.search(r"(\d+)\s?(month|year|week)s?", text.lower())
    if not match:
        return None
    value, unit = int(match.group(1)), match.group(2)
    if unit == "week":
        return f"{value} weeks"
    elif unit == "month":
        return f"{value} months"
    elif unit == "year":
        return f"{value * 12} months"
    return None

def recommend_vaccines(age, data):
    return data.get(age, [])


