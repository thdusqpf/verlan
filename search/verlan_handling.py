from flask import Flask, request, jsonify
# import nltk
from nltk.tokenize import SyllableTokenizer
from unidecode import unidecode

app = Flask(__name__)
vowels = ['a', 'e', 'i', 'o', 'u']

identical_pronunciation = {
    'i': ['i', 'y'],
    'y': ['y', 'u', 'eu'],
    'e': ['e', 'ai', 'eiz'],
    'o': ['o', 'au', 'eau'],
    'u': ['ou', 'aou'],
    'f': ['f', 'ph'],
    'k': ['c', 'cc', 'k', 'que', 'ch'],
    'c': ['q', 'que'],
    's': ['s', 'sc', 'se', 'c', 'x', 'ch'],
    'z': ['z', 's'],
    't': ['tte'],
    'j': ['ge']
}

def remove_accents(text):
    if isinstance(text, str):
        return unidecode(text)
    else:
        return text


def remove_stopword(text):
    ssp = SyllableTokenizer()
    syllables = ssp.tokenize(text)
    first_index = 0
    last_index = len(syllables) - 1

    for i in (first_index, last_index):
        last_alphabet_of_syllable = syllables[i][-1]
        number_of_vowels = sum(syllables[i].count(vowels))

        if number_of_vowels > 1 and last_alphabet_of_syllable == 'u':
            syllables[i] = syllables[i].strip('u')
    return syllables

def switch_syllables(text):
    text.insert(0, text[-1])
    return text[:-1]

def handle_identical_pronounciation(text):
    possible_words = []

    for alphabet in text:
        for key in identical_pronunciation.keys():
            if alphabet == key:
                for value in identical_pronunciation[key]:
                    possible_words.append(alphabet.replace(alphabet, value))
    return possible_words

@app.route('/process_word', methods=['POST'])
def process_word():
    data = request.json
    word = data['word']

    w1 = remove_accents(word)
    w2 = remove_stopword(w1)
    w3 = switch_syllables(w2)
    processed_result = handle_identical_pronounciation(w3)

    # 리스트를 문자열로 변환하여 쉼표로 구분
    processed_result_str = ', '.join(processed_result)

    return jsonify({'result': processed_result_str})


if __name__ == '__main__':
    app.run(debug=True)
