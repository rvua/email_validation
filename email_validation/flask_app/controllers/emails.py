from flask import render_template, redirect, request 
from flask_app import app 
from flask_app.models.email import Email 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate():
    if not Email.is_valid(request.form):
        return redirect('/')
    Email.save(request.form)
    return redirect('/success')

@app.route('/success')
def success():
    return render_template('/success.html', emails=Email.get_all_emails())

