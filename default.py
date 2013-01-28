
import rpdb2 
rpdb2.start_embedded_debugger('pw')
import os, sys, threading, time, imp
import xbmc, xbmcaddon, xbmcgui

if sys.version_info < (2, 7):
    import simplejson
else:
    import json as simplejson

__addon__ = xbmcaddon.Addon()
__addonversion__ = __addon__.getAddonInfo('version')
__addonid__ = __addon__.getAddonInfo('id')
__addonname__ = __addon__.getAddonInfo('name')
__addonPath__ = __addon__.getAddonInfo('path')
__addonResourcePath__ = xbmc.translatePath(os.path.join(__addonPath__, 'resources', 'lib'))
__addonIconFile__ = xbmc.translatePath(os.path.join(__addonPath__, 'icon.png'))
sys.path.append(__addonResourcePath__)

from langcodes import languageTranslate

LOG_NONE = 0
LOG_ERROR = 1
LOG_INFO = 2
LOG_DEBUG = 3

logLevel = __addon__.getSetting('log_level')
if logLevel and len(logLevel) > 0:
    logLevel = int(logLevel)
else:
    logLevel = LOG_INFO
    
    
def log(level, msg):
    if level <= logLevel:
        if level == LOG_ERROR:
            l = xbmc.LOGERROR
        elif level == LOG_INFO:
            l = xbmc.LOGINFO
        elif level == LOG_DEBUG:
            l = xbmc.LOGDEBUG
        xbmc.log("[Language Preference Manager]: " + str(msg), l)

class Main:
    def __init__( self ):
        self._init_vars()
        if __addon__.getSetting('enabled') != 'true':
            log(LOG_INFO, "Service not enabled")
        self._daemon()

    def _init_vars( self ):
         self.Player = LangPrefMan_Player()

    def _daemon( self ):
        while (not xbmc.abortRequested):
            xbmc.sleep(500)
            

