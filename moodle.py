--- moodle.py	(original)
+++ moodle.py	(refactored)
@@ -1,6 +1,6 @@
 #!/usr/bin/env python
 # -*- coding: utf-8 -*-
-import urllib, urllib2, re, cookielib, os, hashlib, sendmail
+import urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse, re, http.cookiejar, os, hashlib, sendmail
 from BeautifulSoup import BeautifulSoup
 from threading import Thread
 from time import strftime
@@ -12,12 +12,12 @@
                 'Accept-Encoding': 'utf-8'                                   
             } 
     if(postData is not None):
-        postData = urllib.urlencode(postData)
-    req = urllib2.Request(url, postData, header)
+        postData = urllib.parse.urlencode(postData)
+    req = urllib.request.Request(url, postData, header)
     try:
-        return urllib2.urlopen(req)
-    except urllib2.HTTPError, e:
-        print 'Error Code:', e.code
+        return urllib.request.urlopen(req)
+    except urllib.error.HTTPError as e:
+        print('Error Code:', e.code)
         return None
 
 class Course(Thread):
@@ -34,7 +34,7 @@
         links = soup.findAll(attrs={'href' : re.compile("resource/view.php")})
         for link in links:
             if not(link.span is None):
-                new = self.download(link['href'], link.span.next, self.CourseName)
+                new = self.download(link['href'], link.span.__next__, self.CourseName)
                 for n in new:
                     self.newFiles.append(n)
     
@@ -59,7 +59,7 @@
                 files = soup.findAll(attrs={'href' : re.compile("http://moodle.uni-duisburg-essen.de/file.php")})
                 dirs = soup.findAll(attrs={'href' : re.compile("subdir")})
     
-                folder = re.sub(u"[^a-zA-Z0-9_()äÄöÖüÜ ]", "", folder).strip()
+                folder = re.sub("[^a-zA-Z0-9_()äÄöÖüÜ ]", "", folder).strip()
                 for f in files:
                     savedFile = self.saveFile(f['href'], folder)
                     if(len(savedFile) > 0):
@@ -170,10 +170,10 @@
 casService = "http://moodle.uni-duisburg-essen.de/login/index.php?authCAS=CAS"
 
 # Setup
-jar = cookielib.CookieJar()
-handler = urllib2.HTTPCookieProcessor(jar)
-opener = urllib2.build_opener(handler)
-urllib2.install_opener(opener)
+jar = http.cookiejar.CookieJar()
+handler = urllib.request.HTTPCookieProcessor(jar)
+opener = urllib.request.build_opener(handler)
+urllib.request.install_opener(opener)
     
 # Get token
 data = getResponse(casUrl).read()
@@ -201,7 +201,7 @@
 
 for link in links:
     CourseName = link.string.replace("&amp;", "&")
-    CourseName = re.sub(u"[^a-zA-Z0-9_() ]", "", CourseName).strip()
+    CourseName = re.sub("[^a-zA-Z0-9_() ]", "", CourseName).strip()
     #print u"Kurs: " + CourseName
     current = Course(link['href'], CourseName)
     courses.append(current)
