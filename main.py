import os
import io
import PyPDF2
from deep_translator import GoogleTranslator
from fpdf import FPDF
from gtts import gTTS
import streamlit as st

# Function to extract text from PDF
def extract_text(pdf_file: io.BytesIO) -> [str]:
    reader = PyPDF2.PdfReader(pdf_file)
    pdf_text = []
    for page in reader.pages:
        content = page.extract_text()
        if content:
            pdf_text.append(content)
    return pdf_text

# Function to translate extracted text
def translate_text(extracted_text, target_language):
    translator = GoogleTranslator(target=target_language)
    translated_pages = []
    for text in extracted_text:
        try:
            translation = translator.translate(text)
            translated_pages.append(translation)
        except Exception as e:
            print(f"Translation error: {e}")
            translated_pages.append("Translation error")
    return translated_pages

# Function to create a PDF from translated text
def create_pdf(translated_text, font_path='DejaVuSans.ttf'):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Check if the font file exists and is accessible
    if not os.path.isfile(font_path):
        raise FileNotFoundError(f"TTF Font file not found: {font_path}")

    pdf.add_page()
    pdf.add_font("DejaVuSans", style='', fname=font_path)
    pdf.set_font("DejaVuSans", size=12)

    for page_num, translation in enumerate(translated_text, start=1):
        pdf.add_page()
        pdf.set_font("DejaVuSans", size=12)
        pdf.multi_cell(0, 10, translation.encode('latin-1', 'replace').decode('latin-1'))

    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output

# Function to create an audiobook from translated text
def create_audiobook(translated_text):
    temp_audio_files = []
    for page_num, translation in enumerate(translated_text, start=1):
        try:
            tts = gTTS(text=translation, lang='en')  # Use appropriate language code
            temp_audio_file = f"page_{page_num}.mp3"
            tts.save(temp_audio_file)
            temp_audio_files.append(temp_audio_file)
        except Exception as e:
            print(f"Audio generation error: {e}")

    audiobook_output = io.BytesIO()
    with open('audiobook.mp3', 'wb') as final_audio:
        for temp_file in temp_audio_files:
            with open(temp_file, 'rb') as f:
                final_audio.write(f.read())
            os.remove(temp_file)

    with open('audiobook.mp3', 'rb') as f:
        audiobook_output.write(f.read())

    audiobook_output.seek(0)
    return audiobook_output

# Streamlit UI
def main():
    st.title("PDF Translator and Audiobook Generator")
    st.write("Upload a PDF file to translate its content and generate an audiobook.")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file:
        target_language = st.text_input("Enter the Target Language (e.g., 'fr' for French, 'es' for Spanish):")

        if st.button('Process'):
            if not target_language:
                st.error("Please enter a target language.")
            else:
                # Extract text
                extracted_text = extract_text(uploaded_file)

                # Translate text
                translated_text = translate_text(extracted_text, target_language)

                # Create translated PDF
                try:
                    pdf_output = create_pdf(translated_text)
                    st.download_button(
                        label="Download Translated PDF",
                        data=pdf_output,
                        file_name='translated_output.pdf',
                        mime='application/pdf'
                    )
                except Exception as e:
                    st.error(f"Error creating PDF: {e}")

                # Create audiobook
                try:
                    audiobook_output = create_audiobook(translated_text)
                    st.download_button(
                        label="Download Audiobook",
                        data=audiobook_output,
                        file_name='audiobook.mp3',
                        mime='audio/mpeg'
                    )
                except Exception as e:
                    st.error(f"Error creating audiobook: {e}")

if __name__ == "__main__":
    main()
