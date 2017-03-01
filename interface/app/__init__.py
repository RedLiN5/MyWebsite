from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask import flash
import sys
sys.path.append('/Users/Leslie/GitHub/WeiboFans')
from sinaweibo import SinaWeibo

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST', 'GET'])
def search():
    error = ''
    try:
        if request.method == 'POST':
            username = request.form['username']
            print(username)
            return render_template('/weibo/search_user.html')
        return render_template('/weibo/search_user.html')
    except Exception as e:
        flash(e)
        return render_template('/weibo/search_user.html', error=error)




if __name__ == '__main__':
    app.run()
