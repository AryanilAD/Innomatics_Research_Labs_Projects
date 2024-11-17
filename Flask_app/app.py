from flask import Flask, render_template, request
import re
import datetime

app = Flask(__name__)

@app.route('/')
def welcome():
    current_hour = datetime.datetime.now().hour
    # Choose an emoji based on the time of day
    if 5 <= current_hour < 12:
        emoji = "☀️"
    elif 12 <= current_hour < 18:
        emoji = "🌤️"
    else:
        emoji = "🌙"
    return render_template('welcome.html', emoji=emoji)

# Route for the main Regex Matching page
@app.route('/regex_app', endpoint='regex_app')
def regex_app():
    return render_template('index.html')

# Route for regex matching results
@app.route('/results', methods=['POST'])
def results():
    test_string = request.form['test_string']
    regex = request.form['regex']
    matches = re.findall(regex, test_string)
    return render_template('index.html', test_string=test_string, regex=regex, matches=matches)

# Route for the email validator page
@app.route('/email_validator')
def email_validator():
    return render_template('email_validator.html', email=None, is_valid= None)

# Route for email validation results
@app.route('/validate_email', methods=['POST'])
def validate_email():
    email = request.form['email']
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    is_valid = re.match(email_pattern, email) is not None
    return render_template('email_validator.html', email=email, is_valid=is_valid)

if __name__ == '__main__':
    app.run(debug=True, host ='0.0.0.0', port=5000)
