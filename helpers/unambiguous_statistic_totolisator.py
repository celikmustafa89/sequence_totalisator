#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Mustafa ÇELİK"


import sys
import codecs
import nltk
from nltk.tokenize import LineTokenizer
from nltk.tokenize import WhitespaceTokenizer
import collections
from tabulate import tabulate


if len(sys.argv) < 2:
    print('usage:', sys.argv[0], 'corpus[ex: analyzer_result_of_hasim_sak.txt]')
    exit(1)


def main():
    f = codecs.open(sys.argv[1], mode="r", encoding="utf-8")
    raw_data = f.read()
    f.close()

    # Split sentences by removing BS ES Tags in Hasim Sak Analyzer
    sentences = split_bs_es_tags(raw_data)

    word_parsing_list = list()  # her bir elemanı seklindeki['ve', 've[Conj]'] listelerdir.

    for sentence in sentences:

        # Split sentences into lines which are word and its parses
        word_parses = word_tokenizer(sentence)

        for word_parse in word_parses:

            tokens = tokenize_word_parse(word_parse)
            if tokens is None:
                continue
            else:
                word_parsing_list.append(tokens)

    print("Tüm kelime çözümleri parse edilip listeye[word_parsing_list] alındı...")

    unambiguous_series_list = calculate_unambiguity_statistic(word_parsing_list)
    print("Unambiguity istatislikleri hesaplandi.[peşpeşe gelen unambiguous dizilerin bulunması]")

    unambiguous_series_statistic = dict()
    for serie in unambiguous_series_list:
        if len(serie) in unambiguous_series_statistic:
            unambiguous_series_statistic[len(serie)]["count"] += 1
            if unambiguous_series_statistic[len(serie)]["count"] < 100:
                unambiguous_series_statistic[len(serie)]["parses"].append(serie)
        else:
            unambiguous_series_statistic[len(serie)] = {"count": 1, "parses": [serie]}

    write_unambiguous_series_statistic_to_file("unambiguous_series_statistic.mc", unambiguous_series_statistic)


def write_unambiguous_series_statistic_to_file(filename, unambiguous_series_statistic):
    tabulated_unambiguous_series_statistic = \
        [(lengths,
            statistics["count"],
            statistics["parses"]
          ) for lengths, statistics in unambiguous_series_statistic.items()]

    with open(filename, 'w') as f:
        f.write(tabulate(tabulated_unambiguous_series_statistic,
                         tablefmt="plain",
                         headers=["Series Length",
                                  "Count",
                                  "Parses"]))
    f.close()

    # print(unabiguous_seris_list)

    # tags = get_tags(word_parsing_list)


def calculate_unambiguity_statistic(word_parsing_list):

    unambiguous_series = list()
    unambig_serie = list()

    for word in word_parsing_list:
        if len(word) == 2:  # tek bir parse'i varsa
            unambig_serie.append(word)
        else:
            if len(unambig_serie) >= 2:  # pespese gelen bir dizi varsa
                unambiguous_series.append(unambig_serie)
                unambig_serie = []
            else:
                unambig_serie = []

    return unambiguous_series


def get_tags(word_parsing_list):
    tags = list()
    for word_parse in word_parsing_list:
        root = word_parse.split('[', 1)[0]
        tag = word_parse.split(root, 1)[1]
        tags.append(tag)
        print(tag)

    return tags


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


def tokenize_word_parse(word_parse):
    """Returns the line tokens which is "cezalı cezalı[Adj] ceza[Noun]+[A3sg]+[Pnon]+[Nom]-lH[Adj+With]"

    :param word_parse: cezalı cezalı[Adj] ceza[Noun]+[A3sg]+[Pnon]+[Nom]-lH[Adj+With]
    :return: list of tokens
    """
    # Split word_parse line which is "hafta hafta[Noun]+[A3sg]+[Pnon]+[Nom]  haf[Noun]+[A3sg]+[Pnon]+DA[Loc]"
    tokens = WhitespaceTokenizer().tokenize(word_parse)
    for token in tokens:
        if "[Unknown]" in token or "[unknown]" in token or token[0] == "" or "[Num]" in token:
            return None

    return tokens

if __name__ == '__main__':
    main()
