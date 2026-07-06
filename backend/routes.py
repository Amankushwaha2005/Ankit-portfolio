import os
from flask import Blueprint, request, jsonify
from models import save_contact, save_application
from config import MAX_CONTENT_LENGTH

api = Blueprint('api', __name__)


@api.route('/api/contact', methods=['POST'])
def contact():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    subject = data.get('subject', '').strip()
    message = data.get('message', '').strip()

    if not all([name, email, subject, message]):
        return jsonify({'error': 'All fields are required'}), 400

    if '@' not in email or '.' not in email:
        return jsonify({'error': 'Invalid email address'}), 400

    save_contact(name, email, subject, message)

    return jsonify({
        'message': 'Thank you! Your message has been sent successfully.',
        'success': True
    }), 201


@api.route('/api/apply', methods=['POST'])
def apply():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    position = request.form.get('position', '').strip()
    experience = request.form.get('experience', '').strip()
    message = request.form.get('message', '').strip()
    resume = request.files.get('resume')

    if not all([name, email, phone, position]):
        return jsonify({'error': 'Name, email, phone, and position are required'}), 400

    if '@' not in email or '.' not in email:
        return jsonify({'error': 'Invalid email address'}), 400

    if not resume or resume.filename == '':
        return jsonify({'error': 'Please upload your resume'}), 400

    if request.content_length and request.content_length > MAX_CONTENT_LENGTH:
        return jsonify({'error': 'File size must be less than 5MB'}), 400

    try:
        save_application(name, email, phone, position, experience, message, resume)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception:
        return jsonify({'error': 'Failed to upload resume. Please try again.'}), 500

    return jsonify({
        'message': 'Application submitted successfully! We will review your resume and contact you soon.',
        'success': True
    }), 201


@api.route('/api/contacts', methods=['GET'])
def get_contacts():
    from models import get_db
    conn = get_db()
    rows = conn.execute('SELECT * FROM contacts ORDER BY created_at DESC').fetchall()
    conn.close()
    contacts = [dict(row) for row in rows]
    return jsonify(contacts)


@api.route('/api/applications', methods=['GET'])
def get_applications():
    from models import get_db
    conn = get_db()
    rows = conn.execute(
        'SELECT id, name, email, phone, position, experience, resume_filename, created_at FROM applications ORDER BY created_at DESC'
    ).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])
