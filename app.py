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

        notes = request.form.get("notes","")

        if "image" in request.files:
            file = request.files["image"]

            if file.filename != "":
                img = Image.open(file).convert("L")

                img = img.resize((img.width*2, img.height*2))

                img = np.array(img)
                img = (img > 150) * 255
                img = Image.fromarray(img.astype('uint8'))

                extracted_text = pytesseract.image_to_string(img, lang="eng")

                extracted_text = extracted_text.replace("\n\n", "\n")

                print(extracted_text)

                notes = notes + "\n" + extracted_text

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
    app.run(debug=True)