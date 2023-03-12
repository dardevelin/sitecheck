--- BeautifulSoup.py	(original)
+++ BeautifulSoup.py	(refactored)
@@ -76,7 +76,7 @@
 SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE, DAMMIT.
 
 """
-from __future__ import generators
+
 
 __author__ = "Leonard Richardson (leonardr@segfault.org)"
 __version__ = "3.1.0.1"
@@ -84,12 +84,12 @@
 __license__ = "New-style BSD"
 
 import codecs
-import markupbase
+import _markupbase
 import types
 import re
-from HTMLParser import HTMLParser, HTMLParseError
+from html.parser import HTMLParser, HTMLParseError
 try:
-    from htmlentitydefs import name2codepoint
+    from html.entities import name2codepoint
 except ImportError:
     name2codepoint = {}
 try:
@@ -98,18 +98,18 @@
     from sets import Set as set
 
 #These hacks make Beautiful Soup able to parse XML with namespaces
-markupbase._declname_match = re.compile(r'[a-zA-Z][-_.:a-zA-Z0-9]*\s*').match
+_markupbase._declname_match = re.compile(r'[a-zA-Z][-_.:a-zA-Z0-9]*\s*').match
 
 DEFAULT_OUTPUT_ENCODING = "utf-8"
 
 # First, the classes that represent markup elements.
 
-def sob(unicode, encoding):
+def sob(str, encoding):
     """Returns either the given Unicode string or its encoding."""
     if encoding is None:
-        return unicode
+        return str
     else:
-        return unicode.encode(encoding)
+        return str.encode(encoding)
 
 class PageElement:
     """Contains the navigational information for some part of the page
@@ -153,7 +153,7 @@
         #this element (and any children) hadn't been parsed. Connect
         #the two.
         lastChild = self._lastRecursiveChild()
-        nextElement = lastChild.next
+        nextElement = lastChild.__next__
 
         if self.previous:
             self.previous.next = nextElement
@@ -178,8 +178,8 @@
         return lastChild
 
     def insert(self, position, newChild):
-        if (isinstance(newChild, basestring)
-            or isinstance(newChild, unicode)) \
+        if (isinstance(newChild, str)
+            or isinstance(newChild, str)) \
             and not isinstance(newChild, NavigableString):
             newChild = NavigableString(newChild)
 
@@ -233,7 +233,7 @@
                 newChild.nextSibling.previousSibling = newChild
             newChildsLastElement.next = nextChild
 
-        if newChildsLastElement.next:
+        if newChildsLastElement.__next__:
             newChildsLastElement.next.previous = newChildsLastElement
         self.contents.insert(position, newChild)
 
@@ -334,7 +334,7 @@
         g = generator()
         while True:
             try:
-                i = g.next()
+                i = next(g)
             except StopIteration:
                 break
             if i:
@@ -350,7 +350,7 @@
     def nextGenerator(self):
         i = self
         while i:
-            i = i.next
+            i = i.__next__
             yield i
 
     def nextSiblingGenerator(self):
@@ -385,22 +385,22 @@
     def toEncoding(self, s, encoding=None):
         """Encodes an object to a string in some encoding, or to Unicode.
         ."""
-        if isinstance(s, unicode):
+        if isinstance(s, str):
             if encoding:
                 s = s.encode(encoding)
         elif isinstance(s, str):
             if encoding:
                 s = s.encode(encoding)
             else:
-                s = unicode(s)
+                s = str(s)
         else:
             if encoding:
                 s  = self.toEncoding(str(s), encoding)
             else:
-                s = unicode(s)
+                s = str(s)
         return s
 
-class NavigableString(unicode, PageElement):
+class NavigableString(str, PageElement):
 
     def __new__(cls, value):
         """Create a new NavigableString.
@@ -410,12 +410,12 @@
         passed in to the superclass's __new__ or the superclass won't know
         how to handle non-ASCII characters.
         """
