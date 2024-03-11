from flask import Flask, render_template, request
from datetime import datetime #imports the datetime class from the datetime module in Python's standard library
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) #create an instance of a flask web application
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

#Initialize Database:
class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(10))
    problem_description = db.Column(db.String(400)) #Free text up to 300 chars-Example: “My device is making weird noises”
    device_serial_number = db.Column(db.String(100), nullable=False) #64 chars-Example: “24-X-125447-DC”
    light1 = db.Column(db.String(10), nullable=False)
    light2 = db.Column(db.String(10), nullable=False)
    light3 = db.Column(db.String(10), nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.now)
    response_status = db.Column(db.String(100))



def create_database():
    with app.app_context():
        db.create_all()


# Define the home page
@app.route("/")
def home():
    return render_template("index.html")


# Get data from form submission
@app.route("/process_input", methods=["POST"])
def process_input():
    user_id = request.form.get('user_id')
    problem_description = request.form.get('problem_description')
    device_serial_number = request.form.get('device_serial_number')
    light1 = request.form.get('light1')
    light2 = request.form.get('light2')
    light3 = request.form.get('light3')

    error_message = []

    if user_id is None or not user_id.isdigit():
        error_message.append('Invalid user ID.')

    if len(problem_description) > 300:
        error_message.append('Problem description cannot exceed 300 characters.')
        
    if not device_serial_number:
        error_message.append('Device serial number is required.')

    elif len(device_serial_number) > 64:
        error_message.append('Device serial number cannot exceed 64 characters.')


    if not all ([light1, light2, light3]):
        error_message.append('Please select a status for all indicator lights.')  

    if error_message:
        return render_template("index.html", error_message=error_message)

    # Calculate response status
    response_status = calculate_response_status(device_serial_number, light1, light2, light3)

    # Save data to database
    form_data = FormData(
        user_id=user_id,
        problem_description=problem_description,
        device_serial_number=device_serial_number,
        light1=light1,
        light2=light2,
        light3=light3,
        response_status=response_status
    )
    db.session.add(form_data)
    db.session.commit()

    # Display response status on a new page
    return render_template("response.html", response_status=response_status)


def calculate_response_status(device_serial_number, light1, light2, light3):
    if device_serial_number.startswith("24-X"):
        return "Please upgrade your device"
    elif device_serial_number.startswith("36-X"):
            if light1 == "off" and light2 == "off" and light3 == "off":
                return "Turn on the device"
            elif [light1, light2, light3].count("blinking") >= 2:
                return "Please wait"
            elif light1 == "on" and light2 == "on" and light3 == "on":
                return "ALL is ok" 
            else:
                return "Unknown device"

    elif device_serial_number.startswith("51-B"):
        if light1 == "off" and light2 == "off" and light3 == "off":
            return "Turn on the device"
        elif "blinking" in [light1, light2, light3]:
            return "Please wait"
        elif [light1, light2, light3].count("on") > 1 and [light1, light2, light3].count("blinking") == 0:
            return "ALL is ok"
        else:
            return "Unknown device"
    elif device_serial_number.isdigit():
        return "Bad serial number"
    else:
        return "Unknown device"


if __name__ == "__main__":
    create_database()
    app.run(debug=True)