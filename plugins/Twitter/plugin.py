import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks

import calendar
from random import choice
import re
import simplejson
import supybot.utils.web as web
import time
import datetime
from urllib import urlencode, quote
from BeautifulSoup import BeautifulStoneSoup as BSS
import lxml.html
import tweepy


HEADERS = dict(ua = 'Zoia/1.0 (Supybot/0.83; Twitter Plugin; http://code4lib.org/irc)')

class Twitter(callbacks.Plugin):
    """Add the help for "@plugin help Twitter" here
    This should describe *how* to use this plugin."""
    threaded = True

    def __init__(self, irc):
      self.__parent = super(Twitter, self)
      self.__parent.__init__(irc)
      self.last_mention = None
      self.last_request = 0
      self.api = self._api()

        
    def __call__(self, irc, msg):
      self.__parent.__call__(irc, msg)
      now = time.time()
      wait = self.registryValue('waitPeriod')
      if now - self.last_request > wait:
        self.last_request = now
        irc = callbacks.SimpleProxy(irc, msg)
        responses = self._get_mentions(maxAge=7200)
        if len(responses) > 0:
          irc.reply(' ; '.join(responses), to='#code4lib', prefixNick=False)

    def _api(self):
        auth = tweepy.OAuthHandler('BahWsa9ynBogaXxRoJPX5Q', '5bWdyET8iFpFUlpFuFJV02NOILoKEn5u6jt7TwXoXI')
        auth.set_access_token('116458525-eI3WNzzatAm4S7DjYzX5fjOCr1wGyY0NtrOdfOqk','H0I2F1cvL8Z421isUW4nARTgEC0nbDBFCmF4lLoE')
        return tweepy.API(auth)

    def tweet(self, irc, msg, args, user, text):
        """<text>

   Post to the @bot4lib Twitter account"""
        #      tweet_text = '<%s> %s' % (user.name, text)
        tweet_text = self._shorten_urls(text)
        if len(tweet_text) > 140:
            truncate_msg = " Tweet was truncated from original %d characters" % len(tweet_text)
            while len(tweet_text) + 3 > 140:
                tweet_text = tweet_text[:len(tweet_text) - 1]
            tweet_text = tweet_text + '...'
        else:
            truncate_msg = ""

        self.api.update_status(tweet_text )
        irc.reply('The operation succeeded.%s' % truncate_msg)

    tweet = wrap(tweet, ['user','text'])

    def _shorten_urls(self, s):
        result = s
        urlreg = re.compile('[a-z]+://[^\s\[({\]})]+')
        for longUrl in urlreg.findall(s):
            if len(longUrl) > 22:
                params = { 'longUrl' : longUrl, 'login' : 'zoia', 'apiKey' : 'R_e0079bf72e9c5f53bb48ef0fe706a57c',
                           'version' : '2.0.1', 'format' : 'json' }
                url = 'http://api.bit.ly/shorten?' + urlencode(params)
                response = self._fetch_json(url)
                shortUrl = response['results'][longUrl]['shortUrl']
                result = result.replace(longUrl,shortUrl)
        return(result)

    def _lengthen_urls(self, tweet):
        for link in tweet.entities['urls']:
            tweet.text = tweet.text.replace(link['url'], link['expanded_url'])
        for media in tweet.entities.get('media', []):
            tweet.text = tweet.text.replace(media.url, media.media_url)

    def twit(self, irc, msg, args, opts, query):
        """
        @twit [--from user] [--id tweet_id] [query]

        Return the last three tweets matching a given string
        and/or user. if no query specified returns a random tweet from
        the public timeline if no options given.
        """

        screen_name = None
        tweet_id = None

        for (opt, arg) in opts:
            if opt == 'from':
                screen_name = arg
            if opt == 'id':
                tweet_id = arg


        def recode(text):
            return BSS(text.encode('utf8','ignore'), convertEntities=BSS.HTML_ENTITIES)

        resp = 'Gettin nothin from teh twitter.'
        if tweet_id:
            tweet = self.api.get_status(tweet_id)
            self._lengthen_urls(tweet)
            resp = "<%s> %s" % (tweet.author.screen_name, recode(tweet.text))
        elif query:
            if screen_name:
                query = "%s %s" % (screen_name, query)
            tweets = self.api.search(query)
            try:
                for tweet in tweets:
                    self._lengthen_urls(tweet)
                extracted = ["<%s> %s" % (x.author.screen_name, recode(x.text)) for x in tweets]
                resp = ' ;; '.join(extracted)
            except:
                pass
        else:
            if screen_name:
                tweets = self.api.user_timeline(screen_name)
            else:
                tweets = self.api.public_timeline()
            if tweets:
                tweet = tweets[0] #randint(0, len(tweets)-1)]
                self._lengthen_urls(tweet)
                resp = "%s: %s" % (tweet.author.screen_name, recode(tweet.text))
        irc.reply(resp.replace('\n',' ').strip(' '))

    twit = wrap(twit, [getopts({'from':'something','id':'something'}), optional('text')])


    def dogs(self, irc, msg, args, channel, name):
        """
        @dogs [user]

        Dr. dogsdoingthings describes the philosomatic state of
        a random channel member, or [user] if specified.
        """

        resp = u"Dogs positing that, in the infinite timeframe of the universe, a bug is indistinguishable from an unknown feature."
        if name:
            username = name
        else:
            username = choice(list(irc.state.channels[channel].users))

        url = 'http://api.twitter.com/1/statuses/user_timeline.json?screen_name=dogsdoingthings&count=100'

        tweets = self.api.user_timeline('dogsdoingthings', count=100)
        if tweets:
            resp = choice(tweets).text

        irc.reply(resp.replace("Dogs", username).strip(' '))

    dogs = wrap(dogs, ['channeldb', optional('text')])

    def _get_mentions(self, maxAge = None):
        params = {}
        if self.last_mention != None:
            tweets = self.api.mentions_timeline(since_id=self.last_mention)
        else:
            tweets=self.api.mentions_timeline()
        responses = []
        if tweets:
            now = datetime.datetime.now()
            self.last_mention = tweets[0].id
            for tweet in tweets:
                age = now - tweet.created_at
                if (maxAge is None) or (age <= datetime.timedelta(seconds=maxAge)):
                    self._lengthen_urls(tweet)
                    responses.append('<%s> %s' % (tweet.author.screen_name,tweet.text))
            responses.reverse()
        return responses

Class = Twitter


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