-        if isinstance(value, unicode):
-            return unicode.__new__(cls, value)
-        return unicode.__new__(cls, value, DEFAULT_OUTPUT_ENCODING)
+        if isinstance(value, str):
+            return str.__new__(cls, value)
+        return str.__new__(cls, value, DEFAULT_OUTPUT_ENCODING)
 
     def __getnewargs__(self):
-        return (unicode(self),)
+        return (str(self),)
 
     def __getattr__(self, attr):
         """text.string gives you text. This is for backwards
@@ -424,7 +424,7 @@
         if attr == 'string':
             return self
         else:
-            raise AttributeError, "'%s' object has no attribute '%s'" % (self.__class__.__name__, attr)
+            raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, attr))
 
     def encode(self, encoding=DEFAULT_OUTPUT_ENCODING):
         return self.decode().encode(encoding)
@@ -435,23 +435,23 @@
 class CData(NavigableString):
 
     def decodeGivenEventualEncoding(self, eventualEncoding):
-        return u'<![CDATA[' + self + u']]>'
+        return '<![CDATA[' + self + ']]>'
 
 class ProcessingInstruction(NavigableString):
 
     def decodeGivenEventualEncoding(self, eventualEncoding):
         output = self
-        if u'%SOUP-ENCODING%' in output:
+        if '%SOUP-ENCODING%' in output:
             output = self.substituteEncoding(output, eventualEncoding)
-        return u'<?' + output + u'?>'
+        return '<?' + output + '?>'
 
 class Comment(NavigableString):
     def decodeGivenEventualEncoding(self, eventualEncoding):
-        return u'<!--' + self + u'-->'
+        return '<!--' + self + '-->'
 
 class Declaration(NavigableString):
     def decodeGivenEventualEncoding(self, eventualEncoding):
-        return u'<!' + self + u'>'
+        return '<!' + self + '>'
 
 class Tag(PageElement):
 
@@ -460,7 +460,7 @@
     def _invert(h):
         "Cheap function to invert a hash."
         i = {}
-        for k,v in h.items():
+        for k,v in list(h.items()):
             i[v] = k
         return i
 
@@ -479,23 +479,23 @@
         escaped."""
         x = match.group(1)
         if self.convertHTMLEntities and x in name2codepoint:
-            return unichr(name2codepoint[x])
+            return chr(name2codepoint[x])
         elif x in self.XML_ENTITIES_TO_SPECIAL_CHARS:
             if self.convertXMLEntities:
                 return self.XML_ENTITIES_TO_SPECIAL_CHARS[x]
             else:
-                return u'&%s;' % x
+                return '&%s;' % x
         elif len(x) > 0 and x[0] == '#':
             # Handle numeric entities
             if len(x) > 1 and x[1] == 'x':
-                return unichr(int(x[2:], 16))
+                return chr(int(x[2:], 16))
             else:
-                return unichr(int(x[1:]))
+                return chr(int(x[1:]))
 
         elif self.escapeUnrecognizedEntities:
-            return u'&amp;%s;' % x
+            return '&amp;%s;' % x
         else:
-            return u'&%s;' % x
+            return '&%s;' % x
 
     def __init__(self, parser, name, attrs=None, parent=None,
                  previous=None):
@@ -524,7 +524,7 @@
                 return kval
             return (k, re.sub("&(#\d+|#x[0-9a-fA-F]+|\w+);",
                               self._convertEntities, val))
-        self.attrs = map(convert, self.attrs)
+        self.attrs = list(map(convert, self.attrs))
 
     def get(self, key, default=None):
         """Returns the value of the 'key' attribute for the tag, or
@@ -533,7 +533,7 @@
         return self._getAttrMap().get(key, default)
 
     def has_key(self, key):
-        return self._getAttrMap().has_key(key)
+        return key in self._getAttrMap()
 
     def __getitem__(self, key):
         """tag[key] returns the value of the 'key' attribute for the tag,
