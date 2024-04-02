import streamlit as st
import zipfile
import assemblyai as ai
from textblob import TextBlob

# Function to extract MP3 files from a zip file
def extract_mp3_from_zip(zip_file):
    extracted_files = []
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        file_list = zip_ref.namelist()
        mp3_files = [file for file in file_list if file.endswith('.mp3')]
        # Extracting the MP3 files
        for mp3_file in mp3_files:
            zip_ref.extract(mp3_file)
            extracted_files.append(mp3_file)
    return extracted_files

# Function to transcribe the audio file 
def transcribe_audio(audio_file, api_key):
    ai.settings.api_key = api_key
    transcriber = ai.Transcriber()

    try:
        transcript = transcriber.transcribe(audio_file)
        return transcript.text
    except Exception as e:
        st.error(f"Transcription failed: {e}")
        return None

# Function to analyze sentiment
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"
    
# Function to calculate error rate
def error_rate_calculation(text):
    keywords = ["fault", "mistake", "problem", "incorrect", "issue", "apology", "sorry"]
    errors = sum(text.lower().count(keyword) for keyword in keywords)
    total_words = len(text.split())
    return ((errors/total_words)*100)

# Function to calculate resolution rate
def resolution_rate_calculation(text):
    keywords = ["resolved", "satisfied", "problem solved", "resolving"]
    issue_resolved = any(keyword in text.lower() for keyword in keywords)
    resolution_rate = 1 if issue_resolved else 0
    return resolution_rate

#Function to calculate abandonment rate
def abandonment_rate_calculation(text):
    keywords = ["disconnected", "hung up"]
    abandoned_calls = sum(text.lower().count(keyword) for keyword in keywords)
    return abandoned_calls

# Function to read text from file
def read_text_from_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    return text

def main():
    st.title("Quality Management System")
    st.write("Please upload a zip file containing MP3 files.")

    zip_file = st.file_uploader("Upload Zip File", type=['zip'])
    
    if zip_file is not None:
        # Extract MP3 files from the uploaded zip file
        extracted_files = extract_mp3_from_zip(zip_file)

        api_key = "2ff0709983594e23823ce6cc5683cf11"

        if extracted_files:
            st.write("MP3 files extracted successfully:")
            for file in extracted_files:
                st.write(file)

            # Transcriptions and Sentiment Analysis
            st.write("Quality Analysis:")
            for mp3_file in extracted_files:
                # Transcribe each MP3 file
                transcription = transcribe_audio(mp3_file, api_key)
                if transcription:
                    st.write(f"{mp3_file}: {transcription}")
                    
                    # Write transcribed text to a text file
                    text_file_path = f"{mp3_file}.txt"
                    with open(text_file_path, 'w') as text_file:
                        text_file.write(transcription)
                        
                    sentiment = analyze_sentiment(transcription)
                    st.write(f"Sentiment for {mp3_file}: {sentiment}")
                    
                    error_rate = error_rate_calculation(transcription)
                    st.write(f"Error Rate for {mp3_file}: {error_rate}")
                    
                    resolution_rate = resolution_rate_calculation(transcription)
                    st.write(f"Resolution Rate for {mp3_file}: {resolution_rate}")
                    
                    abandonment_rate = abandonment_rate_calculation(transcription)
                    st.write(f"Abandonment Rate for {mp3_file}: {abandonment_rate}")
                
                else:
                    st.write(f"{mp3_file}: Transcription failed")
    
if __name__ == "__main__":
    main()
