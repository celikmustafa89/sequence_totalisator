#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import nltk
import codecs
from nltk.tokenize import LineTokenizer
from nltk.tokenize import WhitespaceTokenizer

if len(sys.argv) < 2:
    print 'usage:', sys.argv[0], 'corpus[ex: ambiguation_result_set.txt]'
    exit(1)


def count_sequence():
    file = codecs.open(sys.argv[1], mode="rb", encoding="U8")
    # file = open(sys.argv[1], 'rb')
    raw = file.read()

    sentences = split_bs_es_tags(raw)   # Split sentences by removing BS ES Tags in HasimSak Analyzer

    for sentence in sentences:
        print sentence
        lines = line_tokenizer(sentence)    # Split sentences into lines which are word and its sequence
        for line in lines:
            tokens = WhitespaceTokenizer().tokenize(line)   # Split word word_sequence into tokens using whitespaces
            print tokens
    file.close()


def line_tokenizer(text):
    """ split the sentence into lines.

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


def split_sentences(text):
    """Divides text into sentences. Return list of sentences.

    :param text:
    :return: list of sentences
    """
    from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
    punkt_param = PunktParameters()
    # TODO: buraya türkçe kısaltmalar eklenebilir. Cuneyd hocanın dediği dr. tarzı kısaltmalar
    punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs', 'prof', 'inc'])
    sentence_splitter = PunktSentenceTokenizer(punkt_param)
    sentences = sentence_splitter.tokenize(text)

    return sentences

count_sequence()