@@ -551,7 +551,7 @@
     def __contains__(self, x):
         return x in self.contents
 
-    def __nonzero__(self):
+    def __bool__(self):
         "A tag is non-None even if it has no contents."
         return True
 
@@ -577,14 +577,14 @@
                 #We don't break because bad HTML can define the same
                 #attribute multiple times.
             self._getAttrMap()
-            if self.attrMap.has_key(key):
+            if key in self.attrMap:
                 del self.attrMap[key]
 
     def __call__(self, *args, **kwargs):
         """Calling a tag like a function is the same as calling its
         findAll() method. Eg. tag('a') returns a list of all the A tags
         found within this tag."""
-        return apply(self.findAll, args, kwargs)
+        return self.findAll(*args, **kwargs)
 
     def __getattr__(self, tag):
         #print "Getattr %s.%s" % (self.__class__, tag)
@@ -592,7 +592,7 @@
             return self.find(tag[:-3])
         elif tag.find('__') != 0:
             return self.find(tag)
-        raise AttributeError, "'%s' object has no attribute '%s'" % (self.__class__, tag)
+        raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__, tag))
 
     def __eq__(self, other):
         """Returns true iff this tag has the same name, the same attributes,
@@ -822,11 +822,11 @@
     def recursiveChildGenerator(self):
         if not len(self.contents):
             raise StopIteration
-        stopNode = self._lastRecursiveChild().next
+        stopNode = self._lastRecursiveChild().__next__
         current = self.contents[0]
         while current is not stopNode:
             yield current
-            current = current.next
+            current = current.__next__
 
     def childGenerator(self):
         if not len(self.contents):
@@ -880,7 +880,7 @@
             else:
                 match = True
                 markupAttrMap = None
-                for attr, matchAgainst in self.attrs.items():
+                for attr, matchAgainst in list(self.attrs.items()):
                     if not markupAttrMap:
                          if hasattr(markupAttrs, 'get'):
                             markupAttrMap = markupAttrs
@@ -921,14 +921,14 @@
             if self._matches(markup, self.text):
                 found = markup
         else:
-            raise Exception, "I don't know how to match against a %s" \
-                  % markup.__class__
+            raise Exception("I don't know how to match against a %s" \
+                  % markup.__class__)
         return found
 
     def _matches(self, markup, matchAgainst):
         #print "Matching %s against %s" % (markup, matchAgainst)
         result = False
-        if matchAgainst == True and type(matchAgainst) == types.BooleanType:
+        if matchAgainst == True and type(matchAgainst) == bool:
             result = markup != None
         elif callable(matchAgainst):
             result = matchAgainst(markup)
@@ -938,7 +938,7 @@
             if isinstance(markup, Tag):
                 markup = markup.name
             if markup is not None and not isString(markup):
-                markup = unicode(markup)
+                markup = str(markup)
             #Now we know that chunk is either a string, or None.
             if hasattr(matchAgainst, 'match'):
                 # It's a regexp object.
@@ -947,10 +947,10 @@
                   and (markup is not None or not isString(matchAgainst))):
                 result = markup in matchAgainst
             elif hasattr(matchAgainst, 'items'):
-                result = markup.has_key(matchAgainst)
+                result = matchAgainst in markup
             elif matchAgainst and isString(markup):
-                if isinstance(markup, unicode):
-                    matchAgainst = unicode(matchAgainst)
+                if isinstance(markup, str):
+                    matchAgainst = str(matchAgainst)
                 else:
                     matchAgainst = str(matchAgainst)
 
@@ -971,13 +971,13 @@
     """Convenience method that works with all 2.x versions of Python
     to determine whether or not something is listlike."""
     return ((hasattr(l, '__iter__') and not isString(l))
-            or (type(l) in (types.ListType, types.TupleType)))
+            or (type(l) in (list, tuple)))
 
 def isString(s):
     """Convenience method that works with all 2.x versions of Python
     to determine whether or not something is stringlike."""
     try:
-        return isinstance(s, unicode) or isinstance(s, basestring)
+        return isinstance(s, str) or isinstance(s, str)
     except NameError:
         return isinstance(s, str)
 
@@ -989,7 +989,7 @@
     for portion in args:
         if hasattr(portion, 'items'):
             #It's a map. Merge it.
-            for k,v in portion.items():
+            for k,v in list(portion.items()):
                 built[k] = v
         elif isList(portion) and not isString(portion):
             #It's a list. Map each item to the default.
@@ -1034,7 +1034,7 @@
         object, possibly one with a %SOUP-ENCODING% slot into which an
         encoding will be plugged later."""
         if text[:3] == "xml":
