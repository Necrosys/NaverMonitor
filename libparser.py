#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
    libparser
    by Chae Jong Bin
"""

__description__ = 'libparser'
__author__ = 'Chae Jong Bin'

import xml.dom.minidom
from HTMLParser import HTMLParser

# Class for XML Parsing
class MyXMLParser():
    def getText(self, nodelist):
        rc = ""

        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data

        return rc

    def getItem(self, nodelist):
        items = {}

        for node in nodelist:
            items[node.tagName] = self.getText(node.childNodes)

        return items

    def getItemList(self, data):
        try:
            items = xml.dom.minidom.parseString(data).getElementsByTagName("channel")[0].getElementsByTagName("item")
        except:
            items = {}
        itemlist = {}

        for i, item in enumerate(items):
            itemlist[i] = self.getItem(item.childNodes)

        return itemlist

# Classes for HTML Parsing
class MyHTMLParserAOnly(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = ""
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                if attr[0] == "href":
                    self.data = attr[1]

class MyHTMLParserDataOnly(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = ""
    def handle_data(self, data):
        if data.strip():
            self.data = data
#    def handle_endtag(self, tag):
#        if tag == "a":
#            print "End tag  :", tag
#    def handle_comment(self, data):
#        print "Comment  :", data
#    def handle_entityref(self, name):
#        print "Named ent:", name
#    def handle_charref(self, name):
#        print "Num ent  :", name
#    def handle_decl(self, data):
#        print "Decl     :", data
