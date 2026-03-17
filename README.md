# STUDENT PERFORMANCE MONITORING AND RISK PREDICTION SYSTEM

The **Student Performance Monitoring and Risk Prediction System** is developed by **Joel Jacob**, a **III BSc Artificial Intelligence and Machine Learning student** at **Sree Narayana Guru College, Coimbatore**.

It is designed to analyze student data such as **marks, attendance, and behavior** to monitor performance and identify students who may be at academic risk. The system provides an interactive dashboard built with **Streamlit** for visualizing insights and supporting better academic decision-making.

## Features

- Interactive dashboard built using **Streamlit**
- Student performance tracking based on marks and attendance  
- Risk prediction for identifying low-performing students  
- Separate views for top-performing and at-risk students  
- Data visualization for better understanding of trends  
- Easy-to-use and lightweight interface  

## UI Preview

### Dashboard (Light Mode)
<img width="860" height="711" alt="Image" src="https://github.com/user-attachments/assets/e5042742-81b7-41ff-8dea-296111f1def7" />

### Dashboard (Dark Mode)
<img width="892" height="728" alt="Image" src="https://github.com/user-attachments/assets/70eaff53-6114-4945-938c-edcac3379855" />

## Attendance UI

### Attendance View (first page)
<img width="830" height="534" alt="Image" src="https://github.com/user-attachments/assets/a9b45961-df05-4dd8-9e95-dfb38ae0c672" />

### Attendance View (second page)
<img width="755" height="588" alt="Image" src="https://github.com/user-attachments/assets/c41f2e1b-7361-43f4-91bb-f2cf82ac54c9" />

## Student Overview UI

### Student View (first page)
<img width="879" height="562" alt="Image" src="https://github.com/user-attachments/assets/e78d0da4-4dec-497a-8528-1da296edc419" />

### Student View (second page)
<img width="812" height="591" alt="Image" src="https://github.com/user-attachments/assets/a90115f5-e481-441c-8625-5e22ace834e1" />

## Top Students UI

### Top Performers (Light Mode)
<img width="837" height="833" alt="Image" src="https://github.com/user-attachments/assets/8123b255-a758-4c4c-bca7-364ed69d7246" />


<img width="763" height="713" alt="Image" src="https://github.com/user-attachments/assets/8c6456d0-8936-4cd7-aba0-db943f775cf3" />

## At-Risk Students UI

### At-Risk Students (Light Mode)
<img width="811" height="835" alt="Image" src="https://github.com/user-attachments/assets/7cd4757c-9391-4986-8988-85f52f181501" />

<img width="745" height="723" alt="Image" src="https://github.com/user-attachments/assets/8308aff0-849a-4957-87f4-cea91d537818" />

## Demo Video

https://github.com/user-attachments/assets/0d3fd1d9-6e4a-4983-961f-cd66bbdffac0

## Sample Data Used

- `students.csv` — student details  
- `marks.csv` — subject-wise marks  
- `attendance.csv` — attendance records  
- `behavior.csv` — behavioral data  

## Project Structure

- `app.py` — main Streamlit application  
- `data_loader.py` — data loading and preprocessing  
- `ui_helpers.py` — UI components  
- `utils.py` — utility functions  
- `*.csv` — datasets  

## Setup (Windows)

1. Install dependencies:
```bash
pip install -r requirements.txt
