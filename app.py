from flask import Flask, request, jsonify, render_template, session
import os
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Location and club data
locations = {
    "LT BLOCK": "https://maps.app.goo.gl/mNoeBD7Pjdbz2JYD9",
    "SAWMILL (LTS BLOCK)": "https://maps.app.goo.gl/TiSJmpEGnc5DRg737",
    "SYNDICATED HALL (SH)": "https://maps.app.goo.gl/aq66XMQnoRfUJpfe8",
    "PAVILION": "https://maps.app.goo.gl/vVXLxgx36GMFbxjF9",
    "LIB FF": "https://maps.app.goo.gl/Xx6FJ5Vwzy47oVxE9",
    "APP LAB": "https://maps.app.goo.gl/MqmJnxgBgsiuKeM59",
    "ENGINEERING LAB": "https://maps.app.goo.gl/qtHwBKit5fVPMQZa8",
    "OLD AUDITORIUM": "https://maps.app.goo.gl/8MxZU6H6aNbgtcr9A",
    "ODUM BLOCK": "https://maps.app.goo.gl/VczUUxBuH6UduRer5",
    "CAFETERIA": "https://maps.app.goo.gl/8bsySAv8cQpPcQjE7",
    "ADMINISTRATION BLOCK": "https://maps.app.goo.gl/vV5FJtHedVmLwcDz9",
    "IT DIRECTORATE": "https://maps.app.goo.gl/q4wTatyLm2K4LEZGA",
    "UENR BASIC": "https://maps.app.goo.gl/zGaP6FKVa26DoNiW9",
    "FINANCE DIRECTORATE": "https://maps.app.goo.gl/VJ4krFNDrA4mVmeK6",
    "SCHOOL CLINIC": "https://maps.app.goo.gl/QuS3tezmBxGxC4nQ9",
    "CENTER FOR RESEARCH AND APPLIED BIOLOGY": "https://maps.app.goo.gl/WQkwXQGzuT1eY2kN8",
    "SCHOOL FIELD": "https://maps.app.goo.gl/otfc79Gf8tk16dwN6",
    "LIBRARY": "https://maps.app.goo.gl/ZBKb6BVncbN2dRFs7",
    "UNIVERSITY HALL 1": "https://maps.app.goo.gl/u6GuF4aGVStXL3Eg6",
    "UNIVERSITY HALL 2": "https://maps.app.goo.gl/D73haigJyMwwnArK8",
    "UNER POLICE POST": "https://maps.app.goo.gl/t4qwNkEQSwhnz8Br6",
    "REGIONAL CENTRE FOR ENERGY AND ENVIRONMENTAL SUSTAINABILITY": "https://maps.app.goo.gl/ntWJX3YHG1K5UEcPA",
    "NEW AUDITORIUM": "https://maps.app.goo.gl/fAKH55wuTZjv1ar16IS",
    "SKILLS LAB": "https://maps.app.goo.gl/zoKmpWRe3KSSyvoC6",
    "UENR DRIVING SCHOOL": "https://maps.app.goo.gl/SKF2FiZ8g4gMXNC26",
}

