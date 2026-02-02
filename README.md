# Web-Based Facial Authentication System

This project is a simple website where you can log in using your face instead of a password.

The system checks two things:
- Does your face match the saved photo?
- Are you a real person and not a photo? (It checks this by asking you to blink or open your mouth)

Only when both checks are successful, you will be logged in.

## What Happens When You Use This

1. You open the website in your browser  
2. Your camera turns on  
3. You show your face to the camera  
4. You blink your eyes or open your mouth  
5. The system compares your face with the saved photo  
6. If everything matches, you go to the dashboard  
7. If not, you see an error message  

## Why This Is Useful

This project can be used for:
- Secure login systems  
- Attendance systems  
- Office or lab access  
- Online exams  
- Cybersecurity demonstrations  

It is more secure than normal face login because it can stop:
- Printed photos  
- Photos shown on another phone  
- Fake or still images  

## Main Features

- Login using face instead of password  
- Checks if the user is real (blink or mouth movement)  
- Blocks too many wrong login attempts  
- Shows a dashboard after login  
- Simple and easy-to-use design  

## Technologies Used

- Python  
- Flask  
- OpenCV  
- face_recognition (dlib)  
- HTML and CSS  

## Project Files

facial-auth-system/
├── app.py (Main program)
├── requirements.txt (List of required software)
├── .gitignore (Files that should not be uploaded)
├── utils/
│ └── liveness.py (Checks blinking and mouth movement)
├── templates/
│ ├── login.html (Login page)
│ └── dashboard.html (Dashboard page)
└── static/
└── style.css (Website design)


## How to Run the Project

1. Create a virtual environment:
python -m venv venv
venv\Scripts\activate


2. Install the needed libraries:
pip install -r requirements.txt


3. Start the program:
python app.py


4. Open this link in your browser

5. 
## How to Test

- Look at the camera  
- Blink your eyes or open your mouth  
- Click Login  
- If your face matches, the dashboard will open  
- If not, access will be denied  

## Security Notes

- Face photos are not uploaded to GitHub  
- The system blocks repeated wrong login attempts  
- Only real face movement allows login  

## Limitations

- Needs good lighting  
- Needs a webcam  
- Works best when the saved photo and live camera image look similar  

## Future Improvements

- Add a way to register faces from the website  
- Support more than one user  
- Improve mobile design  
- Add an admin panel  

## Author (Optional)

Badri Venkata Durga Prasad  
M.Tech - Cybersecurity
