from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling search requests
@app.route('/search', methods=['POST'])
def search():
    data = request.json
    university_name = data.get('university_name')

    if not university_name:
        return jsonify({'error': 'University name is required'}), 400

    try:
        # Construct the URL for UCAS course search
        base_url = 'https://digital.ucas.com'
        search_url = f'{base_url}/coursedisplay/courses'
        params = {
            'name': university_name,
            'academicYearId': '2025',  # Adjust as needed
            'courseOptionId': 'bf75a5da-f9a2-41b7-bbef-4d82a5f38675'  # Adjust as needed
        }

        # Perform the search
        response = requests.get(search_url, params=params)
        if response.status_code != 200:
            return jsonify({'error': f'Failed to retrieve data: {response.status_code}'}), 500

        # Parse HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract course details
        course_title = soup.find('h1', class_='course-title').get_text().strip()
        course_summary = soup.find('div', class_='course-summary').get_text().strip()

        # Extract entry requirements
        entry_requirements = soup.find('section', id='entry-requirements')
        if entry_requirements:
            entry_requirements_text = ' '.join([p.get_text().strip() for p in entry_requirements.find_all('p')])
        else:
            entry_requirements_text = 'Entry requirements not specified.'

        # Return JSON response
        return jsonify({
            'title': course_title,
            'summary': course_summary,
            'entry_requirements': entry_requirements_text
        })

    except Exception as e:
        return jsonify({'error': f'Error fetching data: {str(e)}'}), 500

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
