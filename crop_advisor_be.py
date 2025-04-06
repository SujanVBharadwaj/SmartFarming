from flask import Flask, jsonify, render_template
from cropadvisor import CropAdvisor

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('cropadvisor.html')

@app.route('/run')
def run_crop_advisor():
    advisor = CropAdvisor()
    result = advisor.analyze()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
