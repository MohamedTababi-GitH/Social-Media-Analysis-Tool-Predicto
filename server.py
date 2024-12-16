from flask import Flask, render_template, request
from TrendAnalyzer import analyze_frequency_modin, get_top_topics
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('new_template/index.html', term=None)

@app.route('/analyze-trend', methods=['GET', 'POST'])
def analyze_trend():
    term = None
    results = None
    if request.method == 'POST':
        term = request.form.get('term')  
        if term:  
            try:
                results = get_top_topics()
                print(results) 
            except Exception as e:
                results = f"An error occurred: {str(e)}"
    return render_template('new_template/index.html', term=term)

if __name__ == '__main__':
    app.run(debug=True)
