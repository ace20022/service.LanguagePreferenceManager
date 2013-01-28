# -*- coding: utf-8 -*- 




LANGUAGES      = (
    
    # Full Language name[0]     podnapisi[1]  ISO 639-1[2]   ISO 639-1 Code[3]   Script Setting Language[4]   localized name id number[5]
    
    ("Albanian"                   , "29",       "sq",            "alb",                 "0",                     30201  ),
    ("Arabic"                     , "12",       "ar",            "ara",                 "1",                     30202  ),
    ("Belarusian"                 , "0" ,       "hy",            "arm",                 "2",                     30203  ),
    ("Bosnian"                    , "10",       "bs",            "bos",                 "3",                     30204  ),
    ("Bulgarian"                  , "33",       "bg",            "bul",                 "4",                     30205  ),
    ("Catalan"                    , "53",       "ca",            "cat",                 "5",                     30206  ),
    ("Chinese"                    , "17",       "zh",            "chi",                 "6",                     30207  ),
    ("Croatian"                   , "38",       "hr",            "hrv",                 "7",                     30208  ),
    ("Czech"                      , "7",        "cs",            "cze",                 "8",                     30209  ),
    ("Danish"                     , "24",       "da",            "dan",                 "9",                     30210  ),
    ("Dutch"                      , "23",       "nl",            "dut",                 "10",                    30211  ),
    ("English"                    , "2",        "en",            "eng",                 "11",                    30212  ),
    ("Estonian"                   , "20",       "et",            "est",                 "12",                    30213  ),
    ("Persian"                    , "52",       "fa",            "per",                 "13",                    30247  ),
    ("Finnish"                    , "31",       "fi",            "fin",                 "14",                    30214  ),
    ("French"                     , "8",        "fr",            "fre",                 "15",                    30215  ),
    ("German"                     , "5",        "de",            "ger",                 "16",                    30216  ),
    ("Greek"                      , "16",       "el",            "ell",                 "17",                    30217  ),
    ("Hebrew"                     , "22",       "he",            "heb",                 "18",                    30218  ),
    ("Hindi"                      , "42",       "hi",            "hin",                 "19",                    30219  ),
    ("Hungarian"                  , "15",       "hu",            "hun",                 "20",                    30220  ),
    ("Icelandic"                  , "6",        "is",            "ice",                 "21",                    30221  ),
    ("Indonesian"                 , "0",        "id",            "ind",                 "22",                    30222  ),
    ("Italian"                    , "9",        "it",            "ita",                 "23",                    30224  ),
    ("Japanese"                   , "11",       "ja",            "jpn",                 "24",                    30225  ),
    ("Korean"                     , "4",        "ko",            "kor",                 "25",                    30226  ),
    ("Latvian"                    , "21",       "lv",            "lav",                 "26",                    30227  ),
    ("Lithuanian"                 , "0",        "lt",            "lit",                 "27",                    30228  ),
    ("Macedonian"                 , "35",       "mk",            "mac",                 "28",                    30229  ),
    ("Norwegian"                  , "3",        "no",            "nor",                 "29",                    30230  ),
    ("Polish"                     , "26",       "pl",            "pol",                 "30",                    30232  ),
    ("Portuguese"                 , "32",       "pt",            "por",                 "31",                    30233  ),
    ("PortugueseBrazil"           , "48",       "pb",            "pob",                 "32",                    30234  ),
    ("Romanian"                   , "13",       "ro",            "rum",                 "33",                    30235  ),
    ("Russian"                    , "27",       "ru",            "rus",                 "34",                    30236  ),
    ("Serbian"                    , "36",       "sr",            "scc",                 "35",                    30237  ),
    ("Slovak"                     , "37",       "sk",            "slo",                 "36",                    30238  ),
    ("Slovenian"                  , "1",        "sl",            "slv",                 "37",                    30239  ),
    ("Spanish"                    , "28",       "es",            "spa",                 "38",                    30240  ),
    ("Swedish"                    , "25",       "sv",            "swe",                 "39",                    30242  ),
    ("Thai"                       , "0",        "th",            "tha",                 "40",                    30243  ),
    ("Turkish"                    , "30",       "tr",            "tur",                 "41",                    30244  ),
    ("Ukrainian"                  , "46",       "uk",            "ukr",                 "42",                    30245  ),
    ("Vietnamese"                 , "51",       "vi",            "vie",                 "43",                    30246  ),
    ("BosnianLatin"               , "10",       "bs",            "bos",                 "100",                   30204  ),
    ("Farsi"                      , "52",       "fa",            "per",                 "13",                    30247  ),
    ("English (US)"               , "2",        "en",            "eng",                 "100",                   30212  ),
    ("English (UK)"               , "2",        "en",            "eng",                 "100",                   30212  ),
    ("Portuguese (Brazilian)"     , "48",       "pt-br",         "pob",                 "100",                   30234  ),
    ("Portuguese (Brazil)"        , "48",       "pb",            "pob",                 "32",                    30234  ),
    ("Portuguese-BR"              , "48",       "pb",            "pob",                 "32",                    30234  ),
    ("Brazilian"                  , "48",       "pb",            "pob",                 "32",                    30234  ),
    ("Español (Latinoamérica)"    , "28",       "es",            "spa",                 "100",                   30240  ),
    ("Español (España)"           , "28",       "es",            "spa",                 "100",                   30240  ),
    ("Spanish (Latin America)"    , "28",       "es",            "spa",                 "100",                   30240  ),
    ("Español"                    , "28",       "es",            "spa",                 "100",                   30240  ),
    ("SerbianLatin"               , "36",       "sr",            "scc",                 "100",                   30237  ),
    ("Spanish (Spain)"            , "28",       "es",            "spa",                 "100",                   30240  ),
    ("Chinese (Traditional)"      , "17",       "zh",            "chi",                 "100",                   30207  ),
    ("Chinese (Simplified)"       , "17",       "zh",            "chi",                 "100",                   30207  ) )

def languageTranslate(lang, lang_from, lang_to):
  for x in LANGUAGES:
    if lang == x[lang_from] :
      return x[lang_to]
