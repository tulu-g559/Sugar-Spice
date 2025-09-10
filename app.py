from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    user_input = data.get("input", "")
    mode = data.get("mode", "roast")  # roast or compliment

    prompt = ""
    if mode == "roast":
        prompt = f"""
                You are a witty friend. Write one short, funny roast about this person. 
                Keep it playful, light, and human — like a joke you'd make in conversation. 
                Do not explain your reasoning, give options, or add extra notes. 
                Person: {user_input}
                use emojis in the output.

"""
    elif mode == "compliment":
        prompt = f"""
                You are a kind and funny friend. Write one short, wholesome compliment about this person. 
                Make it natural, warm, and slightly witty — like something you'd actually say to make them smile. 
                Do not explain your reasoning or give options. 
                Person: {user_input}
                use emojis in the output

        """

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)

    return jsonify({"output": response.text})

if __name__ == "__main__":
    app.run(debug=True)
