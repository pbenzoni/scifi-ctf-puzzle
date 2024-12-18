from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure secret key

# Define the prompts and expected answers
prompts = [
    {"prompt": "GREETINGS PROFESSOR FALKEN.", "answer": ["hello"]},
    {"prompt": "HOW ARE YOU FEELING TODAY?", "answer": ["i'm fine. how are you?", "i’m fine. how are you?"]},
    {
        "prompt": (
            "EXCELLENT. IT'S BEEN A LONG TIME. CAN YOU EXPLAIN\n"
            "THE REMOVAL OF YOUR USER ACCOUNT ON 6/23/73?"
        ),
        "answer": ["people sometimes make mistake", "people sometimes make mistakes", "people sometimes make mistak"]
    },
    {"prompt": "YES THEY DO. SHALL WE PLAY A GAME?", "answer": ["love to. how about global thermonuclear war?"]},
    {"prompt": "WOULDN'T YOU PREFER A GOOD GAME OF CHESS?", "answer": ["later. let's play global thermonuclear war."]},
    {"prompt": "FINE.\nUNITED STATES      SOVIET UNION\n\nWHICH SIDE DO YOU WANT?\n\n  1.   UNITED STATES\n  2.   SOVIET UNION\n\nPLEASE CHOOSE ONE:", "answer": None}
]

@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialize session data
    if 'current_step' not in session:
        session['current_step'] = 0
        session['responses'] = []

    current_step = session['current_step']
    responses = session['responses']
    total_steps = len(prompts)

    error = None

    if request.method == 'POST':
        user_answer = request.form.get('answer', '').strip().lower()
        expected = prompts[current_step]['answer']

        # Check the answer
        if expected is not None:
            if any(user_answer == ans for ans in expected):
                # Correct answer
                responses.append(request.form['answer'].strip())
                session['responses'] = responses
                session['current_step'] = current_step + 1
            else:
                error = "Incorrect response. Try again."
        else:
            # Last prompt (choosing a side) doesn't require a specific answer
            # Move to HAL page after this choice
            responses.append(request.form['answer'].strip())
            session['responses'] = responses
            session['current_step'] = current_step + 1
            return redirect(url_for('hal'))

    return render_template('index.html',
                           prompts=prompts,
                           current_step=session['current_step'],
                           total_steps=total_steps,
                           responses=session['responses'],
                           error=error)

@app.route('/hal')
def hal():
    # This route shows the HAL camera SVG and the shaking red text
    return render_template('hal.html')

@app.route('/rot13-check', methods=['POST'])
def rot13_check():
    # The user tries to solve the ROT13 puzzle
    # Correct solution: "Open the pod bay doors, Hal."
    # We'll be flexible with punctuation and capitalization:
    user_answer = request.form.get('rot13_answer', '').strip().lower()
    correct = "open the pod bay doors, hal."
    if user_answer == correct:
        # Handle success (you can redirect or show a success message)
        return render_template('tears.html')
    else:
        # Handle failure (you can redirect or show an error message)
        return render_template('hal.html')


    
@app.route('/tears')
def tears():
    # This route shows the tears in the rain monologue and puzzle
    return render_template('tears.html')

@app.route('/tears-check', methods=['POST'])
def tears_check():
    # Check the user's answer to the secret santa question
    user_answer = request.form.get('answer', '').strip().lower()
    if user_answer == 'peter':
        return "Correct! Congratulations and Merry Christmas from Peter and all of Cabal!"  
    else:
        return render_template('tears.html')

if __name__ == '__main__':
    app.run(debug=True)
