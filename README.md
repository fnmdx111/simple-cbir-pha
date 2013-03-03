Simple CBIR with Simple PHA
===========================

GOAL
----

Find out images that are similar to the specified one within given image set.

* gui (web app or pyqt if nothing else)
* replaceable hash algorithm
* more...


DEPENDENCY
----------

+ PIL
+ Flask
+ Flask-Bootstrap
+ (possibly Pymongo for data persistence)
+ (possibly watchdog for folder change notification)


CHANGELOG
---------

+ 13/03/03 complete retrieve images by url and hash, retrieving by uploading local image has been delayed
+ 13/01/24 fixed bugs in lib/disjoint_set.py
+ 13/01/23 core prototype completed
