## Overview

This Flask application provides a simple web interface for processing text input and files. Users can upload text files or input text directly to generate multiple-choice questions. The application also supports downloading results in PDF and Word formats. 


## Technology and Methodology

### Technologies Used

- **[spaCy](https://spacy.io/):** A powerful NLP library for processing and analyzing text. It is used for tokenization, lemmatization, and sentence segmentation.
- **[scikit-learn](https://scikit-learn.org/):** A machine learning library for Python. It provides tools for vectorization and feature extraction, specifically using the `TfidfVectorizer` for transforming text data into numerical features.
- **[NumPy](https://numpy.org/):** A library for numerical computations in Python. It is used for handling and manipulating arrays, such as sorting and selecting feature scores.

### Methodology

1. **Text Preprocessing:**
   - Convert the input text to lowercase and remove newline characters.
   - Use spaCy to split the text into sentences and tokens.
   - Clean the tokens by removing stop words, punctuation, and digits, and perform lemmatization.

2. **Feature Extraction:**
   - Apply `TfidfVectorizer` to convert the cleaned sentences into TF-IDF features.
   - Calculate the TF-IDF scores for each feature and sort them to identify the most relevant terms.

3. **Question Generation:**
   - Select a fixed number of high-scoring features (terms) to create questions.
   - For each selected term, find its occurrence in the original sentences and replace it with a blank ("____").
   - Generate multiple-choice options by selecting random terms from the sorted features list, ensuring the correct answer is included among the choices.
   - Shuffle the choices and format them into a dictionary with letter options.

4. **Question Formatting:**
   - Create MCQ objects with the formatted question, choices, and the correct answer.
   - Ensure unique questions by checking for duplicates before adding them to the final list.

The process results in a set of multiple-choice questions that are designed to test comprehension of the key terms and concepts extracted from the input text.


## Features

- Upload a `.txt` file or enter text directly.
- Generate multiple-choice questions from the text.
- Download the generated questions as a PDF or Word document.
- Contact Us page for sending inquiries.
- Feedback page for submitting feedback.
- Flash messages for user feedback on form submissions.

## Project Structure

- **`app.py`** - The main Flask application script.
- **`templates/`** - Directory containing HTML templates:
  - **`base.html`** - Base template with common layout and footer.
  - **`index.html`** - Home page for text input or file upload.
  - **`results.html`** - Results page displaying generated questions.
  - **`contact.html`** - Contact Us page.
  - **`feedback.html`** - Feedback page.
- **`static/`** - Directory for static files:
  - **`style.css`** - CSS file for styling the application.
- **`core/`** - Directory for core functionality:
  - **`text_processing.py`** - Contains functions for processing text.
  - **`pdf_operations.py`** - Contains functions for creating PDFs.
  - **`word_operations.py`** - Contains functions for creating Word documents.
- **`uploads/`** - Directory for storing uploaded files.

## Configuration

- **`UPLOAD_FOLDER:`** Directory for storing uploaded files.
- **`ALLOWED_EXTENSIONS:`** Allowed file extensions for uploads (currently `.txt`).
- **`SECRET_KEY:`** Used for session management and flash messages. Update this to a secure key in a production environment.

## Usage

1. **Navigate to the Home Page**

   You can either enter text directly or upload a `.txt` file.

2. **Submit Text or File**

   - Enter text in the provided textarea or upload a `.txt` file.
   - Click "Submit" to process the input.

3. **View Results**

   - Generated questions will be displayed on the results page.
   - You can download the questions in PDF or Word format using the respective buttons.

4. **Contact Us / Provide Feedback**

   - Use the "Contact Us" and "Feedback" pages to send inquiries or provide feedback.


## Installation

### Prerequisites

- Python 3.x
- Flask
- Required Python libraries

 **Clone the Repository**

   ```bash
   git clone https://github.com/codeasarjun/mcq_genrator.git
   cd <your folder>
```
