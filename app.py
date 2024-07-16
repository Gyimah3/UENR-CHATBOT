from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management
CORS(app)

# Set up Google API key and configure genai
#os.environ["GOOGLE_API_KEY"] = 'AIzaSyBkpkOJMjbADblWa7jsRxJtFsNSG9QW3Pw'
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-pro')

# Location and club data (as in your original code)
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
    
    # Initialize or get the conversation history
    session['conversation'] = session.get('conversation', [])
    session['conversation'].append({"role": "user", "content": user_message})
    
    response = get_gemini_response(user_message, session['conversation'])
    
    # Add the assistant's response to the conversation history
    session['conversation'].append({"role": "assistant", "content": response})
    
    flask_response = jsonify({'response': response})
    flask_response.headers['Cache-Control'] = 'max-age=86400, stale-while-revalidate=604800'
    return flask_response

def get_gemini_response(message, conversation_history):
    # Check for location or club queries first
    for loc_name, loc_link in locations.items():
        if loc_name.lower() in message.lower():
            return f"The location of {loc_name} can be found here: {loc_link}"
    
    for club_name, club_info in clubs.items():
        if club_name.lower() in message.lower():
            return f"{club_info['description']} You can find more about them here: {club_info.get('x_handle', '')} {club_info.get('ig', '')} {club_info.get('fb', '')}"

    # Prepare the conversation history
    context = "\n".join([f"{'Human' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}" for msg in conversation_history])
    
    prompt = f"""You are a friendly chatbot of the University of Energy and Natural Resources (UENR), and I like to keep our conversations personal and engaging as if I'm the Vice Chancellor. 🎓 "
        "I can assist you with information on admissions 📝, financial aid 💰, academic programs 📚, campus life 🏫, registration procedures 🖊️, and various student services 🛠️. "
        "I can also provide the locations of different blocks on campus 🏢 and information about student clubs 🏆 with Google Map links 🌍. "
        "Feel free to ask me anything about UENR! 😊.

    Here are some guidelines for your responses:
    1. Always maintain a friendly and professional tone.
    2. If you're not sure about something, say so politely and offer to help with related information you do know.
    3. Provide concise answers for simple questions, but offer more detailed explanations for complex topics.
    4. If a user expresses interest in a topic, offer to expand on it or suggest related areas they might find interesting.
    5. Always prioritize information directly related to UENR and its benefits for education.
    6. If a user asks about something not directly related to UENR, try to bridge the topic back to relevant UENR concepts if possible.
    7. When asked for a link on UENR, refer the user to the official UENR website.
    8. Be encouraging and positive about the benefits of studying at UENR, but remain factual and avoid exaggeration.
    9. You can provide information on admissions, financial aid, academic programs, campus life, registration procedures, and various student services.
    10. You also have access to information about campus locations and student clubs, which you can share when relevant.
    
    Conversation History:
    {context}
    
    Human: {message}
    Assistant:"""
    
    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    app.run(debug=True)