import xbmc, xbmcaddon
import re
from langcodes import *

LOG_NONE = 0
LOG_ERROR = 1
LOG_INFO = 2
LOG_DEBUG = 3
    


class settings():

    def log(self, level, msg):
        if level <= self.logLevel:
            if level == LOG_ERROR:
                l = xbmc.LOGERROR
            elif level == LOG_INFO:
                l = xbmc.LOGINFO
            elif level == LOG_DEBUG:
                l = xbmc.LOGDEBUG
            xbmc.log("[Language Preference Manager]: " + str(msg), l)

    def init(self):
        addon = xbmcaddon.Addon()
        self.logLevel = addon.getSetting('log_level')
        if self.logLevel and len(self.logLevel) > 0:
            self.logLevel = int(self.logLevel)
        else:
            self.logLevel = LOG_INFO
            
        self.custom_prefs_delim = r'>'
        self.custom_condSub_delim = r':'
        self.custom_audio = []
        self.custom_subs = []
        self.custom_condsub = []

        self.service_enabled = addon.getSetting('enabled') == 'true'
    
    def __init__( self ):
        self.init()
        
        #self.readSettings()

    def readSettings(self):
        self.readPrefs()
        self.readCustomPrefs()
        self.log(LOG_DEBUG,
                 '\n##### LPM Settings #####\n' \
                 'delay: {0}ms\n' \
                 'audio on: {1}\n' \
                 'subs on: {2}\n' \
                 'cond subs on: {3}\n' \
                 'turn subs on: {4}, turn subs off: {5}\n' \
                 'use file name: {6}, file name regex: {7}\n' \
                 'at least one pref on: {8}\n'\
                 'audio prefs: {9}\n' \
                 'sub prefs: {10}\n' \
                 'cond sub prefs: {11}\n' \
                 'custom audio prefs: {12}\n' \
                 'custom subs prefs: {13}\n'
                 'custom cond subs prefs: {14}\n'
                 '##### LPM Settings #####\n'
                 .format(self.delay, self.audio_prefs_on, self.sub_prefs_on,
                         self.condsub_prefs_on, self.turn_subs_on, self.turn_subs_off,
                         self.useFilename, self.filenameRegex, self.at_least_one_pref_on,
                         self.AudioPrefs, self.SubtitlePrefs, self.CondSubtitlePrefs,
                         self.custom_audio, self.custom_subs, self.custom_condsub)
                 )
      
    def readPrefs(self):
      addon = xbmcaddon.Addon()    

      self.service_enabled = addon.getSetting('enabled') == 'true'
      self.delay = int(addon.getSetting('delay'))
      self.audio_prefs_on = addon.getSetting('enableAudio') == 'true'
      self.sub_prefs_on = addon.getSetting('enableSub') == 'true'
      self.condsub_prefs_on = addon.getSetting('enableCondSub') == 'true'
      self.turn_subs_on = addon.getSetting('turnSubsOn') == 'true'
      self.turn_subs_off = addon.getSetting('turnSubsOff') == 'true'
      self.useFilename = addon.getSetting('useFilename') == 'true'
      self.filenameRegex = addon.getSetting('filenameRegex')
      if self.useFilename:
          self.reg = re.compile(self.filenameRegex, re.IGNORECASE)
          self.split = re.compile(r'[_|.|-]*', re.IGNORECASE)

      self.at_least_one_pref_on = self.audio_prefs_on or self.sub_prefs_on or self.condsub_prefs_on or self.useFilename
      
      self.AudioPrefs = [
          (languageTranslate(addon.getSetting('AudioLang01'), 4, 0) , languageTranslate(addon.getSetting('AudioLang01'), 4, 3)),
          (languageTranslate(addon.getSetting('AudioLang02'), 4, 0) , languageTranslate(addon.getSetting('AudioLang02'), 4, 3)),
          (languageTranslate(addon.getSetting('AudioLang03'), 4, 0) , languageTranslate(addon.getSetting('AudioLang03'), 4, 3))
      ]
      self.SubtitlePrefs = [
          (languageTranslate(addon.getSetting('SubLang01'), 4, 0) , languageTranslate(addon.getSetting('SubLang01'), 4, 3)),
          (languageTranslate(addon.getSetting('SubLang02'), 4, 0) , languageTranslate(addon.getSetting('SubLang02'), 4, 3)),
          (languageTranslate(addon.getSetting('SubLang03'), 4, 0) , languageTranslate(addon.getSetting('SubLang03'), 4, 3))
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

    def readCustomPrefs(self):
        self.custom_audio = []
        self.custom_subs = []
        self.custom_condsub = []

        self.readCustomAudio()
        self.readCustomSub()
        self.readCustomCondSub()



    def readCustomAudio(self):
        self.custom_audio_prefs_on = False
        addon = xbmcaddon.Addon()
        if (addon.getSetting('CustomAudio').find(self.custom_prefs_delim) > 0):
            for pref in addon.getSetting('CustomAudio').split(self.custom_prefs_delim):
                temp_pref = (languageTranslate(pref, 3, 0), pref)
                if temp_pref[0]:
                    self.custom_audio.append(temp_pref)
                else:
                    self.log(LOG_INFO, 'Custom audio prefs: lang code {0} not found in db! Please report this'.format(pref))
                
        elif len(addon.getSetting('CustomAudio')) > 0:
            self.log(LOG_INFO, 'Custom audio prefs parse error: {0}'.format(addon.getSetting('CustomAudio')))
            
        if len(self.custom_audio) > 0:
            self.custom_audio_prefs_on = True            
            #self.log(LOG_DEBUG, 'Custom audio prefs: {0}'.format(self.custom_audio))
        


    def readCustomSub(self):
        self.custom_sub_prefs_on = False
        addon = xbmcaddon.Addon()
        if (addon.getSetting('CustomSub').find(self.custom_prefs_delim) > 0):
            for pref in addon.getSetting('CustomSub').split(self.custom_prefs_delim):
                temp_pref = (languageTranslate(pref, 3, 0), pref)
                if temp_pref[0]:
                    self.custom_subs.append(temp_pref)
                else:
                    self.log(LOG_INFO, 'Custom sub prefs: lang code {0} not found in db! Please report this'.format(pref))
                    
        elif len(addon.getSetting('CustomSub')) > 0:
            self.log(LOG_INFO, 'Custom subs prefs parse error: {0}'.format(addon.getSetting('CustomSub')))
            
        if len(self.custom_subs) > 0:
             self.custom_sub_prefs_on = True
             #self.log(LOG_DEBUG, 'Custom subs prefs: {0}'.format(self.custom_subs))


    def readCustomCondSub(self):
        self.custom_condsub_prefs_on = False
        addon = xbmcaddon.Addon()
        if (addon.getSetting('CustomCondSub').find(self.custom_prefs_delim) > 0):
            for prefs in addon.getSetting('CustomCondSub').split(self.custom_prefs_delim):
                if (prefs.find(self.custom_condSub_delim) > 0):
                    temp_split = prefs.split(self.custom_condSub_delim)
                    if len(temp_split) != 2:
                        self.log(LOG_INFO, 'Custom cond subs prefs parse error: {0}'.format(temp_split))
                    else:
                        temp_a = (languageTranslate(temp_split[0], 3, 0), temp_split[0])
                        temp_s = (languageTranslate(temp_split[1], 3, 0), temp_split[1])
                        if (temp_a[0] and temp_a[1] and temp_s[0] and temp_s[1]):
                            self.custom_condsub.append((temp_a[0], temp_a[1], temp_s[0], temp_s[1]))
                        else:
                            self.log(LOG_INFO, 'Custom cond sub prefs: lang code not found in db! Please report this: {0}:{1}'.format(temp_a, temp_s))
        if len(self.custom_condsub) >0:
            self.custom_condsub_prefs_on = True
            #self.log(LOG_DEBUG, 'Custom cond subs prefs: {0}'.format(self.custom_condsub))