-            text = u"xml version='1.0' encoding='%SOUP-ENCODING%'"
+            text = "xml version='1.0' encoding='%SOUP-ENCODING%'"
         self._toStringSubclass(text, ProcessingInstruction)
 
     def handle_comment(self, text):
@@ -1044,7 +1044,7 @@
     def handle_charref(self, ref):
         "Handle character references as data."
         if self.soup.convertEntities:
-            data = unichr(int(ref))
+            data = chr(int(ref))
         else:
             data = '&#%s;' % ref
         self.handle_data(data)
@@ -1056,7 +1056,7 @@
         data = None
         if self.soup.convertHTMLEntities:
             try:
-                data = unichr(name2codepoint[ref])
+                data = chr(name2codepoint[ref])
             except KeyError:
                 pass
 
@@ -1147,7 +1147,7 @@
                        lambda x: '<!' + x.group(1) + '>')
                       ]
 
-    ROOT_TAG_NAME = u'[document]'
+    ROOT_TAG_NAME = '[document]'
 
     HTML_ENTITIES = "html"
     XML_ENTITIES = "xml"
@@ -1236,14 +1236,14 @@
     def _feed(self, inDocumentEncoding=None, isHTML=False):
         # Convert the document to Unicode.
         markup = self.markup
-        if isinstance(markup, unicode):
+        if isinstance(markup, str):
             if not hasattr(self, 'originalEncoding'):
                 self.originalEncoding = None
         else:
             dammit = UnicodeDammit\
                      (markup, [self.fromEncoding, inDocumentEncoding],
                       smartQuotesTo=self.smartQuotesTo, isHTML=isHTML)
-            markup = dammit.unicode
+            markup = dammit.str
             self.originalEncoding = dammit.originalEncoding
             self.declaredHTMLEncoding = dammit.declaredHTMLEncoding
         if markup:
@@ -1269,8 +1269,8 @@
     def isSelfClosingTag(self, name):
         """Returns true iff the given string is the name of a
         self-closing tag according to this parser."""
-        return self.SELF_CLOSING_TAGS.has_key(name) \
-               or self.instanceSelfClosingTags.has_key(name)
+        return name in self.SELF_CLOSING_TAGS \
+               or name in self.instanceSelfClosingTags
 
     def reset(self):
         Tag.__init__(self, self, self.ROOT_TAG_NAME)
@@ -1305,7 +1305,7 @@
 
     def endData(self, containerClass=NavigableString):
         if self.currentData:
-            currentData = u''.join(self.currentData)
+            currentData = ''.join(self.currentData)
             if (currentData.translate(self.STRIP_ASCII_SPACES) == '' and
                 not set([tag.name for tag in self.tagStack]).intersection(
                     self.PRESERVE_WHITESPACE_TAGS)):
@@ -1368,7 +1368,7 @@
 
         nestingResetTriggers = self.NESTABLE_TAGS.get(name)
         isNestable = nestingResetTriggers != None
-        isResetNesting = self.RESET_NESTING_TAGS.has_key(name)
+        isResetNesting = name in self.RESET_NESTING_TAGS
         popTo = None
         inclusive = True
         for i in range(len(self.tagStack)-1, 0, -1):
