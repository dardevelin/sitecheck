--- sites.py	(original)
+++ sites.py	(refactored)
@@ -2,7 +2,7 @@
 Used as a centralized way to send email over an SMTP server.
 '''
 import os
-import urllib2
+import urllib.request, urllib.error, urllib.parse
 import shutil
 
 from BeautifulSoup import BeautifulSoup
@@ -28,9 +28,9 @@
             if len(parts) == 2:
                 sites[parts[0].strip()] = parts[1].strip()
             else:
-                print "Unknown site format: {0}".format(site)
+                print("Unknown site format: {0}".format(site))
         except exception as err:
-            print "Error: {0}".format(err)
+            print("Error: {0}".format(err))
             
     return sites
 
@@ -48,7 +48,7 @@
     diff = None
     url = siteDict[site]
     hash = url.__hash__()
-    content = urllib2.urlopen(url).read()
+    content = urllib.request.urlopen(url).read()
     prettyContent = BeautifulSoup(content).prettify()
     
     if not os.path.exists(site + ".old"):
