from flask import Blueprint, render_template, request, redirect, url_for
import os, yaml

collections_bp = Blueprint('collections', __name__)
COLLECTION_PATH = './temp/collections'

@collections_bp.route('/collections')
def collections():
    files = [f for f in os.listdir(COLLECTION_PATH) if f.endswith('.yml') or f.endswith('.yaml')]
    return render_template('collections.html', files=files)

@collections_bp.route('/collections/new', methods=['GET', 'POST'])
def new_collection():
    if request.method == 'POST':
        name = request.form['name']
        content = {
            'name': name,
            'requests': []
        }
        filepath = os.path.join(COLLECTION_PATH, f"{name}.yml")
        with open(filepath, 'w') as f:
            yaml.dump(content, f)
        return redirect(url_for('collections.collections'))
    return render_template('collection_form.html')

@collections_bp.route('/collections/view/<filename>')
def view_collection(filename):
    filepath = os.path.join(COLLECTION_PATH, filename)
    if not os.path.exists(filepath):
        return "Collection file not found", 404
    with open(filepath, 'r') as f:
        content = yaml.safe_load(f)
    return render_template('collection_view.html', content=content, filename=filename)

@collections_bp.route('/collections/<filename>/request/<int:request_index>', methods=['GET', 'POST'])
def request_detail(filename, request_index):
    filepath = os.path.join(COLLECTION_PATH, filename)
    if not os.path.exists(filepath):
        return "Collection file not found", 404

    with open(filepath, 'r') as f:
        collection = yaml.safe_load(f)

    try:
        request_data = collection['requests'][request_index]
    except (IndexError, KeyError):
        return "Request not found", 404

    response_data = None

    if request.method == 'POST':
        method = request.form['method']
        url = request.form['url']
        headers = {}
        query_params = {}
        body = request.form.get('body_raw', '').strip()

        # Parse headers
        for k, v in zip(request.form.getlist('header_key'), request.form.getlist('header_value')):
            if k:
                headers[k] = v

        # Parse query params
        for k, v in zip(request.form.getlist('query_key'), request.form.getlist('query_value')):
            if k:
                query_params[k] = v

        try:
            req = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=query_params,
                data=body
            )
            response_data = {
                "status_code": req.status_code,
                "headers": dict(req.headers),
                "body": req.text
            }
        except Exception as e:
            response_data = {"error": str(e)}

        # Reflect updated fields back
        request_data.update({
            "method": method,
            "url": url,
            "headers": headers,
            "query_params": query_params,
            "body": {
                "mode": "raw",
                "raw": body
            }
        })

    return render_template(
        'request_detail_view.html',
        request_data=request_data,
        collection_name=collection['name'],
        filename=filename,
        request_index=request_index,
        response_data=response_data
    )
