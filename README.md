unfollowed
=============

Outsmart the Twitter Unfollow Bug

* Written by David Longenecker
* Twitter: @dnlongen
* Email: david (at) securityforrealpeople.com

It is widely acknowledged, if not proven, that Twitter has an "unfollow" bug that causes users to stop following others. This script is a simple attempt to help. The first time it is run, it will store a list of users that you follow. On all future runs, it will by default give you a list of changes - all new users you have started following, and all previous users you no longer follow. With the -l parameter, it will also identify everyone you are following instead of just the changes.

The Twitter API allows querying a maximum of 5,000 followed accounts before breaking the list into pages; as I have not implemented any page handling, this script is practically limited to 5,000 accounts followed.

By default, unfollowed will use the Twitter account associated with the API token used, but you can supply an alternate (your "@name") via the -a argument.

If Internet access requires a proxy, supply it with the parameter -p, in the form of https://proxy.url:port, for instance, -p https://proxy.abc.com:8080


Requirements:
=============

* Requires tweepy, the Twitter API module for Python, available from https://github.com/tweepy/tweepy
* Requires an application token for the Twitter API. Refer to documentation at https://dev.twitter.com/oauth/overview/application-owner-access-tokens, and set up your own app-specific tokens at https://apps.twitter.com
 

Usage:
=============

```
usage: following.py [-h] [-a TWITTER_ALIAS] [-l] [-p PROXY]

Details about who you are following, and who you have followed or unfollowed
since the last time this tool ran. Twitter has a widely acknowledged but not
understood "unfollow bug" in which you may stop following others for no
apparent reason. This script is useful for seeing whom you have unfollowed.

optional arguments:
  -h, --help            show this help message and exit
  -a TWITTER_ALIAS, --alias TWITTER_ALIAS
                        Twitter alias whose follows to analyze. If none
                        provided, will default to the user whose API key is
                        used.
  -l, --list-all        List all aliases I am following (instead of only
                        showing the change since the last run)
  -p PROXY, --proxy PROXY
                        HTTPS proxy to use, if necessary, in the form of
                        https://proxy.com:port
```

Change Log:
=============

* v0.1 Original release.

Errata:
=============

* TBD
