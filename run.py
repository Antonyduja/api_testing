# run.py
from app import create_app
import os

app = create_app()

@app.context_processor
def inject_sidebar_data():
    collection_files = [f for f in os.listdir('./temp/collections') if f.endswith('.yml')]
    environment_files = [f for f in os.listdir('./temp/environments') if f.endswith('.yml')]
    return dict(collection_files=collection_files, environment_files=environment_files)

if __name__ == '__main__':
    app.run(debug=True)