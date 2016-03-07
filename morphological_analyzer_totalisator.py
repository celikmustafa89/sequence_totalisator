#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Mustafa ÇELİK"

import sys
import nltk
import codecs
from nltk.tokenize import LineTokenizer
from nltk.tokenize import WhitespaceTokenizer
import collections
from tabulate import tabulate
import csv
import operator

if len(sys.argv) < 2:
    print('usage:', sys.argv[0], 'corpus[ex: analyzer_result_of_hasim_sak.txt]')
    exit(1)


def count_seq(tokens):
    for index in range(len(tokens)):
        if index == 0:
            word_dictionary[tokens[index]] = {'word': tokens[index]}
        elif index % 3 == 1:
            sequence_root = get_sequence_root(tokens[index])
            sequence = get_sequence(tokens[index], sequence_root)
            if sequence in sequence_dictionary:
                sequence_dictionary[sequence]['count'] += 1
                # TODO: buraya farklı kök olma durumu için eğer bu kök yoksa ekle seçeneği konulmalıdır.
            else:
                sequence_dictionary[sequence] = {'root': [sequence_root], 'count': 1}
        else:
            continue


def get_sequence(token, root):
    sequence = token.split(root, 1)[1]
    return sequence


def get_sequence_root(token):
    root = token.split('[', 1)[0]
    return root


def main():
    f = codecs.open(sys.argv[1], mode="r", encoding="utf-8")
    raw_data = f.read()

    # Split sentences by removing BS ES Tags in Hasim Sak Analyzer
    sentences = split_bs_es_tags(raw_data)

    for sentence in sentences:

        # Split sentences into lines which are word and its sequence
        words_parse = word_tokenizer(sentence)

        for word_parse in words_parse:
            count_parse_number(word_parse)
            # word_dictionary['word'] = pure_word
            # word_dictionary['#sequence'] = (len(tokens)-1) / 3
            # word_dictionary['whole_sequences'] =
            # count_seq(tokens)
    f.close()
    sorted_parsing_statistic = sort_parsing_statistic_by_key()
    sorted_parsing_statistic = calculate_statistics(sorted_parsing_statistic)
    write_parsing_statistic_to_file("sorted_parsing_statistic.mc", sorted_parsing_statistic)


def calculate_statistics(sorted_parsing_statistic):
    total = 0

    # finds the total parsing
    for key in sorted_parsing_statistic:
        total += sorted_parsing_statistic[key]["total"]

    for key in sorted_parsing_statistic:
        sorted_parsing_statistic[key]["ratio"] = float(sorted_parsing_statistic[key]["total"]/total)
        sorted_parsing_statistic[key]["random_guess_accuracy"] = \
            float(sorted_parsing_statistic[key]["ratio"]*sorted_parsing_statistic[key]["random_guess"])
    return sorted_parsing_statistic


def sort_parsing_statistic_by_key():
    """Sorts parsing_statistic by key.

    :return: sorted_parsing_statistic dictionary
    """
    sorted_parsing_statistic = collections.OrderedDict(sorted(parsing_statistic.items()))
    return sorted_parsing_statistic


def write_parsing_statistic_to_file(filename, parsing_dictionary):
    """Writes parsing_statistic into the given filename.

    :param filename: filename of the output.
    :param parsing_dictionary: dictionary to be written.
    :return: None
    """

    # TODO: words list can be added to tabulate form, but causes problem in file.
    tabulated_parsing_dictionary = \
        [(parse_number,
          statistics["total"],
          statistics["ratio"],
          statistics["random_guess"],
          statistics["random_guess_accuracy"]) for parse_number, statistics in parsing_dictionary.items()]

    with open(filename, 'w') as f:
        f.write(tabulate(tabulated_parsing_dictionary,
                         tablefmt="plain",
                         headers=["Parse_Number",
                                  "Total",
                                  "Ratio",
                                  "Random_Guess",
                                  "Random_Guess_Accuracy"]))
    f.close()


def read_list_from_file(filename):
    """Reads dictionary of elements from the given filename.

    :param filename: filename of the input.
    :return: dictionary of the given file which is parsing_statistic
    """

    # TODO: write_parsing_statistic_to_file methoduna gore okuma islemi yapilacak.
    # with open(filename, 'r') as f:
    #     lines = [line.rstrip(' ') for line in f]
    #
    #     readed_parsing_statistic = dict()
    #     readed_parsing_statistic[key] = [count, [wordlist]]
    return None


