# PDF Speak

PDF Speak is a web-based tool designed to translate PDF documents into different languages and generate an audiobook from the translated content. It is built using Python libraries like `PyPDF2`, `deep_translator`, `FPDF`, and `gTTS` combined with Streamlit to offer a user-friendly interface. The project allows users to upload PDFs, translate their content, download the translated PDF, and generate an audio version of the translated text.

This project serves as an excellent learning opportunity to explore PDF text extraction, translation APIs, text-to-speech conversion, and building simple web applications with Streamlit.

## Features
- **Upload PDF**: Upload a PDF document to extract its text content.
- **Translate Text**: Choose a target language to translate the extracted text into.
- **Download Translated PDF**: The translated content can be downloaded as a PDF.
- **Generate Audiobook**: Create an audiobook from the translated text in the target language and download it in MP3 format.

---

## File Structure

```
pdf-speak/
│
├── fonts/                            # Custom fonts for PDF generation (optional)
│   └── DejaVuSans.ttf                
├── main.py                           # Main application code
├── requirements.txt                  # Python dependencies
└── README.md                         # Project documentation
```

---

## Installation

1. **Clone the Repository**

   Clone this repository to your local machine using:
   ```bash
   git clone https://github.com/yourusername/pdf-speak.git
   ```

2. **Install the Required Packages**

   Navigate into the project directory and install the necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**

   You can start the Streamlit app with the following command:
   ```bash
   streamlit run main.py
   ```

---

## Usage

1. Open the web interface by running the application.
2. Upload a PDF file using the file uploader.
3. Input the target language (e.g., 'fr' for French, 'es' for Spanish).
4. Click the "Process" button to start translation and audiobook generation.
5. Download the translated PDF or the generated audiobook from the download buttons provided on the interface.

---

## Code Overview

### `main.py`

- **Text Extraction**: Uses `PyPDF2` to extract text from the uploaded PDF document.
  ```python
  reader = PyPDF2.PdfReader(pdf_file)
  for page in reader.pages:
      content = page.extract_text()
  ```

- **Text Translation**: Utilizes the `deep_translator.GoogleTranslator` to translate the extracted text to the desired language.
  ```python
  translator = GoogleTranslator(target=target_language)
  translation = translator.translate(text)
  ```

- **PDF Generation**: The translated text is formatted and converted into a downloadable PDF using the `FPDF` library.
  ```python
  pdf.add_font("DejaVuSans", style='', fname=font_path)
  pdf.multi_cell(0, 10, translation.encode('latin-1', 'replace').decode('latin-1'))
  ```

- **Audiobook Generation**: Converts the translated text into speech using Google Text-to-Speech (`gTTS`) and saves it as an MP3 file.
  ```python
  tts = gTTS(text=translation, lang='en')
  tts.save(temp_audio_file)
  ```

- **Streamlit Interface**: Provides a simple UI for uploading the PDF, selecting the language, and generating both the translated PDF and audiobook.
  ```python
  uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
  target_language = st.text_input("Enter the Target Language")
  ```

---

## Requirements

The required dependencies for this project are specified in the `requirements.txt` file:

```
streamlit
PyPDF2
deep-translator
fpdf
gTTS
```

To install them, simply run:
```bash
pip install -r requirements.txt
```

---

## Limitations

- Translation accuracy relies on the `deep_translator` library and may vary depending on the language and text complexity.
- Text extraction might not work perfectly with scanned PDFs or PDFs with complex formatting.
- The generated audiobook language is set to English (`gTTS` default) by design, but this can be changed based on the target language.

---

## Disclaimer

This project is created for **learning purposes** and is not designed to be used in a production environment.
