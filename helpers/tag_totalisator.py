#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Mustafa ÇELİK"


import sys
import codecs
import nltk
from nltk.tokenize import LineTokenizer
from nltk.tokenize import WhitespaceTokenizer


if len(sys.argv) < 2:
    print('usage:', sys.argv[0], 'corpus[ex: analyzer_result_of_hasim_sak.txt]')
    exit(1)


def main():
    f = codecs.open(sys.argv[1], mode="r", encoding="utf-8")
    raw_data = f.read()

    # Split sentences by removing BS ES Tags in Hasim Sak Analyzer
    sentences = split_bs_es_tags(raw_data)

    word_parsing_list = list()

    for sentence in sentences:

        # Split sentences into lines which are word and its sequence
        words_parse = word_tokenizer(sentence)

        for word_parse in words_parse:

            tokens = tokenize_word_parse(word_parse)
            word_parsing_list.extend(tokens[1:])
    f.close()

    tags = get_tags(word_parsing_list)

    print("number of tag: {0}".format(len(tags)))
    print("number of tag: {0}".format(len(word_parsing_list)))
    # print("number of distinct tag: {0}".format(set(len(tags))))
    fd = nltk.FreqDist(tags)
    print("number of distinct tag: {0}".format(len(fd.keys())))


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
    return tokens

if __name__ == '__main__':
    main()
