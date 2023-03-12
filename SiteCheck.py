--- SiteCheck.py	(original)
+++ SiteCheck.py	(refactored)
@@ -25,7 +25,7 @@
             if len(diff.strip()) > 0:
                 sitesWithDiff[site] = diff.strip()
 
-    print "Found",len(sitesWithDiff), "Sites with diffs"
+    print("Found",len(sitesWithDiff), "Sites with diffs")
 
     # construct the email notice
     if len(sitesWithDiff) > 0:
@@ -43,8 +43,8 @@
 	subject += " " + strftime("%d.%m.%Y")
         text += "SiteCheck.py - " + VERSION
 
-        print subject
-        print text
+        print(subject)
+        print(text)
 
 	# Send the mail to every address in mails.txt
         mails = open("mails.txt", "r").readlines()
@@ -60,6 +60,6 @@
     try:
         sys.exit(checkSites())
     except Exception as err:
-	print err # Stupid but gets the job done...
+	print(err) # Stupid but gets the job done...
 	sys.exit(1)
 
