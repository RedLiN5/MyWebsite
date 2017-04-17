from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import flash
import sys
import glob
sys.path.append('/Users/Leslie/GitHub/MyWebsite/Weibo')
from sinaweibo import SinaWeibo

weibo = SinaWeibo()

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

@app.route('/weibo/search', methods=['POST', 'GET'])
def weibo_search():
    error = ''
    try:
        if request.method == 'POST':
            username = request.form['username']
            if username != '':
                filenames = glob.glob('static/plots/*.png')
                if sum(username in f for f in filenames)==3:
                    pass
                else:
                    weibo.initial(bloger=username,
                                  max_page=20)
                    captcha_name = weibo.captcha_name
                    captcha_dir = 'login_captcha/{0}'.format(captcha_name)
                    print(captcha_dir)
                    weibo.first_part()
                    return render_template('weibo/captcha.html',
                                           captcha_name = captcha_dir)
                likes_dir = 'plots/weibo_likes_{0}.png'.format(username)
                trend_dir = 'plots/weibo_trend_{0}.png'.format(username)
                record_dir = 'plots/weibo_records_{0}.png'.format(username)
                return render_template('weibo/search_result.html',
                                       likes_dir=likes_dir,
                                       trend_dir=trend_dir,
                                       record_dir=record_dir)
            else:
                flash('\"Username\" cannot be empty!',
                      category='warning')
                return render_template('weibo/search.html')
        return render_template('weibo/search.html')
    except Exception as e:
        flash(e)
        return render_template('weibo/search.html', error=error)

@app.route('/weibo/captcha', methods=['POST', 'GET'])
def captcha_input():
    error = ''
    try:
        if request.method == 'POST':
            captcha = request.form['captcha']
            weibo.second_part(captcha=captcha)
            username = weibo.nickname
            likes_dir = 'plots/weibo_likes_{0}.png'.format(username)
            trend_dir = 'plots/weibo_trend_{0}.png'.format(username)
            record_dir = 'plots/weibo_records_{0}.png'.format(username)
            return render_template('weibo/search_result.html',
                                   likes_dir=likes_dir,
                                   trend_dir=trend_dir,
                                   record_dir=record_dir)
    except Exception as e:
        flash(e)
        return render_template('weibo/search.html',
                               error=error)
    return render_template('weibo/captcha.html')


@app.route('/douban/search', methods=['POST', 'GET'])
def douban_search():
    error = ''
    try:
        if request.method == 'POST':
            groupid = request.form['groupname']
            keywords = request.form['keywords']
            pagenum = request.form['pagenum']
            if groupid != '' and pagenum != '':
                return render_template('weibo/search_result.html',
                                       groupid=groupid,
                                       keywords=keywords,
                                       pagenum=pagenum)
            else:
                flash('\"Group Name\" or \"Page Num\" may be empty!',
                      category='warning')
                return render_template('douban/search.html')
        return render_template('douban/search.html')

    except Exception as e:
        flash(e)
        return render_template('douban/search.html', error=error)


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run()
