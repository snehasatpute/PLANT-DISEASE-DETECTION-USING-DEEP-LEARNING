from flask import Flask, render_template, request, redirect, session, url_for, send_from_directory, flash
import numpy as np
import json
import uuid
import tensorflow as tf
import os


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load model
model = tf.keras.models.load_model("models/plant_disease_recog_model_pwp.keras")

# Load labels and info
with open("plant_disease.json", 'r', encoding='utf-8') as file:
    plant_disease = json.load(file)

# Language and region options
LANGUAGES = ['English', 'Hindi', 'Marathi']
REGIONS = [
    'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
    'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka',
    'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
    'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
    'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'
]

@app.route('/uploadimages/<path:filename>')
def uploaded_images(filename):
    return send_from_directory('uploadimages', filename)

@app.route('/')
def home():
    if not session.get("logged_in"):
        return redirect("/login")

    language = session.get("language", "English")
    region = session.get("region", "Maharashtra")

    return render_template('home.html', language=language, region=region,
                           languages=LANGUAGES, regions=REGIONS)

@app.route('/set_preferences', methods=['POST'])
def set_preferences():
    session['language'] = request.form.get('language', 'English')
    session['region'] = request.form.get('region', 'Maharashtra')
    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == '1234':
            session['logged_in'] = True
            return redirect('/')

        if os.path.exists('users.json'):
            with open('users.json', 'r') as f:
                users = json.load(f)

            for user in users:
                if user['username'] == username and user['password'] == password:
                    session['logged_in'] = True
                    return redirect('/')

        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']

        if os.path.exists('users.json'):
            with open('users.json', 'r') as f:
                users = json.load(f)
        else:
            users = []

        for user in users:
            if user['username'] == email:
                return render_template('signup.html', error="User already exists.")

        users.append({'username': email, 'password': password})
        with open('users.json', 'w') as f:
            json.dump(users, f)

        flash("Account created successfully. Please log in.")
        return redirect('/login')

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/contact')
def contact():
    return render_template('contact.html', email="fhasalcrop34@gmail.com", phone="7020880420")

# Image feature extraction and prediction
def extract_features(image):
    image = tf.keras.utils.load_img(image, target_size=(160, 160))
    feature = tf.keras.utils.img_to_array(image)
    feature = np.expand_dims(feature, axis=0)
    return feature

def model_predict(image, lang="English"):
    img = extract_features(image)
    prediction = model.predict(img)
    label_index = prediction.argmax()
    data = plant_disease[label_index]

    translated_result = {
        "name": data["name"].get(lang, data["name"]["English"]),
        "cause": data["cause"].get(lang, data["cause"]["English"]),
        "cure": data["cure"].get(lang, data["cure"]["English"])
    }
    return translated_result

@app.route('/upload/', methods=['POST'])
def uploadimage():
    if not session.get("logged_in"):
        return redirect("/login")

    image = request.files['img']
    filename = f"uploadimages/temp_{uuid.uuid4().hex}_{image.filename}"
    image.save(filename)

    lang = session.get("language", "English")
    region = session.get("region", "Maharashtra")
    prediction = model_predict(filename, lang)

    return render_template('home.html', result=True, imagepath=f'/{filename}',
                           prediction=prediction, language=lang, region=region,
                           languages=LANGUAGES, regions=REGIONS)

if __name__ == "__main__":
    if not os.path.exists("uploadimages"):
        os.makedirs("uploadimages")
    app.run(debug=True)

