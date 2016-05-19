'''
following v0.1
Source: https://github.com/dnlongen/following
Author: David Longenecker
Author email: david@securityforrealpeople.com 
Author Twitter: @dnlongen
Requires tweepy, the Twitter API module for Python, available from https://github.com/tweepy/tweepy
Requires an application token for the Twitter API. See https://dev.twitter.com/oauth/overview/application-owner-access-tokens for documentation, and https://apps.twitter.com to generate your tokens
'''

import argparse, tweepy, sys, codecs, time, csv
debug = False

#########################################################################
# Replace the below values with your own, from https://apps.twitter.com #
consumer_key = <your consumer key>
consumer_secret = <your consumer secret>
access_token = <your access token>
access_token_secret = <your access token secret>
#########################################################################

# Define supported parameters and default values
parser = argparse.ArgumentParser(description='Details about who you are following, and who you have followed or unfollowed since the last time this tool ran. Twitter has a widely acknowledged but not understood \"unfollow bug\" in which you may stop following others for no apparent reason. This script is useful for seeing whom you have unfollowed.')
parser.add_argument('-a', '--alias', dest='twitter_alias', default='', required=False, help='Twitter alias whose follows to analyze. If none provided, will default to the user whose API key is used.')
parser.add_argument('-l', '--list-all', dest='list_all', default=False, action='store_true', help='List all aliases I am following (instead of only showinf the change since the last run)')
parser.add_argument('-p', '--proxy', default='', required=False, help='HTTPS proxy to use, if necessary, in the form of https://proxy.com:port')
args=parser.parse_args()
twitter_user=args.twitter_alias
https_proxy=args.proxy
list_all=args.list_all

#Uncomment for Python 2:
#if sys.stdout.encoding != 'cp850':
#  sys.stdout = codecs.getwriter('cp850')(sys.stdout, 'xmlcharrefreplace')
#if sys.stderr.encoding != 'cp850':
#  sys.stderr = codecs.getwriter('cp850')(sys.stderr, 'xmlcharrefreplace')

#Uncomment for Python 3:
#if sys.stdout.encoding != 'cp850':
#  sys.stdout = codecs.getwriter('cp850')(sys.stdout.buffer, 'xmlcharrefreplace')
#if sys.stderr.encoding != 'cp850':
#  sys.stderr = codecs.getwriter('cp850')(sys.stderr.buffer, 'xmlcharrefreplace')

def chunks(l, n):
    # Break a list "l" into a list of smaller lists of maximum length "n"
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]


#################################################################################################
# Main body
#################################################################################################

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,proxy=https_proxy)
if (twitter_user==""): twitter_user=api.me().screen_name
print("Processing user " + twitter_user)
following=api.friends_ids(twitter_user)

if debug: print("Currently following: " + str(following))
filename=twitter_user + ".dat"
# first, if file already exists, read it in as oldfollowing
try:
    with open(filename, 'r') as followingfile:
        for row in csv.reader(followingfile):
            oldfollowing = list(map(int,row))
            if debug: print("Previously following: " + str(oldfollowing))
except:
    # most likely the file does not exist.
    if debug: print("Could not open file " + filename)

# second, write following to the file
try:
    with open(filename, 'w') as followingfile:
        wr = csv.writer(followingfile, quoting=csv.QUOTE_ALL)
        wr.writerow(following)

except:
    print("Error - could not write to file " + filename)

if (list_all):
    # default mode: show all currently following
    following_chunked=chunks(following, 100)
    for sublist in following_chunked:
        sublisted = api.lookup_users(sublist)
        for friend in sublisted:
            print("Friend: " + str(friend.id) + " (@" + friend.screen_name + ": " + friend.name + ")")

print("")
print("===================================================================================")
print("=======                     Users UNfollowed since last run                     ===")
print("===================================================================================")
unfollowed_chunked=chunks(list(set(oldfollowing) - set(following)), 100)
for sublist in unfollowed_chunked:
    sublisted = api.lookup_users(sublist)
    for friend in sublisted:
        print("Friend: " + str(friend.id) + " (@" + friend.screen_name + ": " + friend.name + ")")

print("")
print("===================================================================================")
print("=======                      Users followed since last run                      ===")
print("===================================================================================")
followed_chunked=chunks(list(set(following) - set(oldfollowing)), 100)
for sublist in followed_chunked:
    sublisted = api.lookup_users(sublist)
    for friend in sublisted:
        print("Friend: " + str(friend.id) + " (@" + friend.screen_name + ": " + friend.name + ")")
