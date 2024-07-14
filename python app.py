from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Define route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Define route for handling search requests
@app.route('/search', methods=['POST'])
def search():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        response = requests.get(url)
        if response.status_code != 200:
            return jsonify({'error': 'Failed to retrieve the webpage'}), 500

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the course title
        title = soup.find('h1').get_text().strip() if soup.find('h1') else 'N/A'

        # Extract the course summary
        summary = soup.find('div', class_='course-summary').get_text().strip() if soup.find('div', class_='course-summary') else 'N/A'

        # Extract entry requirements
        entry_requirements = soup.find('section', id='entry-requirements')
        entry_requirements_text = ''
        if entry_requirements:
            requirements_text = entry_requirements.find_all(['p', 'li'])
            entry_requirements_text = ' '.join([req.get_text().strip() for req in requirements_text])

        return jsonify({
            'title': title,
            'summary': summary,
            'entry_requirements': entry_requirements_text
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
