from flask import Blueprint, render_template, request, redirect
import os

home_page_bp = Blueprint('homepage', __name__)

@home_page_bp.route('/')
def dashboard():
    return render_template("index.html")

@home_page_bp.context_processor
def inject_sidebar_data():
    collection_files = [f for f in os.listdir('./temp/collections') if f.endswith('.yml')]
    environment_files = [f for f in os.listdir('./temp/environments') if f.endswith('.yml')]
    return dict(collection_files=collection_files, environment_files=environment_files)


