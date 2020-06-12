import argparse
import flask
import os

from flask import request, jsonify, json, render_template, redirect, url_for, abort, Response, jsonify
from twitter import get_user_profile, get_following_list, generate_follow_graph

parser = argparse.ArgumentParser()
parser.add_argument('--host',
                    type=str,
                    default='0.0.0.0',
                    help="port of the server.")
parser.add_argument('--port',
                    '-p',
                    type=int,
                    default=3000,
                    help="port of the server.")

app = flask.Flask(__name__, static_folder='static/')
app.config.update(DEBUG=True, SECRET_KEY='collective_intelligence')

@app.route('/heart-beat', methods=['GET'])
def heart_beat():
    return jsonify({'message': 'life is good.'})

@app.route('/', methods=['GET'])
def homepage():
    return render_template('homepage.html')

@app.route('/how-it-works', methods=['GET'])
def how_it_works():
    return render_template('how-it-works.html')

@app.route('/graph/<username>', methods=['GET'])
def graph(username):
    graph = generate_follow_graph(username)
    return jsonify(graph)

@app.route('/recommend', methods=['GET'])
def recommend():
    username = request.args.get('username')
    limit = request.args.get('limit', 20)
    return render_template('recommend.html', username=username, limit=limit)

@app.route('/followings/<username>', methods=['GET'])
def followings(username):
    limit = request.args.get('limit', 20)
    following_list = get_following_list(username, limit=limit)
    response = {
        'username': username,
        'following_list': following_list
    }
    print(response)
    return jsonify(response)

@app.route('/profile/<username>', methods=['GET'])
def profile(username):
    profile = get_user_profile(username)
    return jsonify({
        'profile': profile
    })
    

if __name__ == '__main__':
    args = parser.parse_args()

    extra_dirs = ['templates']
    extra_files = []
    for extra_dir in extra_dirs:
        for dirname, dirs, files in os.walk(extra_dir):
            for filename in files:
                filename = os.path.join(dirname, filename)
                if os.path.isfile(filename):
                    extra_files.append(filename)

    app.run(host=args.host, port=args.port)
