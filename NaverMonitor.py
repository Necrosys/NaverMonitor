#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
    NaverMonitor 0.1.1 (2013/05/09)
    by Chae Jong Bin
"""

__productname__ = 'NaverMonitor'
__description__ = 'Tool for the Naver monitoring'
__author__ = 'Chae Jong Bin'
__version__ = '0.1.1'
__date__ = '2013/05/09'

import urllib, urlparse, time
import libparser, libutil, config, libhash

import cgi

def getSignatures(fileName):
    msg = ""
    TrIDSig = libutil.getSignaturesFromTrID(fileName)

    if TrIDSig:
        msg += "\n<TrID>\n"
        for match in TrIDSig:
            msg += "<Match>%s</Match>\n" % cgi.escape(match)
        msg += "</TrID>"

    try:
        import pefile

        pe = pefile.PE(fileName)
        PEiDSig = libutil.getSignaturesFromPEiD(pe)

        if PEiDSig:
            msg += "\n<PEiD>\n"
            for match in PEiDSig:
                msg += "<Match>%s</Match>\n" % cgi.escape(str(match[0]))
            msg += "</PEiD>"

        return msg
    except:
        return msg

def getHeaderAnalysis(fileName):
    #pe = pefile.PE(fileName)
    pass

def getArchiveMembers(fileName):
    import patoolib
    
    try:
        patoolib.test_archive(fileName, verbosity=-1)
        print "<ArchiveMembers>"
        patoolib.list_archive(fileName)
        print "</ArchiveMembers>"
    except:
        pass

##    if zipfile.is_zipfile(fileName):
##        print "<ZIP>"
##        zipFile = zipfile.ZipFile(fileName, "r")
##        print "<ArchiveMembers>"
##        for file in zipFile.namelist():
##            print "<Name>%s</Name>" % (cgi.escape(file))
##        print "</ArchiveMembers>"
##        zipFile.close()
##        print "</ZIP>"

def findSampleFromBlog(naverData):
    naverBlogUrl = "http://blog.naver.com"
    naverApiUrl = "http://openapi.naver.com"

    itemList = libparser.MyXMLParser().getItemList(naverData)

    for index in range(0,len(itemList)):
        
        if naverBlogUrl in itemList[index]["bloggerlink"]:
            print "<Blog>"
            # HACK: Sleep some seconds
            time.sleep(0.3)
            realNaverBlogUrl = urllib.urlopen(itemList[index]["link"]).geturl()
            print "<URL>%s</URL>" % (cgi.escape(realNaverBlogUrl))
            
            if naverApiUrl not in realNaverBlogUrl:
                realNaverBlogId = urlparse.urlparse(realNaverBlogUrl).path.replace("/", "")
                print "<ID>%s</ID>" % (cgi.escape(realNaverBlogId))

                print "<Post>"

                realNaverBlogPostId = urlparse.urlparse(realNaverBlogUrl).query.split("=")[-1]
                #print realNaverBlogPostId
                realNaverBlogPostUrl = naverBlogUrl + "/PostView.nhn?blogId=" + realNaverBlogId + "&logNo=" + realNaverBlogPostId
                print "<URL>%s</URL>" % (cgi.escape(realNaverBlogPostUrl))
                realNaverBlogPostData = urllib.urlopen(realNaverBlogPostUrl).readlines()

                for data in realNaverBlogPostData:
                    if "_postAddDate" in data:
                        myHTMLParser = libparser.MyHTMLParserDataOnly()
                        myHTMLParser.feed(data)
                        print "<Date>%s</Date>" % (cgi.escape(myHTMLParser.data))
                        myHTMLParser.close()
                        del myHTMLParser

                    if "encodedAttachFileName" in data and ".reg'" not in data:
                        # SECURITY WARNING: eval
                        aPostFiles = eval("[" + "".join(data).split("= [")[1].split("];")[0] + "]")

                        print "<AttachedFiles>"

                        aPostFileIdx = 0

                        for aPostFile in aPostFiles:
                            print "<File>"
                            print "<Index>%s</Index>" % aPostFileIdx
                            print "<URL>%s</URL>" % (cgi.escape(aPostFile["encodedAttachFileUrl"]))
                            
                            fileName = config.SAMPLE_DIR + realNaverBlogId + "_" + realNaverBlogPostId + "_" + aPostFile["encodedAttachFileUrl"].split("/")[-1] + ".vir"
                            libutil.downloadSample(aPostFile["encodedAttachFileUrl"], fileName)

                            libHash = libhash.LibHash()
                            libHash.generateHashesFromFile(fileName)
                            
                            print "<Hashes>%s</Hashes>" % libHash.generateXml()

                            del libHash
                            
                            print "<Signatures>%s</Signatures>" % getSignatures(fileName)
##                            print "<Analysis>%s</Analysis>" % getHeaderAnalysis(fileName)
                            getArchiveMembers(fileName)
                            print "</File>"
                            
                            aPostFileIdx += 1

                        print "</AttachedFiles>"

                    if "tistory.com" in data and "href=" in data:
                        print "<URL>%s</URL>" % (cgi.escape(realNaverBlogPostUrl))
                        myHTMLParser = libparser.MyHTMLParserAOnly()
                        print "<Link><URL>%s</URL></Link>" % (cgi.escape(myHTMLParser.data))
                        myHTMLParser.close()
                        del myHTMLParser

                print "</Post>"
                
            else:
                
                print "<Note>geturl() failed.</Note>"
                
            print "</Blog>"

def naverBlogSearch(engTag, korQuery):
    searchTarget = "blog"

    print "<%s>" % (cgi.escape(engTag))
    findSampleFromBlog(libutil.naverSearch(searchTarget, korQuery))
    print "</%s>" % (cgi.escape(engTag))

def main(args = None):
    import textwrap, sys

    USAGE=textwrap.dedent("""\
        %s %s (%s)
        by %s

        Usage:
            %s.py --printxml # Print XML output
        """ % (__productname__, __version__, __date__, __author__, __productname__))

    if args is None:
        args = sys.argv[1:]

    if not args or args[0] not in ('--printxml'):
        print USAGE
        sys.exit(1)

    if args[0] == '--printxml':
        querys = {
                'PbBot_FastPing':'"패스트핑"',
                'PbBot_ChaosOne':'"카오스원"',
                'PbBot_wLauncher1':'"원순철"',
                'PbBot_wLauncher2':'"w런처"',
                'PbBot_wLauncher3':'"w런쳐"',
                'PbBot_FishServer1':'"피쉬서버"',
                'PbBot_FishServer2':'"피시서버"',
#                'Etc_CTT':'"클릭투트윅"',
#                'Etc_GoClean':'"고클린"',
#                'Etc_ProcessClean':'"프로세스클린"'
#                'Etc_SuddenHack':'"서든핵"',
#                'Etc_WallHack':'"월핵"',
                'Etc_Mosquito':'"모기잡기"',
                'Etc_HanGame':'"한게임"'
                }

        print '<?xml version="1.0" encoding="UTF-8"?>'
        print "<%s>" % (__productname__)
        print "<Version>%s</Version>" % (__version__)
        print "<Querys>"

        for query in querys.keys():
            naverBlogSearch(query, querys[query])

        print "</Querys>"
        print "</%s>" % (__productname__)

if __name__ == "__main__":
    main()