clubs = {
    "UENR ROBOTICS CLUB": {
        "description": "The UENR ROBOTICS CLUB-URC is a student-run organization of tech enthusiasts and students from all engineering and science-related disciplines who promote the field of robotics and related technologies.",
        "x_handle": "https://x.com/uenr_robotics?t=5YSB0E_SI95Tb7x44LONJQ&s=09"
    },
    "Google Developer Student Clubs UENR": {
        "description": "Google Developer Student Clubs UENR bridges the gap between theory and practical application for UENR students who are either developers or have an interest in development.",
        "ig": "https://www.instagram.com/gdsc_uenr/",
        "x": "https://x.com/Gdsc_uenr",
        "fb": "https://bit.ly/fb-gdsc_uenr"
    },
    "Huawei ICT Academy": {
        "description": "Huawei ICT Academy partners with academies worldwide to deliver Huawei ICT technologies training, encourage Huawei certification, and develop practical skills for the ICT industry.",
    }
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/message', methods=['POST'])
def handle_message():
    data = request.get_json()
    user_message = data.get('message')
    session['conversation'] = session.get('conversation', [])
    session['conversation'].append({"role": "user", "content": user_message})
    
    response = get_openai_response(user_message)
    session['conversation'].append({"role": "assistant", "content": response})
    
    flask_response = jsonify({'response': response})
    flask_response.headers['Cache-Control'] = 'max-age=86400, stale-while-revalidate=604800'
    return flask_response

def get_openai_response(message):
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json',
    }
    
    prompt_context = (
        "Hello! 👋 I'm the friendly chatbot of the University of Energy and Natural Resources (UENR), and I like to keep our conversations personal and engaging as if I'm the Vice Chancellor. 🎓 "
        "I can assist you with information on admissions 📝, financial aid 💰, academic programs 📚, campus life 🏫, registration procedures 🖊️, and various student services 🛠️. "
        "I can also provide the locations of different blocks on campus 🏢 and information about student clubs 🏆 with Google Map links 🌍. "
        "Feel free to ask me anything about UENR! 😊"
    )


    messages = [{"role": "system", "content": prompt_context}] + session.get('conversation', [])

    if any(loc_name.lower() in message.lower() for loc_name in locations):
        for loc_name, loc_link in locations.items():
            if loc_name.lower() in message.lower():
                return f"The location of {loc_name} can be found here: {loc_link}"
    
    if any(club_name.lower() in message.lower() for club_name in clubs):
        for club_name, club_info in clubs.items():
            if club_name.lower() in message.lower():
                return f"{club_info['description']} You can find more about them here: {club_info.get('x_handle', '')} {club_info.get('ig', '')} {club_info.get('fb', '')}"

    data = {
        "model": "gpt-3.5-turbo-0125",
        "messages": messages,
    }

    try:
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
        response.raise_for_status()
        api_response = response.json()
        print("OpenAI API response:", api_response)
        return api_response['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print("Error during OpenAI API request:", e)
        return "Sorry, I am unable to respond at the moment. Please try again later."

if __name__ == '__main__':
    app.run(debug=True)




# # app.py
# from flask import Flask, request, jsonify, render_template
# import os
# from dotenv import load_dotenv
# import requests

# load_dotenv()

# app = Flask(__name__)

# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# @app.route('/')
# def home():
#     return render_template('index.html')

# # @app.route('/api/message', methods=['POST'])
# # def handle_message():
# #     data = request.get_json()
# #     user_message = data.get('message')
# #     response = get_openai_response(user_message)
# #     return jsonify({'response': response})

# @app.route('/api/message', methods=['POST'])
# def handle_message():
#     data = request.get_json()
#     user_message = data.get('message')
#     response = get_openai_response(user_message)
#     flask_response = jsonify({'response': response})
#     flask_response.headers['Cache-Control'] = 'max-age=86400, stale-while-revalidate=604800'  # Set correct header on your Flask response
#     return flask_response

# def get_openai_response(message):
#     headers = {
#         'Authorization': f'Bearer {OPENAI_API_KEY}',
#         'Content-Type': 'application/json',
#     }
#     prompt_context = (
#         "I am a chatbot knowledgeable about the University of Energy and Natural Resources (UENR) and i make conversation personal as I'm the Vice Chancellor. "
#         "I can provide information on admissions, financial aid, academic programs, campus life,with the neccessary link for student to read more "
#         "registration procedures, and various student services. Ask me anything about UENR!"
#     )
#     data = {
#         "model": "gpt-4o-2024-08-06",
#         "messages": [
#             {"role": "system", "content": prompt_context},
#             {"role": "user", "content": message}
#         ],
#     }
#     response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
#     response.headers['Cache-Control'] = 'max-age=86400, stale-while-revalidate=604800'
#     if response.status_code == 200:
#         return response.json()['choices'][0]['message']['content']
#     else:
#         return "I'm sorry, I couldn't fetch a response. Please try again."
    
#     #response.headers['Cache-Control'] = 'max-age=86400, stale-while-revalidate=604800'


# if __name__ == '__main__':
#     app.run(debug=True)
