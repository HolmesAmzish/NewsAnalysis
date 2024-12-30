"""
file: plotter.py
Functions of image plot
version: 1.0 2024-12-29
since: 2024-12-29
author: Cacc
"""

from wordcloud import WordCloud
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def plot_hist(word_freq):
    top_words = word_freq.most_common(10)
    words, counts = zip(*top_words)
    plt.figure(figsize=(12, 6))
    plt.bar(words, counts)
    plt.xticks(rotation=45)
    plt.show()

def plot_wordcloud(word_freq):
    wordcloud = WordCloud(
        font_path='simhei.ttf',
        background_color='white',
        width=800,
        height=600,
    ).generate_from_frequencies(word_freq)

    plt.switch_backend('TkAgg')
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()