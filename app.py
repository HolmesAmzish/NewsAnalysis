"""
file: app.py
Main flask program for project
version: 1.5 2025-01-02
since: 2024-12-28
author: Cacc
"""

from flask import Flask, render_template, redirect, url_for, session, request, jsonify, abort
import db
import news_getter
import base64
import analyzer

app = Flask(__name__)

app.secret_key = '0123'


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


@app.route('/dashboard', methods=['GET'])
@app.route('/dashboard/<int:page_id>', methods=['GET'])
def dashboard(page_id=1):
    """
    Dashboard page
    :param page_id:
    :return:
    """
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    query = request.args.get('query')
    if query:
        articles = db.search_news_by_title(query, page_id)
    else:
        articles = db.get_all_news(page_id)

    return render_template('dashboard.html', articles=articles, page_id=page_id, query=query)


@app.route('/search', methods=['GET'])
def search():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    query = request.args.get('query')
    page_id = request.args.get('page_id', 1, type=int)
    articles = db.search_news_by_title(query, page_id)

    return render_template('dashboard.html', articles=articles, page_id=page_id, query=query)


@app.route('/crawl_news', methods=['POST'])
def crawl_news():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'success': False, 'message': 'URL is required'})

    try:
        news_content = news_getter.get_news_content_from_url(url)
        db.save_news_to_db(news_content)
        return jsonify({'success': True, 'message': 'News crawled and saved successfully!'})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': 'Failed to crawl news'})


@app.route('/update_news', methods=['POST'])
def update_news():
    """
    Update news articles by crawling and saving to the database.
    Dynamically provide status updates to the frontend.
    """
    try:
        news_links = news_getter.get_links()
        if not news_links:
            return jsonify({'success': False, 'message': 'No new links found'})

        status_list = []
        for link in news_links:
            try:
                # Get news content
                news_content = news_getter.get_news_content_from_url(link)

                # Save news to the database
                saved = db.save_news_to_db(news_content)
                status_list.append({'url': link, 'status': 'Completed'})
            except Exception as e:
                status_list.append({'url': link, 'status': f'Failed: {str(e)}'})

        return jsonify({'success': True, 'status_list': status_list})

    except Exception as e:
        print(f"Error in update_news: {e}")
        return jsonify({'success': False, 'message': 'Failed to update news'})


@app.route('/article/<int:article_id>')
def article(article_id):
    article_content = db.get_news_by_id(article_id)

    if not article:
        abort(404)

    return render_template('article.html', article=article_content)


@app.route('/analysis/<int:article_id>')
def analysis(article_id):
    article = db.get_news_by_id(article_id)
    if not article:
        abort(404)

    article_summary = analyzer.summarize_article(article[2])

    word_freq = analyzer.get_word_freq(article[2])
    img_hist = analyzer.plot_hist(word_freq)
    img_wordcloud = analyzer.plot_wordcloud(word_freq)

    if not img_hist or not img_wordcloud:
        abort(500, description="Failed to generate image")

    img_hist_base64 = base64.b64encode(img_hist).decode('utf-8')
    img_wordcloud_base64 = base64.b64encode(img_wordcloud).decode('utf-8')

    return render_template(
        'article-analysis.html',
        img_hist_data=img_hist_base64,
        img_wordcloud_data=img_wordcloud_base64,
        article_summary=article_summary,
        article_id=article[0],
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

