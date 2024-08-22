from boggle import Boggle
from flask import Flask, request, render_template, jsonify, session

app = Flask(__name__)
app.config["SECRET_KEY"] = 'secret'

boggle_game = Boggle()

@app.route('/')
def home():
    """Show board."""

    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get('highscore', 0)
    nplays = session.get('nplays', 0)

    return render_template('index.html', 
                           board=board, 
                           highscore=highscore, 
                           nplays=nplays)

@app.route('/check-word')
def check_word():
    """Check if word is in dictionary."""

    word = request.args['word']
    board = session['board']
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})

@app.route('/post-score', methods=['POST'])
def post_score():
    """Receives score, updates nplays and updates highscore if appropriate."""

    score = request.json['score']
    highscore = session.get('highscore', 0)
    nplays = session.get('nplays', 0)

    session['highscore'] = max(score, highscore)
    session['nplays'] = nplays + 1

    return jsonify(brokenRecord=score > highscore)
