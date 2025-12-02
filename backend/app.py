# VirtualLab/backend/app.py
from flask import Flask, render_template

app = Flask(
    __name__,
    template_folder='../frontend',
    static_folder='../frontend/src'
)

# --- ROUTES ---
@app.route('/')
def index():
    return render_template('index.html')
    
# Pages
@app.route('/learn')
def learn_page():
    return render_template('pages/learn_page.html')

@app.route('/practice')
def practice_page():
    return render_template('pages/practice_page.html')

# Learn Pages
@app.route('/learn/file-analysis')
def intro_file_analysis():
    return render_template('/learn/intro_file_analysis.html')

@app.route('/learn/metadata-investigation')
def intro_metadata_investigation():
    return render_template('/learn/intro_metadata_investigation.html')

@app.route('/learn/digital-footprint')
def intro_digital_footprint():
    return render_template('/learn/intro_digital_footprint.html')

# Practice Pages
@app.route('/file-analysis')
def file_analysis():
    return render_template('/practice/file_analysis.html')

@app.route('/metadata-investigation')
def metadata_investigation():
    return render_template('/practice/metadata_investigation.html')

@app.route('/digital-footprint')
def digital_footprint():
    return render_template('/practice/digital_footprint.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)