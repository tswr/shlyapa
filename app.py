import random
import json
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)


words = set()
solved = set()

@app.route('/hard_reset')
def hard_reset():
    words = set()
    solved = set()


@app.route('/')
def index():
    load_state()
    return render_template('index.html', len_words=len(words),
            len_solved=len(solved))


@app.route('/adder')
def adder():
    dump_state()
    return render_template('add_word.html')


def dump_state():
    with open('state.txt', 'w') as f:
        print(json.dumps(list(words)), file=f)
        print(json.dumps(list(solved)), file=f)

def load_state():
    global words
    global solved
    try:
        with open('state.txt', 'r') as f:
            words = set(json.loads(f.readline()))
            solved = set(json.loads(f.readline()))
    except Exception as e:
        words = set()
        solved = set()
        print('Can not load state: {}'.format(e))
    print(words)
    print(solved)


@app.route('/reset')
def reset():
    global words
    global solved
    load_state()
    words.update(solved)
    solved = set()
    dump_state()
    return "OK!"


@app.route('/add/<word>')
def add(word):
    load_state()
    if word in words:
        result = "NO!"
    else:
        words.add(word)
        result = "OK!"
    dump_state()
    return result


@app.route('/add2')
def add2():
    load_state()
    word = request.args.get('word')
    print(request.args)
    words.add(word)
    dump_state()
    return redirect(url_for('adder'), code=302)


@app.route('/state')
def state():
    load_state()
    return 'words: %s, solved: %s' % (str(words), str(solved))


@app.route('/get_random')
def get_random():
    load_state()
    if words:
        word = random.choice(list(words))
        return render_template('word.html', word=word)
    else:
        return "No more words"


@app.route('/mark_as_solved/<word>')
def mark_as_solved(word):
    load_state()
    solved.add(word)
    words.remove(word)
    dump_state()
    return redirect(url_for('get_random'), code=302)


if __name__ == "__main__":
    app.run()


