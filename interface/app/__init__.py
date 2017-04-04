from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask import flash
import sys
sys.path.append('/Users/Leslie/GitHub/MyWebsite/Weibo')
from sinaweibo import SinaWeibo

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/apps_demo')
def apps_demo():
    return render_template('apps_demo.html')
    # TODO (Leslie) Build apps_demo.html

@app.route('/projects_demo')
def projects_demo():
    return render_template('projects_demo.html')
    # TODO (Leslie) Build projects_demo.html

@app.route('/search', methods=['POST', 'GET'])
def search():
    error = ''
    try:
        if request.method == 'POST':
            username = request.form['username']
            print(username == '')
            if username != '':
                likes_dir = 'plots/weibo_likes_{0}.png'.format(username)
                trend_dir = 'plots/weibo_trend_{0}.png'.format(username)
                record_dir = 'plots/weibo_records_{0}.png'.format(username)
                return render_template('weibo/search_result.html', likes_dir = likes_dir,
                                       trend_dir= trend_dir, record_dir = record_dir)
            else:
                flash('\"Username\" cannot be empty!', category='warning')
                return render_template('weibo/search.html')
        return render_template('weibo/search.html')
    except Exception as e:
        flash(e)
        return render_template('weibo/search.html', error=error)


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run()
