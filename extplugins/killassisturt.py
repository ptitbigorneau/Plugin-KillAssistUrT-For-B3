# KillAssistUrT Plugin

__author__  = 'ptitbigorneau'
__version__ = '1.1.2'

import b3
import time
import b3.events
import b3.plugin

class KillassisturtPlugin(b3.plugin.Plugin):

    _adminPlugin = None
    _listdamages = []
    _listassits = []
    _pluginactived = "on"
    _assistlevel = 1
    _adminlevel = 100
    _assistdelay = 10

    def onStartup(self):
        
        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:
            self.error('Could not find admin plugin')
            return False

        self.registerEvent(b3.events.EVT_CLIENT_KILL)
        self.registerEvent(b3.events.EVT_CLIENT_KILL_TEAM)
        self.registerEvent(b3.events.EVT_CLIENT_SUICIDE)
        self.registerEvent(b3.events.EVT_CLIENT_DAMAGE)
        self.registerEvent(b3.events.EVT_CLIENT_DAMAGE_TEAM)
        self.registerEvent(b3.events.EVT_GAME_ROUND_START)
        self.registerEvent(b3.events.EVT_GAME_ROUND_END)
        self.registerEvent(b3.events.EVT_GAME_EXIT)        
        self.registerEvent(b3.events.EVT_GAME_MAP_CHANGE)
        self.registerEvent(b3.events.EVT_CLIENT_DISCONNECT)
        self.registerEvent(b3.events.EVT_CLIENT_TEAM_CHANGE)

        self._adminPlugin.registerCommand(self, 'assist',self._assistlevel, self.cmd_assist)
        self._adminPlugin.registerCommand(self, 'killassisturt',self._adminlevel, self.cmd_killassisturt)
        self._adminPlugin.registerCommand(self, 'killassistdelay',self._adminlevel, self.cmd_killassistdelay, 'kadelay')

    def onLoadConfig(self):

        try:
            self._pluginactived = self.config.get('settings', 'pluginactived')
        except Exception, err:
            self.warning("Using default value %s for pluginactived. %s" % (self._pluginactived, err))
        self.debug('pluginactived : %s' % self._pluginactived)

        try:
            self._assistlevel = self.config.getint('settings', 'assistlevel')
        except Exception, err:
            self.warning("Using default value %s for assistlevel. %s" % (self._assistlevel, err))
        self.debug('assistlevel : %s' % self._assistlevel)

        try:
            self._assistdelay = self.config.getint('settings', 'assistdelay')
        except Exception, err:
            self.warning("Using default value %s for assistdelay. %s" % (self._assistdelay, err))
        self.debug('assistdelay : %s' % self._assistdelay)

        try:
            self._adminlevel = self.config.getint('settings', 'adminlevel')
        except Exception, err:
            self.warning("Using default value %s for adminlevel. %s" % (self._adminlevel, err))
        self.debug('adminlevel : %s' % self._adminlevel)
 
    def onEvent(self, event):
        
        if self._pluginactived == 'off':

           return False

        if self._pluginactived == 'on':
        
            if event.type == b3.events.EVT_GAME_ROUND_START:

                self._listdamages = []

            if event.type == b3.events.EVT_GAME_ROUND_END or event.type == b3.events.EVT_GAME_EXIT or event.type == b3.events.EVT_GAME_MAP_CHANGE:
        
                assist = 0

                for c in self._listassits:

                    datadamage = c.split(' ')
                    lnbassists = datadamage[1]
                
                    if int(lnbassists)>= assist:
                    
                        assist = int(lnbassists)

                for y in self._listassits:

                    datadamage = y.split(' ')
                    lclient = datadamage[0]
                    lnbassists = datadamage[1]
                    asclient = None

                    for z in self.console.clients.getList():

                        if int(lclient) == int(z.cid):

                            asclient = z
                            asclient.message('^5Total Assist : ^2%s ^3assist(s)'%(lnbassists))                              

                    if int(lnbassists) == assist and asclient != None:
                    
                        topclient = asclient
                        assist = int(lnbassists)
                        self.console.say('^5Top Assists ^3: %s ^3with ^1%s ^3assist(s)'%(topclient.exactName, assist))
                
                self._listassits = []

            if event.type == b3.events.EVT_CLIENT_DAMAGE or event.type == b3.events.EVT_CLIENT_DAMAGE_TEAM: 

                aclient = event.client
                vclient = event.target
                damage = event.data[0]
                
                test = None
     
                for x in self._listdamages:

                    datadamage = x.split(' ')
                    lclient = datadamage[0]
                    lattacker1 = datadamage[1]
                    lattacker2 = datadamage[2] 
                    lassisttemp1 = datadamage[3]
                    lassisttemp2 = datadamage[4]

                    if int(lclient) == int(vclient.cid):
                    
                        test = 'ok'
                        self._listdamages.remove(x) 
                    
                        if int(aclient.cid) == int(lattacker2):

                            attacker1 = lattacker1
                            attacker2 = aclient.cid
                            assisttemp2 = time.time()
                            
                            if int(aclient.cid) == int(lattacker1):
                                assisttemp1 = time.time()
                                
                            else:
                                assisttemp1 = lassisttemp1

                        if int(aclient.cid) != int(lattacker2):
                        
                            attacker1 = lattacker2
                            attacker2 = aclient.cid
                            assisttemp1 = lassisttemp2
                            assisttemp2 = time.time()

                if test == None:

                    attacker1 = aclient.cid
                    attacker2 = aclient.cid
                    assisttemp1 = time.time()
                    assisttemp2 = time.time()                

                self._listdamages.append('%s %s %s %s %s'%(int(vclient.cid), int(attacker1), int(attacker2), int(assisttemp1), int(assisttemp2)))

            if event.type == b3.events.EVT_CLIENT_KILL: 
            
                aclient = event.client
                vclient = event.target
                gametype = self.console.getCvar('g_gametype').getInt()

                for x in self._listdamages:

                    datadamage = x.split(' ')
                    lclient = datadamage[0]
                    lattacker1 = datadamage[1]
                    lattacker2 = datadamage[2]
                    lassisttemp1 = datadamage[3]
                    asclient = None

                    if int(lattacker1) == 999:

                        self._listdamages.remove(x)
                        return

                    for v in self.console.clients.getList():

                        if int(lattacker1) == int(v.cid):

                            asclient = v
                                  
                    if int(lclient) == int(vclient.cid):
                    
                        if int(aclient.cid) != int(lattacker1):

                            if asclient ==  None:
                            
                                self._listdamages.remove(x)
                                return

                            assisttemp2 = time.time()

                            difftime = assisttemp2 - int(lassisttemp1)

                            assisttime = round(difftime)
                            assisttime = str(assisttime)
                            assisttime = assisttime.replace('.0', '')

                            if difftime > self._assistdelay:
                                
                                self._listdamages.remove(x)
                                return

                            if gametype != 0:
                        
                                if asclient.team == vclient.team:

                                    assist = -1
                                    assistmessage1 = '^1-1^7 Assist Penalty Team Damage for the death of^7 '
                                    assistmessage2 = '^1Penalty Team Damage -1 Assist ^3for the death of^7 '
                        
                                else:

                                    assist = 1
                                    assistmessage1 = '^2+1^7 Assist for the death of^7 '
                                    assistmessage2 = '^2+1 Assist ^3for the death of^7 '

                            else:

                                assist = 1
                                assistmessage1 = '+1 Assist for the death of^7 '
                                assistmessage2 = '^2+1 Assist ^3for the death of^7 '

                            test = None
                         
                            for y in self._listassits:

                                datadamage = y.split(' ')
                                lclient = datadamage[0]
                                lnbassists = datadamage[1]
                 
                                if int(lclient) == int(asclient.cid):
                    
                                    test = 'ok'
                                    self._listassits.remove(y)
                                    nbassists = int(lnbassists) + assist                          

                            if test == None:

                                nbassists = assist

                            self._listassits.append('%s %s'%(int(asclient.cid), int(nbassists)))

                            self.console.write('%s %s %s '%(asclient.exactName, assistmessage1, vclient.exactName))
                            asclient.message('%s %s '%(assistmessage2, vclient.exactName))
                            asclient.message('^5Total Assist : ^2%s ^3assist(s)'%(nbassists))  
                    
                        self._listdamages.remove(x)

                if event.type == b3.events.EVT_CLIENT_KILL_TEAM: 
            
                    aclient = event.client
                    vclient = event.target
            
                for x in self._listdamages:

                    datadamage = x.split(' ')
                    lclient = datadamage[0]

                    if int(lclient) == int(vclient.cid):
                    
                        self._listdamages.remove(x)

            if event.type == b3.events.EVT_CLIENT_SUICIDE: 

                client = event.client
            
                for x in self._listdamages:

                    datadamage = x.split(' ')
                    lclient = datadamage[0]

                    if int(lclient) == int(vclient.cid):
                    
                        self._listdamages.remove(x)

            if event.type == b3.events.EVT_CLIENT_TEAM_CHANGE: 
            
                client = event.client
                          
                for x in self._listdamages:

                    datadamage = x.split(' ')
                    lclient = datadamage[0]

                    if int(lclient) == int(client.cid):
                    
                        self._listdamages.remove(x)

            if event.type == b3.events.EVT_CLIENT_DISCONNECT: 
            
                cidclient = event.data

                for x in self._listdamages:

                    xdata = x.split(' ')
                    xclient = xdata[0]
                    xattacker1 = xdata[1]
                    xattacker2 = xdata[2] 
                    xassisttemp1 = xdata[3]
                    xassisttemp2 = xdata[4]
                    
                    if int(cidclient) == int(xdata[0]):
                       
                        self._listdamages.remove(x)

                    if int(cidclient) == int(xattacker1) and int(cidclient) == int(xattacker2):

                        self._listdamages.remove(x)

                    if int(cidclient) == int(xattacker1) and int(cidclient) != int(xattacker2):

                        self._listdamages.remove(x)
                        
                        self._listdamages.append('%s %s %s %s %s'%(int(vclient.cid), 999, int(attacker2), 999, int(assisttemp2)))

                    if int(cidclient) == int(xattacker2) and int(cidclient) != int(xattacker1):

                        self._listdamages.remove(x)
                        
                        self._listdamages.append('%s %s %s %s %s'%(int(vclient.cid), int(attacker1), 999, int(assisttemp1), 999))

                for y in self._listassits:

                    ydata = y.split(' ')
                   
                    if int(cidclient) == int(ydata[0]):
                       
                        self._listassits.remove(y)

    def cmd_assist(self, data, client, cmd=None):
        
        """\
        Nombre assists
        """
        if self._pluginactived == 'off':

           client.message('^1Plugin KillAssistUrT deactivated')
           return False

        testclient = None

        if data:
            
            input = self._adminPlugin.parseUserCmd(data)
            sclient = self._adminPlugin.findClientPrompt(input[0], client)
            testclient = 'data'

        else:
            
            sclient = client
            testclient = 'nodata'

        test = None
        
        if sclient:

            for y in self._listassits:

                datadamage = y.split(' ')
                lclient = datadamage[0]
                lnbassists = datadamage[1]
                
                if int(lclient) == int(sclient.cid):
                    
                    test = 'ok'
                    
                    if testclient == 'nodata':
                        client.message('^5Total Assist : ^2%s ^3assist(s)'%(lnbassists))

                    if testclient == 'data':
                        client.message('%s ^5Total Assist : ^2%s ^3assist(s)'%(sclient.exactName, lnbassists)) 

            if test == None:

                if testclient == 'nodata':            
                    client.message('^1You have not Assist')

                if testclient == 'data':            
                    client.message('%s^1 has not Assist'%(sclient.exactName))

        else:
            
            client.message('!assist or !assist <player name>')

    def cmd_killassisturt(self, data, client, cmd=None):
        
        """\
        activate / deactivate killassisturt 
        """
        
        if data:
            
            input = self._adminPlugin.parseUserCmd(data)
        
        else:
        
            if self._pluginactived == 'on':

                client.message('killassisturt ^2activated')

            if self._pluginactived == 'off':

                client.message('killassisturt ^1deactivated')

            client.message('!killassisturt <on / off>')
            return

        if input[0] == 'on':

            if self._pluginactived != 'on':

                self._pluginactived = 'on'
                message = '^2activated'

            else:

                client.message('killassisturt is already ^2activated') 

                return False

        if input[0] == 'off':

            if self._pluginactived != 'off':

                self._pluginactived = 'off'
                message = '^1deactivated'

            else:
                
                client.message('killassisturt is already ^1disabled')                

                return False

        client.message('killassisturt %s'%(message))

    def cmd_killassistdelay(self, data, client, cmd=None):
        
        """\
        killassisturt delay
        """
        
        if data:
            
            input = self._adminPlugin.parseUserCmd(data)
        
        else:
        

            client.message('killassisturt delay : %s '%(self._assistdelay))

            client.message('!killassistdelay <seconds>')
            return

        if not input[0].isdigit():

            client.message('!killassistdelay <seconds>')
            return

        if input[0].isdigit():

            self._assistdelay = int(input[0])
            client.message('killassistdelay : %s seconds'%(self._assistdelay))
            