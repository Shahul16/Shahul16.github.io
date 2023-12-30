from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Define a model for the Contact form
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)

# Ensure the database tables are created before running the app
with app.app_context():
    db.create_all()

# ...

@app.route('/forms/contact', methods=['POST'])
def contact_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        # Create a new Contact instance
        new_contact = Contact(name=name, email=email, subject=subject, message=message)

        try:
            # Add the new Contact instance to the session
            db.session.add(new_contact)

            # Commit changes to the database
            db.session.commit()

            return jsonify({'status': 'success', 'message': 'Your message has been sent. Thank you!'})
        except SQLAlchemyError as e:
            # Rollback changes if a SQLAlchemyError occurs
            db.session.rollback()
            # Handle the exception if needed
            # ...

            return jsonify({'status': 'error', 'message': 'An error occurred.'})

    return jsonify({'status': 'error', 'message': 'Invalid request method.'})
