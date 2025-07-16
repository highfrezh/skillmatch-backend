# About SkillMatch

**SkillMatch** is an AI-powered freelance marketplace designed to connect small businesses and startups across Africa with skilled remote freelancers.

Whether you're a growing company looking to hire talent or a freelancer seeking meaningful projects, SkillMatch provides a smart, efficient, and transparent platform to collaborate.

---

## 🎯 Our Mission

We aim to empower African SMEs by making it easy to discover, assess, and hire top freelancers — while helping professionals showcase their skills and earn remotely.

---

## 🚀 Key Features

- **Smart Job Matching** – Uses NLP and resume scoring to rank freelancer proposals  
- **Resume Builder** – Freelancers can showcase skills, education, and upload a resume file  
- **Job Posting** – Employers can post and manage freelance job opportunities  
- **Proposal Submission** – Freelancers can apply to jobs with cover letters  
- **Shortlisting + Status Updates** – Employers can shortlist or reject applicants  
- **Built-in Messaging** – Chat feature between employer and freelancer after shortlisting  

---

## 🛠 Tech Stack

- **Frontend:** React, Tailwind CSS, React Router, Axios  
- **Backend:** Django REST Framework, JWT Authentication, spaCy NLP  
- **Database:** PostgreSQL (or SQLite in development)  

---

## 🌍 Who Is It For?

SkillMatch is ideal for:

- 📌 Startups or small businesses hiring remote freelancers  
- 📌 Freelancers looking to apply their skills in real-world projects  
- 📌 Developers building their portfolio with full-stack AI-driven applications  

---

## 💡 Future Goals

We plan to expand SkillMatch with features like:

- Payment integration  
- Freelancer reviews  
- Job filtering by category  
- AI-powered recommendations for both sides  



# 📘 SkillMatch API Documentation

Welcome to the developer guide for **SkillMatch** — an AI-powered freelance job marketplace that connects African SMEs with skilled remote talent. This documentation provides details on how to interact with key features such as job posting, resume profile formatting, and proposal matching.

---

## 🛠️ Project Overview

SkillMatch is a full-stack web application built with **Django REST Framework** and **React.js**. It enables:

- Employers to post remote jobs
- Freelancers to create resume profiles and submit proposals
- An intelligent match scoring system based on resume content and job requirements
- A built-in messaging system for communication after shortlisting

---

## 📃 Resume Description Format (Freelancer)

To improve your proposal match score, freelancers should populate their resume profile using clear and structured content.

### ✅ Fields

| Field           | Type           | Description                                         |
|----------------|----------------|-----------------------------------------------------|
| `skills`       | `string`       | Comma-separated list of technical and soft skills   |
| `experience`   | `string`       | Summary of past work experience and projects        |
| `education`    | `string`       | Academic background or certifications               |
| `resume_file`  | `file`         | Optional resume upload (PDF/DOCX) for NLP scoring   |

### ✅ Example Input

```json
{
  "skills": "Django, React, Tailwind CSS, PostgreSQL, REST API",
  "experience": "Developed a freelance job board using Django REST and React. Built user authentication, chat system, and job matching engine.",
  "education": "BSc in Computer Science from University of Ibadan"
}

```

Here’s a clear and professional **Markdown guide** on how to run the **SkillMatch backend (Django)** locally:

---

# 🛠 How to Run the SkillMatch Backend (Django)

This guide walks you through setting up and running the backend for the **SkillMatch** project.

---

## ✅ Requirements

- Python 3.10+
- pip (Python package manager)
- virtualenv (recommended)
- PostgreSQL or SQLite
- Git

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/highfrezh/skillmatch-backend.git
cd skillmatch-backend
````

---

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
# Activate virtual environment:
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Set Up Environment Variables (Optional)

Create a `.env` file and add your secret keys (optional):

```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

---

### 5. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 6. Create Superuser (Admin Login)

```bash
python manage.py createsuperuser
```

---

### 7. Run the Development Server

```bash
python manage.py runserver
```

Now visit [http://127.0.0.1:8000](http://127.0.0.1:8000) to access the API.

---

## 📁 API Endpoints Overview

| Endpoint             | Description                  |
| -------------------- | ---------------------------- |
| `/api/v1/register/`  | Register a new user          |
| `/api/v1/token/`     | Get JWT token (login)        |
| `/api/v1/jobs/`      | List or create jobs          |
| `/api/v1/proposals/` | Submit a proposal to a job   |
| `/api/v1/resume/`    | Freelancer resume management |
| `/api/v1/chat/`      | Messaging between users      |

---

## 🧪 Run Tests (Optional)

```bash
python manage.py test
```

---

## 🧠 Notes

* By default, the app uses **SQLite**. You can configure PostgreSQL using `DATABASES` in `settings.py` or via `DATABASE_URL` in `.env`.
* Static and media files are configured for local development. For production, use services like AWS S3 or Cloudinary.

---

## 🧵 Technologies Used

* Django & Django REST Framework
* JWT Authentication
* spaCy NLP
* PostgreSQL or SQLite
* Cloud deployment ready (Render, Railway, etc.)

---


