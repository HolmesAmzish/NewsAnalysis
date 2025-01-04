"""
file: analyzer.py
Functions of image plot
version: 1.0 2024-12-29
since: 2024-12-29
author: Cacc
"""
import jieba
from collections import Counter
import ollama
from wordcloud import WordCloud
import io
import re
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def get_word_freq(content):
    """
    Get word frequency from news
    :param content
    :return:
    """
    content = re.sub(r'[^\w\s]', '', content)
    words = jieba.cut(content, cut_all=True)
    word_list = [word for word in words if len(word) > 1]
    word_freq = Counter(word_list)
    return word_freq


def plot_hist(word_freq):
    top_words = word_freq.most_common(10)
    words, counts = zip(*top_words)
    plt.figure(figsize=(8, 6))
    plt.bar(words, counts)
    plt.xticks(rotation=45)

    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    plt.close()

    img_bytes.seek(0)
    return img_bytes.getvalue()


def plot_wordcloud(word_freq):
    word_dict = dict(word_freq)
    wordcloud = WordCloud(
        width=800, height=600,
        background_color='white',
        font_path='C:/Windows/Fonts/simhei.ttf'
    ).generate_from_frequencies(word_dict)

    plt.figure(figsize=(10, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')

    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    plt.close()

    img_bytes.seek(0)
    return img_bytes.getvalue()


def summarize_article(article_content):
    try:
        response = ollama.chat(model="qwen2.5:0.5b", messages=[{"role": "user", "content": article_content}])

        if 'message' in response and 'content' in response['message']:
            summary = response['message']['content']
            return summary
        else:
            return "Error: No summary found in the response"

    except Exception as e:
        return f"Error: {str(e)}"
