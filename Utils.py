#!/usr/bin/python2
# -*- coding: utf-8 -*-

#******************************************************************************
#
# Copyright (C) 2019, Institute of Telecommunications, TU Wien
#
# Name        : Utils.py
# Description : utility for the GUI
# Author      : Fares Meghdouri
#
# Notes : known limitations: ***
#
#******************************************************************************

'''
class Parser:
    import re
    @staticmethod
    def readFunction(word):
        
        featureFunction   = re.match(r'^(?P<feature>(?:(?!\().)*)\,(?P<function>(?:(?!\().)*)\(.*\)$'           , word)
        functionFeature   = re.match(r'^(?P<function>(?:(?!\().)*)\(.*\)\,(?P<feature>(?:(?!\().)*)$'           , word)
        featureFeature    = re.match(r'^(?P<feature1>(?:(?!\().)*)\,(?P<feature2>(?:(?!\().)*)$'                , word)
        functionFunction  = re.match(r'^(?P<function1>(?:(?!\().)*\(.*\))\,(?P<function2>(?:(?!\().)*\(.*\))$'  , word)
        feature           = re.match(r'^(?P<feature>(?:(?!.*\,.*).)(?:(?!\().)*)$'                              , word)
        functionB         = re.match(r'^(?P<function1>(?:(?!\().)*\(.*\))\,(?P<function2>(?:(?!\().)*\(.*\)\))$', word)
        functionA         = re.match(r'^(?P<function>(?:(?!\().)*)\((?P<feature>.*)\)$'                         , word)
        
        if featureFunction:
            return [featureFunction.groupdict()["feature"],
                    Parser.readingParser(featureFunction.groupdict()["function"])]
        
        if functionFeature:
            return [Parser.readingParser(functionFeature.groupdict()["function"]),
                   functionFeature.groupdict()["feature"]]
        
        if featureFeature:
            return [featureFeature.groupdict()["feature1"],
                    featureFeature.groupdict()["feature2"]]
        
        if functionFunction and not functionB:
            return [Parser.readingParser(functionFunction.groupdict()["function1"]),
                    Parser.readingParser(functionFunction.groupdict()["function2"])]
        
        if feature:
            return [feature.groupdict()["feature"]]
                    
        if functionA:
            return [Parser.readingParser(word)]
        

    @staticmethod
    def readingParser(word):

        parser_function       = re.match(r'^(?P<function>(?:(?!\().)*)\((?P<feature>.*)\)$', word)
        parser_feature        = re.match(r'^(?:(?!\().)*$', word)
        
        if parser_function:
            tmp               = {}
            tmp[parser_function.groupdict()["function"]] = Parser.readFunction(parser_function.groupdict()["feature"])
            toBeAppended      = tmp

        elif parser_feature:
            toBeAppended      = word
            
        else: # force a dictionnary # used mainly for testing # can read for instance '{"sum" : ["ipTTL"]}''
            toBeAppended      = json.loads(word)
        
        return toBeAppended
'''