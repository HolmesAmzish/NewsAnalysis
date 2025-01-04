"""
file: db.py
version: 1.5 2025-01-02
since: 2024-12-29
author: Cacciatore
"""

import sqlite3


def create_table():
    """
    Create a news database while initializing
    :return:
    """
    conn = sqlite3.connect('news_data.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT,
        published_time TEXT,
        url TEXT UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()
    print("Database and table created successfully!")


def save_news_to_db(news_dict):
    """
    Check for duplicate URLs before inserting into the database
    """
    conn = sqlite3.connect('news_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM news WHERE url = ?', (news_dict['url'],))
    exists = cursor.fetchone()[0]

    if exists:
        print(f"Duplicate URL, skipped: {news_dict['title']}")
    else:
        cursor.execute('''
        INSERT INTO news (title, content, published_time, url)
        VALUES (?, ?, ?, ?)
        ''', (
            news_dict['title'],
            news_dict['article_text'],
            news_dict['time'],
            news_dict['url']
        ))
        conn.commit()
        print(f"Saved to DB: {news_dict['title']}")

    conn.close()


def get_all_news(page_id=1):
    """
    Retrieve all news articles from the database with pagination
    :param page_id: Current page number (starts from 1)
    :return: List of news articles for the requested page
    """
    conn = sqlite3.connect('news_data.db')
    cursor = conn.cursor()

    offset = (page_id - 1) * 10

    cursor.execute('''
    SELECT id, title, published_time, url FROM news
    ORDER BY published_time DESC
    LIMIT ? OFFSET ?
    ''', (10, offset))

    news_list = cursor.fetchall()

    conn.close()

    return news_list


def get_news_by_id(article_id):
    """
    Get news by specific article ID
    :param article_id:
    :return:
    """
    conn = sqlite3.connect('news_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM news WHERE id = ?", (article_id,))
    article = cursor.fetchone()
    conn.close()
    return article

def search_news_by_title(keyword, page_id=1):
    """
    Search news by title
    :param keyword: The search keyword
    :param page_id: Current page for pagination
    :return: List of matched news articles
    """
    conn = sqlite3.connect('news_data.db')
    cursor = conn.cursor()

    offset = (page_id - 1) * 10
    keyword = f"%{keyword}%"

    cursor.execute('''
    SELECT id, title, published_time, url FROM news
    WHERE title LIKE ?
    ORDER BY published_time DESC
    LIMIT ? OFFSET ?
    ''', (keyword, 10, offset))

    results = cursor.fetchall()
    conn.close()

    return results
