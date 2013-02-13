import xbmcaddon
from langcodes import *

class settings():
    def __init__( self ):
      self.readPrefs()
      
    def readPrefs(self):
      addon = xbmcaddon.Addon()    
      self.logLevel = addon.getSetting('log_level')
      if self.logLevel and len(self.logLevel) > 0:
          self.logLevel = int(self.logLevel)
      else:
          self.logLevel = LOG_INFO
      self.service_enabled = addon.getSetting('enabled') == 'true'
      self.delay = int(addon.getSetting('delay'))
      self.audio_prefs_on = addon.getSetting('enableAudio') == 'true'
      self.sub_prefs_on = addon.getSetting('enableSub') == 'true'
      self.condsub_prefs_on = addon.getSetting('enableCondSub') == 'true'
      self.turn_subs_on = addon.getSetting('turnSubsOn') == 'true'
      self.turn_subs_off = addon.getSetting('turnSubsOff') == 'true'
      self.at_least_one_pref_on = self.audio_prefs_on or self.sub_prefs_on or self.condsub_prefs_on
      
      
      self.AudioPrefs = [
          (languageTranslate(addon.getSetting('AudioLang01'), 4, 0) , languageTranslate(addon.getSetting('AudioLang01'), 4, 3)),
          (languageTranslate(addon.getSetting('AudioLang02'), 4, 0) , languageTranslate(addon.getSetting('AudioLang02'), 4, 3)),
          (languageTranslate(addon.getSetting('AudioLang03'), 4, 0) , languageTranslate(addon.getSetting('AudioLang03'), 4, 3))
      ]
      self.SubtitlePrefs = [
          (languageTranslate(addon.getSetting('SubLang01'), 4, 0) , languageTranslate(addon.getSetting('AudioLang01'), 4, 3)),
          (languageTranslate(addon.getSetting('SubLang02'), 4, 0) , languageTranslate(addon.getSetting('AudioLang02'), 4, 3)),
          (languageTranslate(addon.getSetting('SubLang03'), 4, 0) , languageTranslate(addon.getSetting('AudioLang03'), 4, 3))
      ]
      self.CondSubtitlePrefs = [
          (
              languageTranslate(addon.getSetting('CondAudioLang01'), 4, 0) , languageTranslate(addon.getSetting('CondAudioLang01'), 4, 3),
              languageTranslate(addon.getSetting('CondSubLang01'), 4, 0) , languageTranslate(addon.getSetting('CondSubLang01'), 4, 3)
          ),
          (
              languageTranslate(addon.getSetting('CondAudioLang02'), 4, 0) , languageTranslate(addon.getSetting('CondAudioLang02'), 4, 3),
              languageTranslate(addon.getSetting('CondSubLang02'), 4, 0) , languageTranslate(addon.getSetting('CondSubLang02'), 4, 3)
          ),
          (
              languageTranslate(addon.getSetting('CondAudioLang03'), 4, 0) , languageTranslate(addon.getSetting('CondAudioLang03'), 4, 3),
              languageTranslate(addon.getSetting('CondSubLang03'), 4, 0) , languageTranslate(addon.getSetting('CondSubLang03'), 4, 3)
          )
      ]