@@ -1381,7 +1381,7 @@
             if (nestingResetTriggers != None
                 and p.name in nestingResetTriggers) \
                 or (nestingResetTriggers == None and isResetNesting
-                    and self.RESET_NESTING_TAGS.has_key(p.name)):
+                    and p.name in self.RESET_NESTING_TAGS):
 
                 #If we encounter one of the nesting reset triggers
                 #peculiar to this tag, or we encounter another tag
@@ -1399,7 +1399,7 @@
         if self.quoteStack:
             #This is not a real tag.
             #print "<%s> is not real!" % name
-            attrs = ''.join(map(lambda(x, y): ' %s="%s"' % (x, y), attrs))
+            attrs = ''.join([' %s="%s"' % (x_y[0], x_y[1]) for x_y in attrs])
             self.handle_data('<%s%s>' % (name, attrs))
             return
         self.endData()
@@ -1493,7 +1493,7 @@
     BeautifulStoneSoup before writing your own subclass."""
 
     def __init__(self, *args, **kwargs):
-        if not kwargs.has_key('smartQuotesTo'):
+        if 'smartQuotesTo' not in kwargs:
             kwargs['smartQuotesTo'] = self.HTML_ENTITIES
         kwargs['isHTML'] = True
         BeautifulStoneSoup.__init__(self, *args, **kwargs)
@@ -1677,7 +1677,7 @@
             parent._getAttrMap()
             if (isinstance(tag, Tag) and len(tag.contents) == 1 and
                 isinstance(tag.contents[0], NavigableString) and
-                not parent.attrMap.has_key(tag.name)):
+                tag.name not in parent.attrMap):
                 parent[tag.name] = tag.contents[0]
         BeautifulStoneSoup.popTag(self)
 
@@ -1751,9 +1751,9 @@
                      self._detectEncoding(markup, isHTML)
         self.smartQuotesTo = smartQuotesTo
         self.triedEncodings = []
-        if markup == '' or isinstance(markup, unicode):
+        if markup == '' or isinstance(markup, str):
             self.originalEncoding = None
-            self.unicode = unicode(markup)
+            self.str = str(markup)
             return
 
         u = None
@@ -1766,7 +1766,7 @@
                 if u: break
 
         # If no luck and we have auto-detection library, try that:
-        if not u and chardet and not isinstance(self.markup, unicode):
+        if not u and chardet and not isinstance(self.markup, str):
             u = self._convertFrom(chardet.detect(self.markup)['encoding'])
 
         # As a last resort, try utf-8 and windows-1252:
@@ -1775,7 +1775,7 @@
                 u = self._convertFrom(proposed_encoding)
                 if u: break
 
-        self.unicode = u
+        self.str = u
         if not u: self.originalEncoding = None
 
     def _subMSChar(self, match):
@@ -1783,7 +1783,7 @@
         entity."""
         orig = match.group(1)
         sub = self.MS_CHARS.get(orig)
-        if type(sub) == types.TupleType:
+        if type(sub) == tuple:
             if self.smartQuotesTo == 'xml':
                 sub = '&#x'.encode() + sub[1].encode() + ';'.encode()
             else:
@@ -1813,7 +1813,7 @@
             u = self._toUnicode(markup, proposed)
             self.markup = u
             self.originalEncoding = proposed
-        except Exception, e:
+        except Exception as e:
             # print "That didn't work!"
             # print e
             return None
@@ -1842,7 +1842,7 @@
         elif data[:4] == '\xff\xfe\x00\x00':
             encoding = 'utf-32le'
             data = data[4:]
-        newdata = unicode(data, encoding)
+        newdata = str(data, encoding)
         return newdata
 
     def _detectEncoding(self, xml_data, isHTML=False):
