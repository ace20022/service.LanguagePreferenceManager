
#import rpdb2 
#rpdb2.start_embedded_debugger('pw')
import os, sys
import xbmc, xbmcaddon

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

from langcodes import *
from settings import *

settings = settings()

LOG_NONE = 0
LOG_ERROR = 1
LOG_INFO = 2
LOG_DEBUG = 3
    
def log(level, msg):
    if level <= settings.logLevel:
        if level == LOG_ERROR:
            l = xbmc.LOGERROR
        elif level == LOG_INFO:
            l = xbmc.LOGINFO
        elif level == LOG_DEBUG:
            l = xbmc.LOGDEBUG
        xbmc.log("[Language Preference Manager]: " + str(msg), l)


class LangPref_Monitor( xbmc.Monitor ):
  def __init__( self ):
    xbmc.Monitor.__init__( self )
        
  def onSettingsChanged( self ):
    settings.readPrefs()

class Main:
    def __init__( self ):
        self._init_vars()
        if ( not settings.service_enabled):
            log(LOG_INFO, "Service not enabled")
        self._daemon()

    def _init_vars( self ):
        self.Monitor = LangPref_Monitor()
        self.Player = LangPrefMan_Player()

    def _daemon( self ):
        while (not xbmc.abortRequested):
            xbmc.sleep(500)
            

class LangPrefMan_Player(xbmc.Player) :
    
    def __init__ (self):
        xbmc.Player.__init__(self)
        
    def onPlayBackStarted(self):
        if settings.service_enabled and settings.at_least_one_pref_on and self.isPlayingVideo():
            log(LOG_DEBUG, 'Playback started')
            self.audio_changed = False
            # switching an audio track to early leads to a reopen -> start at the beginning
            if settings.delay > 0:
                log(LOG_DEBUG, "Delaying preferences evaluation by {0} ms".format(settings.delay))
                xbmc.sleep(settings.delay)
            log(LOG_DEBUG, 'Getting video properties')
            self.getDetails()
            self.evalPrefs()

    def evalPrefs(self):
        if settings.audio_prefs_on:
            trackIndex = self.evalAudioPrefs()
            if trackIndex == -2:
                log(LOG_INFO, 'Audio: None of the preferred languages is available' )
            elif trackIndex >= 0:
                self.setAudioStream(trackIndex)
                self.audio_changed = True
            
        if settings.sub_prefs_on:
            trackIndex = self.evalSubPrefs()
            if trackIndex == -2:
                log(LOG_INFO, 'Subtitle: None of the preferred languages is available' )
                if settings.turn_subs_off:
                    log(LOG_DEBUG, 'Subtitle: disabling subs' )
                    self.showSubtitles(False)
            elif trackIndex >= 0:
                self.setSubtitleStream(trackIndex)
                if setings.turn_subs_on:
                    log(LOG_DEBUG, 'Subtitle: enabling subs' )
                    self.showSubtitles(True)
                
        if settings.condsub_prefs_on:
            trackIndex = self.evalCondSubPrefs()
            if trackIndex == -2:
                log(LOG_INFO, 'Conditional subtitle: None of the preferrences is available' )
                if settings.turn_subs_off:
                    log(LOG_DEBUG, 'Subtitle: disabling subs' )
                    self.showSubtitles(False)
            elif trackIndex >= 0:
                self.setSubtitleStream(trackIndex)
                if settings.turn_subs_on:
                    log(LOG_DEBUG, 'Subtitle: enabling subs' )
                    self.showSubtitles(True)
                
    def evalAudioPrefs(self):
        log(LOG_DEBUG, 'Evaluating audio preferences' )
        i = 0
        for pref in settings.AudioPrefs:
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
                
    def evalSubPrefs(self):
        log(LOG_DEBUG, 'Evaluating subtitle preferences' )
        i = 0
        for pref in settings.SubtitlePrefs:
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

    def evalCondSubPrefs(self):
        log(LOG_DEBUG, 'Evaluating conditional subtitle preferences' )
        # if the audio track has been changed wait some time
        if (self.audio_changed and settings.delay > 0):
            log(LOG_DEBUG, "Delaying preferences evaluation by {0} ms".format(4*settings.delay))
            xbmc.sleep(4*settings.delay)
        log(LOG_DEBUG, 'Getting video properties')
        self.getDetails()
        i = 0
        for pref in settings.CondSubtitlePrefs:
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

if ( __name__ == "__main__" ):
    log(LOG_INFO, 'service {0} version {1} started'.format(__addonname__, __addonversion__))
    main = Main()
    log(LOG_INFO, 'service {0} version {1} stopped'.format(__addonname__, __addonversion__))
