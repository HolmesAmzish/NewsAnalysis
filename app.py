from flask import Flask, render_template, redirect, url_for, session, request, jsonify, abort
import db
from news_getter import get_news_content_from_url

app = Flask(__name__)

app.secret_key = 'hhzs666'


@app.route('/')
def index():
    if "logged_in" not in session:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('dashboard'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login page
    :return:
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == '123':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@app.route('/dashboard')
@app.route('/dashboard/<int:page_id>')
def dashboard(page_id=1):
    """
    Dashboard page
    """
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    # Ensure the page_id is valid and not less than 1
    if page_id < 1:
        page_id = 1

    # Fetch articles with pagination
    articles = db.get_all_news(page_id)

    return render_template('dashboard.html', articles=articles, page_id=page_id)


@app.route('/crawl_news', methods=['POST'])
def crawl_news():
    """
    接收 URL 并爬取新闻，将内容保存到数据库
    """
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'success': False, 'message': 'URL is required'})

    try:
        # 调用爬虫函数获取新闻内容
        news_content = get_news_content_from_url(url)

        # 将新闻保存到数据库
        db.save_news_to_db(news_content)

        return jsonify({'success': True, 'message': 'News crawled and saved successfully!'})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': 'Failed to crawl news'})


@app.route('/update_news', methods=['POST'])
def update_news():



@app.route('/article/<int:article_id>')
def article(article_id):
    article_content = db.get_news_by_id(article_id)

    if not article:
        abort(404)

    # 渲染模板，传递文章数据
    return render_template('article.html', article=article_content)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

