# sales

AI Sales Lead Validator

Overview

The AI Sales Lead Validator is a Streamlit-based web application that helps businesses analyze and predict the conversion probability of sales leads using machine learning. The system allows users to:

Scrape and display sales leads data.

Predict conversion probabilities using a pre-trained KNN model.

Take user feedback via speech recognition.

Manually approve or reject scraped data.

Add new sales leads manually.

Features

✅ Sales Lead Scraping & Display – Scrapes sales lead data and presents it in a table format.
✅ Machine Learning Predictions – Uses a trained KNN model to predict conversion probabilities.
✅ Voice Interaction – AI assistant provides verbal feedback and listens to user responses.
✅ Manual Data Approval – Users can approve or reject sales leads via voice commands or buttons.
✅ New Lead Addition – Allows users to add new sales leads manually via an interactive form.
✅ Real-time Updates – Newly added leads are automatically analyzed and displayed with predictions.

Installation

1. Clone the Repository

git clone https://github.com/your-repo/ai-sales-lead-validator.git
cd ai-sales-lead-validator

2. Install Dependencies

pip install -r requirements.txt

3. Run the Application

streamlit run app.py

Usage

Running the Application

1.Start the Streamlit app using the command: streamlit run app.py

2.View the scraped sales lead data and AI-generated conversion probabilities.

3.Interact with the AI assistant by approving or rejecting the data.

4.Use the "Add a New Sales Lead" form to manually input a new lead.

5.Newly added leads are analyzed and displayed instantly.

File Structure

├── ai-sales-lead-validator/
│   ├── app.py                # Main application file
│   ├── knn_model.pkl         # Pre-trained KNN model
│   ├── requirements.txt      # Dependencies
│   ├── README.md             # Documentation

Dependencies

streamlit

pyttsx3

speechrecognition

numpy

pandas

pickle

Future Enhancements

🔹 Implement real-time web scraping for dynamic sales lead generation.
🔹 Add user authentication for personalized experience.
🔹 Integrate additional ML models for improved accuracy.

Contributing

Contributions are welcome! Feel free to fork this repo and submit a pull request with improvements.

License

This project is licensed under the MIT License.

