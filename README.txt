Google App Engine App that uses PubSubHubbub to cross post your Google Buzz feed in realtime to Blogger.

Notes:
* There are likely hardcoded strings to "buzztoblogger.appspot.com".
* Most of the included libs are unnecessary (not trimmed).
* Some of them are, and one is modified (one of the gdata/gauth libs), as there
  is a bug with the standard lib and auth tokens not tied to an active AppEngine
  user session.

Example Running App Site:
http://buzztoblogger.appspot.com/
