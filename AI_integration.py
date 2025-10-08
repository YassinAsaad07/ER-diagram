import json
import re
import subprocess
import google.generativeai as genai


genai.configure(api_key="AIzaSyDGncTqq8760A9WUFLJWkxM5099mHFye_E")
model = genai.GenerativeModel("models/gemini-2.5-flash")

description = input("Enter your system description: ")

prompt = """from the given detailed english description for the system i want a json file that must strictly follow this schema : 
    {
  "entities": [
    {
      "name": "Student",
      "attributes": [
        { "name": "StudentID", "isPrimaryKey": true },
        { "name": "Name", "composite": ["FirstName", "LastName"] },
        { "name": "Email" },
        { "name": "Phone", "isMultiValued": true }
      ]
    },
    {
      "name": "Course",
      "attributes": [
        { "name": "CourseID", "isPrimaryKey": true },
        { "name": "Title" },
        { "name": "Credits" }
      ]
    },
    {
      "name": "Instructor",
      "attributes": [
        { "name": "InstructorID", "isPrimaryKey": true },
        { "name": "Name" },
        { "name": "Office" }
      ]
    }
  ],
  "relationships": [
    {
      "entity1": "Student",
      "entity2": "Course",
      "name": "Enrolls",
      "cardinality": "M:N",
      "attributes": [
        { "name": "Grade" },
        { "name": "Semester" }
      ]
    },
    {
      "entity1": "Instructor",
      "entity2": "Course",
      "name": "Teaches",
      "cardinality": "1:N"
    }
  ]
}

 with some rules :
    1- no weak entites 
    2- relationships can have attributes
    3- use only valid json without any comments
    """


prompt = description + prompt
response = model.generate_content(prompt)  # markdown + json part

json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
if json_match:
    json_str = json_match.group()  #raw stirng json
    generated_json = json.loads(json_str)  #convert JSON string into a Python dictionary/list
    
    with open("ER-diagram/generated_ER.json", "w") as f:
        json.dump(generated_json, f, indent=2)
    print("ER JSON generated and saved as 'generated_ER.json'")
    subprocess.run(["python", "ER-diagram/ERdiagram.py", "ER-diagram/generated_ER.json"])



#A university has students, professors, and courses. Each student has an ID, name, and email. Each professor has an ID, name, and office. A course has a code, title, and credits. Professors teach courses, and students enroll in courses.
#A hospital management system keeps track of patients, doctors, nurses, departments, appointments, and treatments. Each patient has a unique patient ID, full name (first and last), date of birth, phone numbers (a patient can have multiple), and address. Each doctor has a unique doctor ID, name, specialization, and salary. Each nurse has a nurse ID, name, and assigned department. Departments have a unique department ID, name, and location. Each doctor works in exactly one department, but a department can have many doctors. Patients book appointments with doctors. Each appointment has a date, time, and status (scheduled, completed, canceled). A treatment is prescribed during an appointment and has a treatment ID, description, cost, and duration in days. Nurses assist in treatments — a treatment can have several assisting nurses, and a nurse can assist in multiple treatments. Doctors supervise treatments, and each treatment is supervised by exactly one doctor.


