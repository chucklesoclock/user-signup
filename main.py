from flask import Flask, render_template, request, redirect
import re

app = Flask(__name__)


@app.route('/')
def index():
    error_dict = dict(user_error='', pass_error='', verify_error='', email_error='')
    template = render_template('form.html', user='', email='', **error_dict)
    return template


@app.route('/', methods=['POST'])
def validate():
    user = request.form['user']
    password = request.form['password']
    verify = request.form['verify']
    email = request.form['email']
    new_errors = generate_errors(user, password, verify, email)
    if any(new_errors[error] for error in new_errors):
        return render_template('form.html', user=user, email=email, **new_errors)
    else:
        return redirect('/welcome?name={}'.format(user))


def generate_errors(user, password, verify, email):
    error_dict = dict(user_error='', pass_error='', verify_error='', email_error='')
    if not user or not password:
        if not user:
            error_dict['user_error'] = errors['none']
        else:
            if len(user) > 20:
                error_dict['user_error'] = errors['long']
            elif len(user) < 3:
                error_dict['user_error'] = errors['short']
            else:
                error_dict['user_error'] = errors['spaces'] if ' ' in user else ''
        if not password:
            error_dict['pass_error'] = errors['none']
        else:
            if len(user) > 20:
                error_dict['pass_error'] = errors['long']
            elif len(password) < 3:
                error_dict['pass_error'] = errors['short']
    else:
        # password verification
        good_password = True
        if all(not x.isalpha() for x in password):
            good_password = False
            previous = error_dict['pass_error']
            new = errors['missing'].format('letter') if not previous else previous + ' and 1 letter'
            error_dict['pass_error'] = new
        if all(not x.isdigit() for x in password):
            good_password = False
            previous = error_dict['pass_error']
            new = errors['missing'].format('number') if not previous else previous + ' and 1 number'
            error_dict['pass_error'] = new
        if good_password and password != verify:
            error_dict['verify_error'] = errors['match']
    if email:
        # email verification
        if len(email) > 20:
            error_dict['email_error'] = errors['long']
        elif len(email) < 3:
            error_dict['email_error'] = errors['short']
        else:
            if not re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email):
                error_dict['email_error'] = errors['email']

    return error_dict


@app.route('/welcome', methods=['GET'])
def welcome():
    user = request.args.get('name')
    return render_template('welcome.html', user=user)


errors = {
    'none': 'Why didn\'t you enter anything?',
    'short': 'Too short: please enter at least 3 characters',
    'long': 'Too long: please enter no more than 20 characters',
    'spaces': 'Invalid: please do not include spaces in entry',
    'email': 'Invalid: please enter in format "name@example.com"',
    'match': 'Your passwords did not match O_o'
}

app.run(debug=True)
