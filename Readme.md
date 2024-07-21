# Wine Business Chatbot

This project implements a wine business chatbot using Flask and SentenceTransformers. The chatbot answers questions based on a given corpus and sample question-answer pairs and handles follow-up questions by maintaining conversation history.

## Installation

1. **Clone the repository**:

    ```sh
    git clone https://github.com/yourusername/Bot.git
    cd wine-business-chatbot
    ```

2. **Create and activate a virtual environment**:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages**:

    ```sh
    pip install flask sentence-transformers
    ```

4. **Ensure you have the necessary files**:

    - `corpus.txt`: Contains the corpus text.
    - `Sample Question Answers.json`: Contains sample questions and answers.

## Running the Application

```sh
python app.py
```