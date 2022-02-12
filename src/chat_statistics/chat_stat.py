import json
import re
from pathlib import Path
from typing import Union

import arabic_reshaper
from bidi.algorithm import get_display
from hazm import Normalizer, word_tokenize
from loguru import logger
from src.data import Data_dir
from wordcloud import WordCloud


class ChatStatistics:
    """
    Generate chat statistics from a Telegram json file chat
    """
    # load stopwords
    normalizer = Normalizer()
    stop_words = open(Data_dir / 'stopwords.txt').readlines()
    stop_words = list(map(str.strip, stop_words))
    stop_words = list(map(normalizer.normalize, stop_words))

    def __init__(self, chat_json: Union[str, Path]):
        logger.info(f'loading chat data from {chat_json}')
        with open(chat_json) as f:
            # load data
            self.chat_data = json.load(f)

    def removeWeirdChars(self, text):
        weirdPatterns = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   u"\U0001f926-\U0001f937"
                                   u'\U00010000-\U0010ffff'
                                   u"\u200d"
                                   u"\u2640-\u2642"
                                   u"\u2600-\u2B55"
                                   u"\u23cf"
                                   u"\u23e9"
                                   u"\u231a"
                                   u"\u3030"
                                   u"\ufe0f"
                                   u"\u2069"
                                   u"\u2066"
                                   u"\u200c"
                                   u"\u2068"
                                   u"\u2067"
                                   "]+", flags=re.UNICODE)
        return weirdPatterns.sub(r'', text)

    def generate_word_cloud(self, outputdir: Union[str, Path]):
        logger.info('digging data')
        chat_content = ''
        # dig in to text data
        for msg in self.chat_data['messages']:
            # check if the text is str and is persian char
            if isinstance(msg['text'], str) and not re.match(r'[A-Za-z]+', msg['text'], re.I):
                tokens = list(
                    filter(lambda item: item not in ChatStatistics.stop_words, word_tokenize(msg['text'])))
                chat_content += f" {' '.join(tokens)}"
            else:
                continue

        # normalize, reshape for final persian word cloud
        chat_content = self.normalizer.normalize(chat_content)
        chat_content = arabic_reshaper.reshape(
            self.removeWeirdChars(chat_content))
        chat_content = get_display(chat_content)

        logger.info('generating word cloud')
        wordcloud = WordCloud(
            width=600,
            height=400,
            font_path=str(Data_dir / 'Font/NotoNaskhArabic-Regular.ttf'),
            background_color='white',
            max_font_size=130
        ).generate(chat_content)

        logger.info(f'saving word cloud to {outputdir}')
        # Export to an image
        wordcloud.to_file(str(Path(outputdir) / "World_Cloud.png"))


if __name__ == "__main__":
    # add your taraget json file in the string
    chat_stasts = ChatStatistics(chat_json=Data_dir / 'key+ajnabi.json')
    chat_stasts.generate_word_cloud(Data_dir)

    logger.info('Done!')

