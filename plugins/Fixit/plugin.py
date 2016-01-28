# -*- coding: utf-8 -*-
from supybot.commands import *
from random import choice
import supybot.callbacks as callbacks

class Fixit(callbacks.Plugin):

    verbs = ['attackclone', 'bootstrap', 'tweetybird', 'architect',
           'merge', 'compile', 'boilerstrap', 'git push', 'fork',
           'configure', 'hash', 'salt', 'commit', 'echo', 'version',
           'create value for', 'facet', 're-index', 'relevance-rank',
           'monkeypatch', 'scrape', 'install', 'mashup', 'integrate',
           'snippet', 'wikify', 'network', 'proxy', 'toggle', 'reboot',
           'visualize', 'federate', 'curate', 'gamify', 'crowdsource',
           'scale up', 'cloud-host', 'progressively enhance',
           'open-source', 'havisham', 'refactor', 'empower',
           'continuously deploy', 'inject', 'mock', 'BBM',
           'face-time', 'migrate', 'nextgen', 'panoramically photograph',
           'SMS', 'shibbolize', 'hack', 'munge', 'yak-shave', 'rebase',
           'polish', 'fastfail', 'serialize', 'queue up', 'shard',
           'replicate', 'index', 'transliterate', 'subclass',
           'superclass', 'catalog', 'interleave', 'mesh',
           'disintermediate','multitenancyize','dashboard','onboard',
           'whiteboard','paper prototype','containerize','centralize',
           'decentralize', 'pip install', 'puppetize', 'quantize',
           'monetize', 'pipe', 'wag', 'vagrant up', 'sniff', 'smoke out',
           'light up', 'spin up', 'multitennantize', 'bucketize',
           'Uberize', 'commoditize', 'swipe', 'jiggle', 'relay',
           'innovate', 'vlog', 'disrupt', 'fuzzy match', 'transcode',
           'upload', 'QA', 'breakpoint', 'uberize', 'subtweet'
    ]

    nouns = ['framework', 'html5', 'rubygem', 'shawarma', 'web app',
           'nodefiddle', 'node.js', 'responsive design', 'SSID',
           'Apache', 'command line', 'supybot', 'repo', 'regexp',
           'model instance', 'heroku', 'EC2 instance', 'Islandora',
           'lambda function', 'RESTful JSON API', 'Solr', 'cloud',
           'data', 'Drupal module', 'OAI-PMH', 'metadata', 'schema',
           'Blacklight', 'tweetybird', 'social media', 'backbone',
           'cross-universe compatibility', 'boilerstrap', 'html9',
           'beautifulsoup', 'failwhale', 'mashup', 'cookie', 'dongle',
           'discovery layer', 'architecture', 'github', 'zoia',
           'jquery', 'network', 'transistor', 'PDP-11', 'Fortran',
           'analytics', 'Z39.50', 'skunkworks', 'hadoop', 'persona',
           'web scale cloud ILS', 'scalability', 'singularity',
           'semantic web', 'triplestore', 'SFX', 'Fedora', 'Umlaut',
           u'\xdcml\xe4\xfct', 'pip', 'AbstractSingletonProxyFactoryBean',
           'platform', 'persistent database', 'user', 'Cucumber',
           'beans', 'analytics', 'bitcoin', 'test harness',
           'unit tests', 'dependency', 'QR codes', 'plugin', 'backend',
           'frontend','middleware','CAS', 'robots', 'robots.txt',
           'hackfest', 'encoding', 'utf8', 'MARC8', 'pumpkins',
           'pumpkin patch', 'bot', 'web hook', 'callback', 'shard',
           'hydra head', 'fulltext', 'diacritics', 'EAD',
           'Mechanical Turk', 'quine relay', 'INTERCAL', 'mesh network',
           'octothorpe', 'time machine', 'cross-connected faceplates',
           'reverse library disintermediation', 'doge', 'dogecoin',
           'dashboard', 'punchline', 'visualization', 'encoder',
           'transistor', 'ORM','nanotube','container','cathedral',
           'bazaar', 'emoji', 'devops', 'puppet', 'chef', 'ansible',
           'docker', 'engagement', 'brand', 'self-driving car',
           'MongoDB', 'CouchDB', 'NoSQL', 'SPARQL', 'brony',
           'magical SPARQLpony', 'octocat', 'antipattern', 'haddock',
           u'Heiðrún', 'Updog', 'Hypervisor', 'packets', 'infrastructure',
           'buckets', 'stack', 'slack', 'eyeballs', 'PaaS', 'vlog',
           'SaaS', 'vortal', 'workflow', 'folksonomy', 'DevOps',
           'slack channel', 'hipchat', 'rsync', 'beanstalk', 'unicorn',
           'uber', 'subtweet'
    ]

    def _genwords(self):
        while True:
            verb = choice(self.verbs)
            noun1 = choice(self.nouns)
            noun2 = choice(self.nouns)
            if len(dict((x,1) for x in [verb, noun1, noun2])) == 3:
                return verb, noun1, noun2

    def fixit(self, irc, msg, args):
        """
        Get advice for solving your intractable tech problems.
        """

        verb, thingy, tool = self._genwords()
        advice = "Just "+verb+" the "+thingy+" with your "+tool+"."
        irc.reply(advice, prefixNick=True)

    def mynewstartup(self, irc, msg, args, who):
        """
        Your new business plan.  It is genius.  It cannot fail.
        """

        if who is None:
            owner = "Your"
        else:
            owner = "%s's" % who

        verb, simile, awesomesauce = self._genwords()

        if simile[0] in ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']:
            article = " an "
        else:
            article = " a "
        genius_plan = "%s new startup? It's like%s%s, but you %s it with " \
                      "your %s" % (owner, article, simile, verb, awesomesauce)
        irc.reply(genius_plan, prefixNick=True)

    def notmycircus(self, irc, msg, args, who):
        """
        Not your circus, not your monkeys.
        """
        if who is None:
            owner = "your"
            prefix = True
        else:
            owner = "%s's" % who
            prefix = False

        noun1 = choice(self.nouns)
        noun2 = choice(self.nouns)

        # dubious pluralization rule
        if noun2[-1] != 's':
            noun2 = noun2 + 's'

        relief = u"Not %s %s, not %s %s." % (owner, noun1, owner, noun2)
        irc.reply(relief, prefixNick=prefix)

    mynewstartup = wrap(mynewstartup, [ optional('text') ])
    startup = mynewstartup

    notmycircus = wrap(notmycircus, [ optional('text') ])
    circus = notmycircus

Class = Fixit
