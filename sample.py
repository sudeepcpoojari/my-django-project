import requests
import json

data = [
    {"student_id": 8, "date": "2025-09-28", "status": "ABSENT"},
    {"student_id": 9, "date": "2025-09-28", "status": "ABSENT"},
    {"student_id": 13, "date": "2025-09-28", "status": "ABSENT"}
]

url = "http://127.0.0.1:8000/student/attendence/mark/"

response = requests.post(url, json=data)
print("Status code:", response.status_code)
if response.content:
    try:
        print(response.json())
    except Exception:
        print("Response text:", response.text)
else:
    print("No content returned")