def word_tokenizer(text):
    """Split the sentence into lines.

    <S> <S>+BSTag
    2007-5-2Dişlerimiz 2007-5-2Dişlerimiz[Unknown]
    Arasındaki ara[Adj]-[Noun]+[A3sg]+SH[P3sg]+NDA[Loc]-ki[Adj+Rel] : 22.3828125 Aras[Noun]+[Prop]+[A3sg]+
        SH[P3sg]+NDA[Loc]-ki[Adj+Rel] : 19.3212890625 Aras[Noun]+[Prop]+[A3sg]+Hn[P2sg]+
        NDA[Loc]-ki[Adj+Rel] : 23.994140625 ara[Noun]+[A3sg]+SH[P3sg]+NDA[Loc]-ki[Adj+Rel] : 11.2919921875
    Ceset ceset[Noun]+[A3sg]+[Pnon]+[Nom] : 10.6982421875
    </S> </S>+ESTag

    :param text: sentence
    :return: list of lines
    """
    lines = LineTokenizer(blanklines='discard').tokenize(text)
    return lines


def count_parse_number(word_parse):
    """Bir kelimenin olasi tum parse(cozum) sayisi belirlenmektedir.

     1 cozumu varsa 1 cozumlu kisim guncellenir ve kelime eklenir. Or:

     {'1': [count, [word list]], '2': [count, [word list]], .....} bu sekilde olan dictionary guncellenir.
     Bu dictionary'nin key kisminda toplam cozumleme sayisi tutulur.
     Mesela "ve" kelimesinin bir cozumlemesi varsa, {'1': [count=1, [ile]]} dictionary elemani guncellenir.
     count sayisi bir arttirilir ve listeye "ve" kelimesi eklenir.
     Son hali su sekilde olur: {'1': [count=2, [ile, ve]]}

    :param word_parse: Bir cumledeki herhangi bir kelimenin olasi tum cozumlerinin oldugu satir.
    :return: None,  parsing_statistic global degiskeni guncellenir.
    """

    # Split word_parse line which is "hafta hafta[Noun]+[A3sg]+[Pnon]+[Nom]  haf[Noun]+[A3sg]+[Pnon]+DA[Loc]"
    tokens = WhitespaceTokenizer().tokenize(word_parse)

    # Gets pure word which is "hafta"
    pure_word = tokens[0]

    # Gets the # of total parsing
    number_of_parse = len(tokens) - 1
    if number_of_parse == 0:
        number_of_parse = 1

    if str(number_of_parse) in parsing_statistic:
        parsing_statistic[str(number_of_parse)]["total"] += 1  # increases the total count
        # ratio will will be added after all the word statistic is collected.
        # random_guess is already added.
        # random_guess_accuracy will be added after all the word statistic is collected.
        parsing_statistic[str(number_of_parse)]["words"].append(pure_word)  # append pure word to list
    else:
        parsing_statistic[str(number_of_parse)] = {"total": 1,
                                                   "ratio": 0,
                                                   "random_guess": float(1 / number_of_parse),
                                                   "random_guess_accuracy": 0,
                                                   "words": [pure_word]}


def split_bs_es_tags(text):
    """ Removes the BS and ES Tag of hasim sak analyzer.

    :param text: list of sentences
    :return: list of sentences
    """

    def remove_es_tags(sentence):
        """

        :param sentence: string
        :return: sentence without es_tag
        """
        return sentence.replace("</S> </S>+ESTag", "")

    from nltk.tokenize import RegexpTokenizer

    bs_tokenizer = RegexpTokenizer('<S> <S>\+BSTag', gaps=True)
    sentences = bs_tokenizer.tokenize(text)

    for index in range(len(sentences)):
        sentences[index] = remove_es_tags(sentences[index])

    return sentences


#    sort_sequence()
#     print_sequence_dictionary()
#
#
# def print_sequence_dictionary():
#     #with open("sequence_dictionary.txt", "a") as myfile:
#     w = csv.writer(open("output.csv", "w"))
#     for key, val in sequence_dictionary.items():
#         w.writerow(, val.encode('utf-8')])
# def sort_sequence():
#     sorted_dic = sorted(sequence_dictionary.items(), key=operator.itemgetter(1))
#     print sorted_dic



# def remove_word(text, string_to_remove):
#     """ Removes the given string_to_remove from the original text.
#
#     :param text: the original text
#     :param string_to_remove: the string that will be removed from the original text
#     :return: text
#     """
#     return text.replace(string_to_remove, "")


# def split_sentences(text):
#     """Divides text into sentences. Return list of sentences.
#
#     :param text:
#     :return: list of sentences
#     """
#     from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
#     punkt_param = PunktParameters()
#     # TODO: buraya türkçe kısaltmalar eklenebilir. Cuneyd hocanın dediği dr. tarzı kısaltmalar
#     punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs', 'prof', 'inc'])
#     sentence_splitter = PunktSentenceTokenizer(punkt_param)
#     sentences = sentence_splitter.tokenize(text)
#
#     return sentences


if __name__ == '__main__':
    parsing_statistic = dict()
    word_dictionary = dict()
    sequence_dictionary = dict()
    main()
