import re
import string

stop_words = []
with open("./stopwords.txt", "r") as file:
    for line in file.readlines():
        stop_words.append(line.replace("\n", ""))


def normalize_text(s):
    s = s.lower()
    # remove punctuation that is not word-internal (e.g., hyphens, apostrophes)
    s = re.sub('\s\W', ' ', s)
    s = re.sub('\W\s', ' ', s)
    s = s.replace(".", "").replace("'s", "").replace("'", "").replace("(", "").replace(")", "").replace("‘", "")
    s = s.replace("’", "").replace("“", "").replace("”", "").replace("\"", "").replace("\n", " ")
    # make sure we didn't introduce any double spaces
    s = re.sub('\s+', ' ', s)
    s = s.strip()
    s = s.translate(str.maketrans('', '', string.punctuation))
    s = ' '.join([word for word in s.split() if word not in stop_words])
    s = s.strip()
    return s
