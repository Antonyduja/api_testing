from flask import Blueprint, render_template, request, redirect, url_for
import os, yaml

environments_bp = Blueprint('environments', __name__)
ENVIRONMENT_PATH = './temp/environments'

@environments_bp.route('/environments')
def environments():
    files = [f for f in os.listdir(ENVIRONMENT_PATH) if f.endswith('.yml') or f.endswith('.yaml')]
    return render_template('environments.html', files=files)

@environments_bp.route('/environment/new', methods=['GET', 'POST'])
def new_collection():
    if request.method == 'POST':
        name = request.form['name']
        content = {
        }
        filepath = os.path.join(ENVIRONMENT_PATH, f"{name}.yml")
        with open(filepath, 'w') as f:
            yaml.dump(content, f)
        return redirect(url_for('environments.environments'))
    return render_template('environment_form.html')

@environments_bp.route('/environment/delete/<filename>')
def delete_environment(filename):
    filepath = os.path.join(ENVIRONMENT_PATH, filename)
    print(filepath)
    os.path.delete(filepath)
    return render_template()

@environments_bp.route('/environment/view/<filename>')
def view_environment(filename):
    filepath = os.path.join(ENVIRONMENT_PATH, filename)
    if not os.path.exists(filepath):
        return "File not found", 404
    with open(filepath, 'r') as f:
        content = yaml.safe_load(f)
    return render_template('environment_view.html', content=content, filename=filename)

@environments_bp.route('/environment/update/<filename>', methods=['POST'])
def update_environment(filename):
    filepath = os.path.join(ENVIRONMENT_PATH, filename)
    if not os.path.exists(filepath):
        return "File not found", 404

    with open(filepath, 'r') as f:
        content = yaml.safe_load(f) or {}

    # Handle Delete
    if 'delete_key' in request.form:
        delete_key = request.form['delete_key']
        if delete_key in content:
            del content[delete_key]

    # Handle Add
    elif 'add' in request.form:
        new_key = request.form.get('new_key', '').strip()
        new_value = request.form.get('new_value', '').strip()
        if new_key:
            content[new_key] = new_value

    # Handle Update (Key and Value)
    elif 'update' in request.form:
        updated_content = {}
        index = 0
        while True:
            orig_key = request.form.get(f'orig_key_{index}')
            new_key = request.form.get(f'edit_key_{index}')
            new_value = request.form.get(f'edit_value_{index}')
            if orig_key is None:
                break
            if new_key:
                updated_content[new_key] = new_value
            index += 1
        content = updated_content

    with open(filepath, 'w') as f:
        yaml.safe_dump(content, f)

    return redirect(url_for('environments.view_environment', filename=filename))


