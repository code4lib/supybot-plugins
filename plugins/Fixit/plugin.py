from supybot.commands import *
from random import choice
import supybot.callbacks as callbacks

class Fixit(callbacks.Plugin):

    def fixit(self, irc, msg, args):
      """
      Get advice for solving your intractable tech problems.
      """
      
      verbs = ['attackclone', 'bootstrap', 'tweetybird', 'architect', 
               'merge', 'compile', 'boilerstrap', 'git push', 'fork',
               'configure', 'hash', 'salt', 'commit', 'echo', 'version',
               'create value for', 'facet', 're-index', 'relevance-rank',
               'monkeypatch', 'scrape', 'install', 'mashup', 'integrate',
               'snippet', 'wikify', 'network', 'proxy', 'toggle', 'reboot',
               'visualize', 'federate', 'curate', 'gamify', 'crowdsource',
               'scale up', 'cloud-host', 'progressively enhance', 
               'open-source', 'havisham', 'refactor', 'empower',
               'continuously deploy', 'inject', 'mock', 'BBM me',
               'face-time', 'migrate', 'nextgen', 'panoramically photograph',
               'SMS', 'shibbolize', 'hack', 'munge', 'yak-shave', 'rebase',
               'polish', 'fastfail', 'serialize', 'queue up', 'shard',
               'replicate', 'index', 'transliterate', 'subclass',
               'superclass', 'catalog', 'interleave', 'mesh'
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
               'unit tests', 'dependency', 'QR codes', 'plugin','backend',
               'frontend','middleware','CAS', 'robots', 'robots.txt',
               'hackfest', 'encoding', 'utf8', 'MARC8', 'pumpkins', 
               'pumpkin patch', 'turd', 'web hook', 'callback', 'shard',
               'hydra head', 'fulltext', 'diacritics', 'EAD',
               'Mechanical Turk', 'quine relay', 'INTERCAL', 'mesh network',
               'octothorpe'
      ]
      
      verb = choice(verbs)
      object = choice(nouns)
      tool = choice(nouns)
      advice = "Just "+verb+" the "+object+" with your "+tool+"."
      irc.reply(advice, prefixNick=True)

Class = Fixit
