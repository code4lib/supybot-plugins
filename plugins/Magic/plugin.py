###
# Copyright (c) 2013, Chad Nelson
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import supybot.utils.web as web

from urllib import urlopen
import json
from random import randint

HEADERS = {'User-Agent': 'Zoia/1.0 (Supybot/0.83; Magic The Gathering Plugin; http://code4lib.org/irc)'}
MTG_URL = "http://mtgapi.com/api/v1/fetch/"


class Magic(callbacks.Plugin):

    def magic(self, irc, msg, args, option):
        """(magic [id]): Casts a random Magic the Gathering card from http://mtgapi.com"""
        if option:

            body = urlopen(MTG_URL + "id/%s" % (option)).read()
        else:
            body = urlopen(MTG_URL + "id/%s" % (randint(1,4500))).read()

        card = json.loads(body)
        response = self._howToCastCard(card, msg)


        irc.reply(response, prefixNick=False)

    magic = wrap(magic, [optional('text')])

    def _howToCastCard(self, card, msg):

        title = self._titlePrep(card['name'])
        type  = card['type']
        text  = u' '.join(card['text'])
        flavor = u' '.join(card['flavor'][0]) if card['flavor'] else ''

        action = "plays"
        if "Land" in type:
            action  = u"lays down"
        if "Sorcery" in type:
            action = u"casts"
        if "Creature " in type:
            action = u"summons"
        response = u"%s %s %s." % (msg.nick, action, title)
        if text:
            response += u" %s" % (text)
        if flavor:
            response += u" %s" % (flavor)
            print response
        return response.encode('utf8')

    def _titlePrep(self, title):
        if title[0] in 'aeiou':
            prep = "an"
        else:
            prep = "a"
        return u"%s %s" % (prep, title)

Class = Magic


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