class LangPrefMan_Player(xbmc.Player) :
    
    def __init__ (self):
        xbmc.Player.__init__(self)
        
    def onPlayBackStarted(self):
        if __addon__.getSetting('enabled') == 'true' and self.isPlayingVideo():
            log(LOG_DEBUG, 'Playback started')
            PAUSE = 0
            if __addon__.getSetting('pause') == 'true':
                log(LOG_DEBUG, "Pausing player while evaluating language preferences")
                self.pause()
                xbmc.sleep(100)
                PAUSE = 1
            xbmc.sleep(100)
            log(LOG_DEBUG, 'Reading preferences')
            self.readPrefs()
            self.getDetails()
            self.evalPrefs()
            
            if PAUSE == 1:
                self.pause()

    def evalPrefs(self):
        if __addon__.getSetting('enableAudio') == 'true':
            trackIndex = self.evalAudioPrefs()
            if trackIndex == -2:
                log(LOG_INFO, 'Audio: None of the preferred languages is available' )
            elif trackIndex >= 0:
                #xbmc.sleep(200)
                self.switchAudioTrack(trackIndex)
            
        if __addon__.getSetting('enableSub') == 'true':
            trackIndex = self.evalSubPrefs()
            if trackIndex == -2:
                log(LOG_INFO, 'Subtitle: None of the preferred languages is available' )
            elif trackIndex >= 0:
                #xbmc.sleep(200)
                self.switchSubtitleTrack(trackIndex)
                
        if __addon__.getSetting('enableCondSub') == 'true':
            trackIndex = self.evalCondSubPrefs()
            if trackIndex == -2:
                log(LOG_INFO, 'Conditional subtitle: None of the preferrences is available' )
            elif trackIndex >= 0:
                #xbmc.sleep(200)
                self.switchSubtitleTrack(trackIndex)
                
    def evalAudioPrefs(self):
        log(LOG_DEBUG, 'Evaluating audio preferences' )
        i = 0
        for pref in self.AudioPrefs:
            i += 1
            name, code = pref
            if (self.selected_audio_stream and
                self.selected_audio_stream.has_key('language') and
                (code == self.selected_audio_stream['language'] or name == self.selected_audio_stream['language'])):
                    log(LOG_INFO, 'Selected audio language matches preference {0} ({1})'.format(i, name) )
                    return -1
            else:
                for stream in self.audiostreams:
                    if ((code == stream['language']) or (name == stream['language'])):
                        log(LOG_INFO, 'Audio language of stream {0} matches preference {1} ({2})'.format(stream['index'], i, name) )
                        return stream['index']
                log(LOG_INFO, 'Audio: preference {0} ({1}) not available'.format(i, name) )
        return -2
                
    def switchAudioTrack(self, trackIndex):
        query_string = '{{"jsonrpc": "2.0", "method": "Player.SetAudioStream", "params":{{"playerid": 1,  "stream": {0} }},"id": 1}}'.format(trackIndex)
        log(LOG_DEBUG, query_string)
        json_query = xbmc.executeJSONRPC(query_string)
        json_query = unicode(json_query, 'utf-8', errors='ignore')
        json_response = simplejson.loads(json_query)
        if json_response.has_key('result') and json_response['result'] != None:
            if json_response['result'] == 'OK':
                log(LOG_INFO, 'Audio language succesfully set' )
        else:
            log(LOG_DEBUG, 'Error: ' +  json_response)
            
    def evalSubPrefs(self):
        log(LOG_DEBUG, 'Evaluating subtitle preferences' )
        i = 0
        for pref in self.SubtitlePrefs:
            i += 1
            name, code = pref
            if (self.selected_sub and
                self.selected_sub.has_key('language') and
                (code == self.selected_sub['language'] or name == self.selected_sub['language'])):
                    log(LOG_INFO, 'Selected subtitle language matches preference {0} ({1})'.format(i, name) )
                    return -1
            else:
                for sub in self.subtitles:
                    if ((code == sub['language']) or (name == sub['language'])):
                        log(LOG_INFO, 'Subtitle language of subtitle {0} matches preference {1} ({2})'.format(sub['index'], i, name) )
                        return sub['index']
                log(LOG_INFO, 'Subtitle: preference {0} ({1}) not available'.format(i, name) )
        return -2

    def switchSubtitleTrack(self, trackIndex):
        query_string = '{{"jsonrpc": "2.0", "method": "Player.SetSubtitle", "params":{{"playerid": 1,  "subtitle": {0} }},"id": 1}}'.format(trackIndex)
        log(LOG_DEBUG, query_string)
        json_query = xbmc.executeJSONRPC(query_string)
        json_query = unicode(json_query, 'utf-8', errors='ignore')
        json_response = simplejson.loads(json_query)
        if json_response.has_key('result') and json_response['result'] != None:
            if json_response['result'] == 'OK':
                log(LOG_INFO, 'Subtitle language succesfully set' )
        else:
            log(LOG_DEBUG, 'Error ' +  json_response)
        
    def evalCondSubPrefs(self):
        log(LOG_DEBUG, 'Evaluating conditional subtitle preferences' )
        i = 0
        for pref in self.CondSubtitlePrefs:
            i += 1
            audio_name, audio_code, sub_name, sub_code = pref
            if (self.selected_audio_stream and
                self.selected_audio_stream.has_key('language') and
                (audio_code == self.selected_audio_stream['language'] or audio_name == self.selected_audio_stream['language'])):
                    log(LOG_INFO, 'Selected audio language matches conditional preference {0} ({1}:{2})'.format(i, audio_name, sub_name) )
                    for sub in self.subtitles:
                        if ((sub_code == sub['language']) or (sub_name == sub['language'])):
                            log(LOG_INFO, 'Language of subtitle {0} matches conditional preference {1} ({2}:{3})'.format(sub['index'], i, audio_name, sub_name) )
                            return sub['index']
                        else:
                            log(LOG_INFO, 'Conditional subtitle: no match found for preference {0} ({1}:{2})'.format(i, audio_name, sub_name) )
        return -2

    
    def getDetails(self):
        query_string = '{"jsonrpc": "2.0", "method": "Player.GetProperties", "params":' \
            '{ "properties": ["currentaudiostream", "audiostreams", "subtitleenabled", "currentsubtitle", "subtitles" ], "playerid": 1 },' \
            '"id": 1}'
        json_query = xbmc.executeJSONRPC(query_string)
        json_query = unicode(json_query, 'utf-8', errors='ignore')
        json_response = simplejson.loads(json_query)
        
        if json_response.has_key('result') and json_response['result'] != None:
            self.selected_audio_stream = json_response['result']['currentaudiostream']
            self.selected_sub = json_response['result']['currentsubtitle']
            self.selected_sub_enabled = json_response['result']['subtitleenabled']
            self.audiostreams = json_response['result']['audiostreams']
            self.subtitles = json_response['result']['subtitles']
        log(LOG_DEBUG, json_response )
    
    def readPrefs(self):
        self.AudioPrefs = [
            (languageTranslate(__addon__.getSetting('AudioLang01'), 4, 0) , languageTranslate(__addon__.getSetting('AudioLang01'), 4, 3)),
            (languageTranslate(__addon__.getSetting('AudioLang02'), 4, 0) , languageTranslate(__addon__.getSetting('AudioLang02'), 4, 3)),
            (languageTranslate(__addon__.getSetting('AudioLang03'), 4, 0) , languageTranslate(__addon__.getSetting('AudioLang03'), 4, 3))
        ]
        self.SubtitlePrefs = [
            (languageTranslate(__addon__.getSetting('SubLang01'), 4, 0) , languageTranslate(__addon__.getSetting('AudioLang01'), 4, 3)),
            (languageTranslate(__addon__.getSetting('SubLang02'), 4, 0) , languageTranslate(__addon__.getSetting('AudioLang02'), 4, 3)),
            (languageTranslate(__addon__.getSetting('SubLang03'), 4, 0) , languageTranslate(__addon__.getSetting('AudioLang03'), 4, 3))
        ]
        self.CondSubtitlePrefs = [
            (
                languageTranslate(__addon__.getSetting('CondAudioLang01'), 4, 0) , languageTranslate(__addon__.getSetting('CondAudioLang01'), 4, 3),
                languageTranslate(__addon__.getSetting('CondSubLang01'), 4, 0) , languageTranslate(__addon__.getSetting('CondSubLang01'), 4, 3)
            ),
            (
                languageTranslate(__addon__.getSetting('CondAudioLang02'), 4, 0) , languageTranslate(__addon__.getSetting('CondAudioLang02'), 4, 3),
                languageTranslate(__addon__.getSetting('CondSubLang02'), 4, 0) , languageTranslate(__addon__.getSetting('CondSubLang02'), 4, 3)
            ),
            (
                languageTranslate(__addon__.getSetting('CondAudioLang03'), 4, 0) , languageTranslate(__addon__.getSetting('CondAudioLang03'), 4, 3),
                languageTranslate(__addon__.getSetting('CondSubLang03'), 4, 0) , languageTranslate(__addon__.getSetting('CondSubLang03'), 4, 3)
            )
        ]
        

if ( __name__ == "__main__" ):
    log(LOG_INFO, 'service {0} version {1} started'.format(__addonname__, __addonversion__))
    main = Main()
    log(LOG_INFO, 'service {0} version {1} stopped'.format(__addonname__, __addonversion__))
