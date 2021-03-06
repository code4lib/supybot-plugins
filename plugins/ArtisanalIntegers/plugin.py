###
# Copyright (c) 2012, Mark A. Matienzo
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

from urllib import urlencode
import urllib2
import simplejson

HEADERS = {'User-Agent': 'Zoia/1.0 (Supybot/0.83; ArtisanalIntegers Plugin; http://code4lib.org/irc)'}
BROOKLYNT_URL = "http://api.brooklynintegers.com/rest/"
MISSIONINT_URL = "http://www.missionintegers.com/next-int"

class ArtisanalIntegers(callbacks.Plugin):

    def brooklynt(self, irc, msg, args, option):
        """(brooklynt [raw]): Request a new hand-crafted artisanal integer from http://brooklynintegers.com"""
        params = {'method': 'brooklyn.integers.create'}
        data = urlencode(params)
        request = urllib2.Request(BROOKLYNT_URL, data, HEADERS)
        response = simplejson.load(urllib2.urlopen(request))
        if option == "raw":
            result = response['integer']
        else:
            result = "Your hand-crafted integer is %s - %s " % (response['integer'], response['shorturl'])

        irc.reply(result)

    brooklynt = wrap(brooklynt, [optional('text')])

    brooklyninteger = brooklynt

    def missionint(self, irc, msg, args, option):
        """(missionint [raw]): Request a new hella artisanal integer from http://missionintegers.com"""
        params = {'format': 'json'}
        # todo: handle count parameter to get multiple hella artisanal ints
        data = urlencode(params)
        request = urllib2.Request(MISSIONINT_URL, data, HEADERS)
        response = simplejson.load(urllib2.urlopen(request))
        result = ''.join([unicode(r) for r in response])
        if option != "raw":
            result = "Your West Coast hand-crafted integer(s) is/are " + result
        irc.reply(result)

    missionint = wrap(missionint, [optional('text')])

    missioninteger = missionint

Class = ArtisanalIntegers


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