@@ -1855,41 +1855,41 @@
             elif xml_data[:4] == '\x00\x3c\x00\x3f':
                 # UTF-16BE
                 sniffed_xml_encoding = 'utf-16be'
-                xml_data = unicode(xml_data, 'utf-16be').encode('utf-8')
+                xml_data = str(xml_data, 'utf-16be').encode('utf-8')
             elif (len(xml_data) >= 4) and (xml_data[:2] == '\xfe\xff') \
                      and (xml_data[2:4] != '\x00\x00'):
                 # UTF-16BE with BOM
                 sniffed_xml_encoding = 'utf-16be'
-                xml_data = unicode(xml_data[2:], 'utf-16be').encode('utf-8')
+                xml_data = str(xml_data[2:], 'utf-16be').encode('utf-8')
             elif xml_data[:4] == '\x3c\x00\x3f\x00':
                 # UTF-16LE
                 sniffed_xml_encoding = 'utf-16le'
-                xml_data = unicode(xml_data, 'utf-16le').encode('utf-8')
+                xml_data = str(xml_data, 'utf-16le').encode('utf-8')
             elif (len(xml_data) >= 4) and (xml_data[:2] == '\xff\xfe') and \
                      (xml_data[2:4] != '\x00\x00'):
                 # UTF-16LE with BOM
                 sniffed_xml_encoding = 'utf-16le'
-                xml_data = unicode(xml_data[2:], 'utf-16le').encode('utf-8')
+                xml_data = str(xml_data[2:], 'utf-16le').encode('utf-8')
             elif xml_data[:4] == '\x00\x00\x00\x3c':
                 # UTF-32BE
                 sniffed_xml_encoding = 'utf-32be'
-                xml_data = unicode(xml_data, 'utf-32be').encode('utf-8')
+                xml_data = str(xml_data, 'utf-32be').encode('utf-8')
             elif xml_data[:4] == '\x3c\x00\x00\x00':
                 # UTF-32LE
                 sniffed_xml_encoding = 'utf-32le'
-                xml_data = unicode(xml_data, 'utf-32le').encode('utf-8')
+                xml_data = str(xml_data, 'utf-32le').encode('utf-8')
             elif xml_data[:4] == '\x00\x00\xfe\xff':
                 # UTF-32BE with BOM
                 sniffed_xml_encoding = 'utf-32be'
-                xml_data = unicode(xml_data[4:], 'utf-32be').encode('utf-8')
+                xml_data = str(xml_data[4:], 'utf-32be').encode('utf-8')
             elif xml_data[:4] == '\xff\xfe\x00\x00':
                 # UTF-32LE with BOM
                 sniffed_xml_encoding = 'utf-32le'
-                xml_data = unicode(xml_data[4:], 'utf-32le').encode('utf-8')
+                xml_data = str(xml_data[4:], 'utf-32le').encode('utf-8')
             elif xml_data[:3] == '\xef\xbb\xbf':
                 # UTF-8 with BOM
                 sniffed_xml_encoding = 'utf-8'
-                xml_data = unicode(xml_data[3:], 'utf-8').encode('utf-8')
+                xml_data = str(xml_data[3:], 'utf-8').encode('utf-8')
             else:
                 sniffed_xml_encoding = 'ascii'
                 pass
@@ -1954,7 +1954,7 @@
                     250,251,252,253,254,255)
             import string
             c.EBCDIC_TO_ASCII_MAP = string.maketrans( \
-            ''.join(map(chr, range(256))), ''.join(map(chr, emap)))
+            ''.join(map(chr, list(range(256)))), ''.join(map(chr, emap)))
         return s.translate(c.EBCDIC_TO_ASCII_MAP)
 
     MS_CHARS = { '\x80' : ('euro', '20AC'),
@@ -1997,4 +1997,4 @@
 if __name__ == '__main__':
     import sys
     soup = BeautifulSoup(sys.stdin)
-    print soup.prettify()
+    print(soup.prettify())
