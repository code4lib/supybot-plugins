###
# Copyright (c) 2013, Chad B Nelson
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

import supybot.conf as conf
import supybot.utils as utils
import supybot.ircdb as ircdb
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import supybot.dbi as dbi


class NotMe(callbacks.Plugin):
    """
    A way for channel users to opt out of being named in plugins like who and cast.
    """

    class DB(plugins.DbiChannelDB):
        class DB(dbi.DB):
            class Record(dbi.Record):
                __fields__ = [
                    'op'
                ]
            def add(self, op, **kwargs):
                record = self.Record(op=op, **kwargs)
                return super(self.__class__, self).add(record)
                
    def __init__(self, irc):
        self.__parent = super(NotMe, self)
        self.__parent.__init__(irc)
        self.db = plugins.DB(self.name(), {'flat': self.DB})()

    def _ops(self, channel):
    	result = [r.op for r in self.db.select(channel, lambda x: True)]
    	result.sort()
    	return result

    def _calledByOwner(self, irc, msg, args):
        try:
            u = ircdb.users.getUser(msg.prefix)
        except KeyError:
            irc.errorNotRegistered()
        else:
            if u._checkCapability('owner'):
                return True
            else:
                irc.error(conf.supybot.replies.noCapability() % ('owner'), Raise=True)
        return False

    def notme(self, irc, msg, args, channel):
        """
        Disallow the caller from having fun in channel"""
        if self._calledByOwner(irc, msg, args):
        	if msg.nick in self._ops(channel):
        		irc.error("%s has already opted out of the fun in %s" % (msg.nick, channel), prefixNick=False)
        	else:
        		self.db.add(channel, msg.nick)
        		irc.reply("The operation succeeded. %s has opted out of the fun in %s" % (msg.nick, channel), prefixNick=False)
    notme = wrap(notme, ['channeldb'])

    def remove(self, irc, msg, args, channel, op):
        """<op>
       Let the user have fun in channel again. Woohoo!"""
        if self._calledByOwner(irc, msg, args):
            ids = [r.id for r in self.db.select(channel, lambda r: r.op == op)]
            if len(ids) == 0:
            	irc.error("%s is already a part of the fun in  %s" % (op, channel), prefixNick=False)
            else:
            	for i in ids:
            		self.db.remove(channel, i)
            	irc.reply("The operation suceeded. Welcome %s back to the fun in %s " % (op, channel ), prefixNick=False)
    remove = wrap(remove, ['channeldb', 'nick'])

    def list(self, irc, msg, args, opts, channel):
        """[--all]
        List channel members who like to have decided not to participate in the fun!"""
    	ops = self._ops(channel)
    	if len(ops) == 0:
    		irc.reply("No one has opted out of the fun on  %s" % channel)
    	else:
	    	current = True
	    	for opt,arg in opts:
	    		if opt == 'all':
	    			current = False

	    	if current:	
	    		prefix = 'List of %s fun haters (@help notme for details)' % channel
	    		users = irc.state.channels[channel].users
	    		ops = [op for op in ops if op in users]
	    	else:
	    		prefix = 'List of %s helpers (@help helpers for details)' % channel

	    	if len(ops) == 0:
	    		irc.reply("No fun haters arein %s. Try again with --all to see all registered fun haters." % channel)
	    	else:
	    		irc.reply("%s: %s" % (prefix, ", ".join(ops)), prefixNick=False)

    list = wrap(list, [getopts({'all':''}),'channeldb'])

Class = NotMe 


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
