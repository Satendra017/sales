import streamlit as st
import pyttsx3
import speech_recognition as sr
import pandas as pd
import numpy as np
import pickle
import threading

# Load the trained ML model
with open("knn_model.pkl", "rb") as f:
    model = pickle.load(f)


# Function to convert text to speech asynchronously
def speak(text):
    st.text(f"🗣️ AI: {text}")  # Display text in UI

    def run():
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)
        engine.say(text)
        engine.runAndWait()

    threading.Thread(target=run, daemon=True).start()


# Function to listen for user response with improved error handling
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening for your response... Please speak now.")
        try:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=10)  # Increased timeout
            user_input = recognizer.recognize_google(audio)
            return user_input.lower()
        except sr.UnknownValueError:
            return "Could not understand the audio."
        except sr.RequestError:
            return "Speech recognition API error."
        except sr.WaitTimeoutError:
            return "No response detected. Please try again."


# Simulated scraped sales lead data
scraped_data = [
    {"Website Visits": 5, "Email Engagement": 7, "Call Interaction": 2, "Requested a Quote": 1,
     "Previous Dealings": 3, "Decision Maker Interaction": 4, "Time to Response": 2,
     "Competitor Engagement": 1, "Lead Score": 85, "Company Size": 3,
     "Industry Type": 2, "Geographical Location": 1},
    {"Website Visits": 10, "Email Engagement": 6, "Call Interaction": 3, "Requested a Quote": 0,
     "Previous Dealings": 5, "Decision Maker Interaction": 2, "Time to Response": 1,
     "Competitor Engagement": 0, "Lead Score": 92, "Company Size": 2,
     "Industry Type": 1, "Geographical Location": 3}
]


# Convert scraped data into ML input format
def prepare_features(data):
    return np.array([
        [lead["Website Visits"], lead["Email Engagement"], lead["Call Interaction"],
         lead["Requested a Quote"], lead["Previous Dealings"], lead["Decision Maker Interaction"],
         lead["Time to Response"], lead["Competitor Engagement"], lead["Lead Score"],
         lead["Company Size"], lead["Industry Type"], lead["Geographical Location"]]
        for lead in data
    ])


# Function to predict conversion probability
def predict_conversion(data):
    X = prepare_features(data)
    if X.shape[1] == model.n_features_in_:
        return model.predict_proba(X)[:, 1]  # Get probability of conversion
    else:
        return ["Feature mismatch! Check input data."]


# Generate AI predictions
predictions = predict_conversion(scraped_data)

# Add AI predictions to scraped data
for i, lead in enumerate(scraped_data):
    lead["Conversion Probability"] = f"{predictions[i] * 100:.2f}%" if isinstance(predictions[i], float) else "Error"

# Streamlit UI
st.title("🧠 AI Sales Lead Validator")

st.write("### Scraped Sales Leads (With AI Predictions):")
df = pd.DataFrame(scraped_data)
st.table(df)

# AI prompts the user
speak("AI has predicted conversion probabilities for these sales leads.")
speak("Say Yes to approve or No to reject.")

# Get user response
user_feedback = listen()

# Display voice input
st.write(f"🎤 You said: **{user_feedback}**")

# Manual confirmation buttons in case speech fails
col1, col2 = st.columns(2)
with col1:
    approve = st.button("✅ Approve Data")
with col2:
    retry = st.button("🔄 Retry Scraping")

# Handle user response
if "yes" in user_feedback or approve:
    st.success("✅ Data Approved! Leads will be saved.")
    speak("Great! The data will be saved.")
elif "no" in user_feedback or retry:
    st.warning("🔄 Retrying... New data will be scraped.")
    speak("Understood. The AI will retry scraping new leads.")
else:
    st.error("⚠️ Could not understand response. Please use buttons.")
    speak("I didn't understand your response. Please use the buttons.")

# --------- NEW: Add Sales Lead Data Section ---------
st.write("### ➕ Add a New Sales Lead")

# User input form
with st.form("add_lead_form"):
    website_visits = st.number_input("Website Visits", min_value=0, value=5)
    email_engagement = st.number_input("Email Engagement", min_value=0, value=5)
    call_interaction = st.number_input("Call Interaction", min_value=0, value=2)
    requested_quote = st.number_input("Requested a Quote", min_value=0, value=1)
    previous_dealings = st.number_input("Previous Dealings", min_value=0, value=3)
    decision_maker_interaction = st.number_input("Decision Maker Interaction", min_value=0, value=2)
    time_to_response = st.number_input("Time to Response", min_value=0, value=2)
    competitor_engagement = st.number_input("Competitor Engagement", min_value=0, value=1)
    lead_score = st.number_input("Lead Score", min_value=0, max_value=100, value=85)
    company_size = st.number_input("Company Size", min_value=1, max_value=5, value=3)
    industry_type = st.number_input("Industry Type", min_value=1, max_value=5, value=2)
    geographical_location = st.number_input("Geographical Location", min_value=1, max_value=5, value=1)

    submit_button = st.form_submit_button("➕ Add Lead")

# Add new data and update table
if submit_button:
    new_lead = {
        "Website Visits": website_visits,
        "Email Engagement": email_engagement,
        "Call Interaction": call_interaction,
        "Requested a Quote": requested_quote,
        "Previous Dealings": previous_dealings,
        "Decision Maker Interaction": decision_maker_interaction,
        "Time to Response": time_to_response,
        "Competitor Engagement": competitor_engagement,
        "Lead Score": lead_score,
        "Company Size": company_size,
        "Industry Type": industry_type,
        "Geographical Location": geographical_location
    }

    # Add new lead to dataset
    scraped_data.append(new_lead)

    # Recalculate predictions
    predictions = predict_conversion(scraped_data)

    # Update new lead's conversion probability
    scraped_data[-1]["Conversion Probability"] = f"{predictions[-1] * 100:.2f}%" if isinstance(predictions[-1],
                                                                                               float) else "Error"

    st.success("✅ New Lead Added Successfully!")

    # Refresh table
    df = pd.DataFrame(scraped_data)
    st.table(df)

    # AI voice confirmation
    speak("New lead added and analyzed successfully!")
