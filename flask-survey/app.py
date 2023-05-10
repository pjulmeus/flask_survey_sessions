from flask import Flask, render_template, redirect, request, session
from surveys import Survey, Question, satisfaction_survey 

app = Flask(__name__)
from flask_debugtoolbar import DebugToolbarExtension
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)

question_list = []
choices_list = []
for question in satisfaction_survey.questions:
    question_list.append(question.question)

for question in satisfaction_survey.questions:
    choices_list.append(question.choices)

@app.route('/')
def homepage():
    session["RESPONSES"] = []
    return render_template("start_survey.html", survey_title = satisfaction_survey.title, 
                           survey_instruction = satisfaction_survey.instructions)

@app.route('/questions/<int:id>')
def questions(id):
    return render_template("questions.html", survey_questions = question_list[len(session["RESPONSES"])], 
                           survey_choices = choices_list[len(session["RESPONSES"])])

@app.route('/answer' , methods=["POST"])
def answer_post():
    mark = session["RESPONSES"]
    choice = request.form.get('choice')
    mark.append(choice)
    session["RESPONSES"] = mark
    
    if len(session["RESPONSES"]) == len(question_list):
        return redirect("/final")
    else: 
        return redirect(f'/questions/{len(session["RESPONSES"])}')
    
@app.route('/final')
def final_post():
    response = session["RESPONSES"]
    return render_template("final.html", resp = response)