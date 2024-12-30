import jieba
from collections import Counter
from wordcloud import WordCloud


def get_word_freq(news):
    """
    Get word frequency from news
    :param news: dict of news
    :return:
    """
    words = jieba.cut(news['article_text'], cut_all=True)
    word_list = [word for word in words if len(word) > 1]
    word_freq = Counter(word_list)
    return word_freq
