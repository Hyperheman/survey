import json
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Load existing data from the provided JSON or initialize new data
with open('ctn.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

survey_question = data.get('question', """कंडीशनल बेल होने के बाद प्रतिवादी को सुरक्षा व्यवस्था के तहत अंडरग्राउंड हो जाना बिना निगरानी के क्या यह उचित है या अनुचित?""")

html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Survey</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            background: linear-gradient(to bottom, #000000, #080808);
            color: white;
        }
        
        .container {
            text-align: center;
            padding: 50px;
        }
        
        .gradient-button {
            background: #000;
            border: 2px solid #FF0000;
            color: #FF0000;
            padding: 10px 20px;
            font-size: 18px;
            cursor: pointer;
            margin-right: 10px;
        }
        
        .gradient-button:hover {
            background: #FF0000;
            color: #000;
        }
        
        .response-input {
            border: 2px solid #00FF00;
            padding: 10px;
            font-size: 16px;
            width: 200px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Survey</h1>
        <form method="post">
            <label for="name">Your Name:</label><br>
            <input type="text" id="name" name="name" required class="response-input">
            <br><br>
            <p>{{ question }}</p>
            <button class="gradient-button" type="submit" name="response" value="yes">Yes</button>
            <button class="gradient-button" type="submit" name="response" value="no">No</button>
        </form>
    </div>
</body>
</html>
"""


@app.route('/', methods=['GET', 'POST'])
def survey():
    global data

    if request.method == 'POST':
        name = request.form['name']
        response = request.form['response']
        data[response]['count'] += 1
        data[response]['names'].append(name)

        # Save data to JSON file
        with open('ctn.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        return 'Thank you for completing the survey!'

    return render_template_string(html_template, question=survey_question)


@app.route("/42146173251e3cc2c96823bc525b41fe")
def show_yes_responses():
    global data
    return f"Total 'Yes' responses: {data['yes']['count']}, Names: {', '.join(data['yes']['names'])}"


@app.route("/42146173251e3cc2c96823bc525b41fr")
def show_no_responses():
    global data
    return f"Total 'No' responses: {data['no']['count']}, Names: {', '.join(data['no']['names'])}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
