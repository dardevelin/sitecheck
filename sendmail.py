--- sendmail.py	(original)
+++ sendmail.py	(refactored)
@@ -55,6 +55,6 @@
 def safe_unicode(textstring):
     """ Returns a unicode representation of the given string. """
     try:
-        return unicode(textstring, "UTF-8")
+        return str(textstring, "UTF-8")
     except TypeError:
         return textstring #was already unicode
