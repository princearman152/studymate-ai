import pytesseract
from PIL import Image
from flask import Flask, render_template, request
from groq import Groq
import os
import numpy as np
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = Flask(__name__)

# Add your Groq API key here
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def index():

    result = ""

    if request.method == "POST":

        notes = request.form.get("notes", "")

if "image" in request.files:
    file = request.files["image"]

    if file.filename != "":
        print("Image uploaded but OCR disabled on server")
         

        prompt = f"""
You are an AI study assistant.

Give output in this format:

Summary:
(short explanation)

Key Points:
- point 1
- point 2
- point 3
- point 4
- point 5

Quiz Questions:
1. Question
A)
B)
C)
D)
Answer:

Notes:
{notes}
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content

    return render_template("index.html", result=result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)