from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # 1. Personal Information
    first_name = request.form.get('name')
    middle_name = request.form.get('middlename')
    last_name = request.form.get('lastname')
    email = request.form.get('email')
    reg_num = request.form.get('registrationnumber')
    enroll_date = request.form.get('enrollmentdate')
    gender = request.form.get('gender')

    # 2. Address Details
    addr1 = request.form.get('addressline1')
    addr2 = request.form.get('addressline2')
    city = request.form.get('city')
    state = request.form.get('stateprovinceregion')
    zip_code = request.form.get('zippostalcode')
    country = request.form.get('country')

    # 3. Additional Info
    message = request.form.get('message')

    # For testing: Print the data to your VS Code terminal
    print("--- New Student Admission Received ---")
    print(f"Name: {first_name} {middle_name} {last_name}")
    print(f"Email: {email} | Registration: {reg_num}")
    print(f"Location: {city}, {country}")
    print(f"Message: {message}")
    print("---------------------------------------")

    # Return a simple confirmation page
    return f"""
    <div style="font-family: sans-serif; text-align: center; padding: 50px;">
        <h1 style="color: #4caf50;">Application Submitted!</h1>
        <p>Thank you, <strong>{first_name}</strong>. We have received your enrollment for <strong>{enroll_date}</strong>.</p>
        <a href="/" style="color: #4caf50; text-decoration: none; font-weight: bold;">← Back to Form</a>
    </div>
    """

if __name__ == '__main__':
    app.run(debug=True)