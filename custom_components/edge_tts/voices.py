# --- START OF FILE voices.py ---

"""Contains the dictionary of supported voices for the Edge TTS integration."""

# Format: 'voice-id': 'language-code'
SUPPORTED_VOICES = {
    'zh-CN-XiaoxiaoNeural': 'zh-CN',
    'zh-CN-XiaoyiNeural': 'zh-CN',
    'zh-CN-YunjianNeural': 'zh-CN',
    'zh-CN-YunxiNeural': 'zh-CN',
    'zh-CN-YunxiaNeural': 'zh-CN',
    'zh-CN-YunyangNeural': 'zh-CN',
    'zh-HK-HiuGaaiNeural': 'zh-HK',
    'zh-HK-HiuMaanNeural': 'zh-HK',
    'zh-HK-WanLungNeural': 'zh-HK',
    'zh-TW-HsiaoChenNeural': 'zh-TW',
    'zh-TW-YunJheNeural': 'zh-TW',
    'zh-TW-HsiaoYuNeural': 'zh-TW',
    'af-ZA-AdriNeural': 'af-ZA',
    'af-ZA-WillemNeural': 'af-ZA',
    'am-ET-AmehaNeural': 'am-ET',
    'am-ET-MekdesNeural': 'am-ET',
    'ar-AE-FatimaNeural': 'ar-AE',
    'ar-AE-HamdanNeural': 'ar-AE',
    'ar-BH-AliNeural': 'ar-BH',
    'ar-BH-LailaNeural': 'ar-BH',
    'ar-DZ-AminaNeural': 'ar-DZ',
    'ar-DZ-IsmaelNeural': 'ar-DZ',
    'ar-EG-SalmaNeural': 'ar-EG',
    'ar-EG-ShakirNeural': 'ar-EG',
    'ar-IQ-BasselNeural': 'ar-IQ',
    'ar-IQ-RanaNeural': 'ar-IQ',
    'ar-JO-SanaNeural': 'ar-JO',
    'ar-JO-TaimNeural': 'ar-JO',
    'ar-KW-FahedNeural': 'ar-KW',
    'ar-KW-NouraNeural': 'ar-KW',
    'ar-LB-LaylaNeural': 'ar-LB',
    'ar-LB-RamiNeural': 'ar-LB',
    'ar-LY-ImanNeural': 'ar-LY',
    'ar-LY-OmarNeural': 'ar-LY',
    'ar-MA-JamalNeural': 'ar-MA',
    'ar-MA-MounaNeural': 'ar-MA',
    'ar-OM-AbdullahNeural': 'ar-OM',
    'ar-OM-AyshaNeural': 'ar-OM',
    'ar-QA-AmalNeural': 'ar-QA',
    'ar-QA-MoazNeural': 'ar-QA',
    'ar-SA-HamedNeural': 'ar-SA',
    'ar-SA-ZariyahNeural': 'ar-SA',
    'ar-SY-AmanyNeural': 'ar-SY',
    'ar-SY-LaithNeural': 'ar-SY',
    'ar-TN-HediNeural': 'ar-TN',
    'ar-TN-ReemNeural': 'ar-TN',
    'ar-YE-MaryamNeural': 'ar-YE',
    'ar-YE-SalehNeural': 'ar-YE',
    'az-AZ-BabekNeural': 'az-AZ',
    'az-AZ-BanuNeural': 'az-AZ',
    'bg-BG-BorislavNeural': 'bg-BG',
    'bg-BG-KalinaNeural': 'bg-BG',
    'bn-BD-NabanitaNeural': 'bn-BD',
    'bn-BD-PradeepNeural': 'bn-BD',
    'bn-IN-BashkarNeural': 'bn-IN',
    'bn-IN-TanishaaNeural': 'bn-IN',
    'bs-BA-GoranNeural': 'bs-BA',
    'bs-BA-VesnaNeural': 'bs-BA',
    'ca-ES-EnricNeural': 'ca-ES',
    'ca-ES-JoanaNeural': 'ca-ES',
    'cs-CZ-AntoninNeural': 'cs-CZ',
    'cs-CZ-VlastaNeural': 'cs-CZ',
    'cy-GB-AledNeural': 'cy-GB',
    'cy-GB-NiaNeural': 'cy-GB',
    'da-DK-ChristelNeural': 'da-DK',
    'da-DK-JeppeNeural': 'da-DK',
    'de-AT-IngridNeural': 'de-AT',
    'de-AT-JonasNeural': 'de-AT',
    'de-CH-JanNeural': 'de-CH',
    'de-CH-LeniNeural': 'de-CH',
    'de-DE-AmalaNeural': 'de-DE',
    'de-DE-ConradNeural': 'de-DE',
    'de-DE-KatjaNeural': 'de-DE',
    'de-DE-SeraphinaMultilingualNeural': 'de-DE',
    'de-DE-KillianNeural': 'de-DE',
    'el-GR-AthinaNeural': 'el-GR',
    'el-GR-NestorasNeural': 'el-GR',
    'en-AU-NatashaNeural': 'en-AU',
    'en-AU-WilliamNeural': 'en-AU',
    'en-CA-ClaraNeural': 'en-CA',
    'en-CA-LiamNeural': 'en-CA',
    'en-GB-LibbyNeural': 'en-GB',
    'en-GB-MaisieNeural': 'en-GB',
    'en-GB-RyanNeural': 'en-GB',
    'en-GB-SoniaNeural': 'en-GB',
    'en-GB-ThomasNeural': 'en-GB',
    'en-HK-SamNeural': 'en-HK',
    'en-HK-YanNeural': 'en-HK',
    'en-IE-ConnorNeural': 'en-IE',
    'en-IE-EmilyNeural': 'en-IE',
    'en-IN-NeerjaNeural': 'en-IN',
    'en-IN-PrabhatNeural': 'en-IN',
    'en-KE-AsiliaNeural': 'en-KE',
    'en-KE-ChilembaNeural': 'en-KE',
    'en-NG-AbeoNeural': 'en-NG',
    'en-NG-EzinneNeural': 'en-NG',
    'en-NZ-MitchellNeural': 'en-NZ',
    'en-NZ-MollyNeural': 'en-NZ',
    'en-PH-JamesNeural': 'en-PH',
    'en-PH-RosaNeural': 'en-PH',
    'en-SG-LunaNeural': 'en-SG',
    'en-SG-WayneNeural': 'en-SG',
    'en-TZ-ElimuNeural': 'en-TZ',
    'en-TZ-ImaniNeural': 'en-TZ',
    'en-US-AnaNeural': 'en-US',
    'en-US-AriaNeural': 'en-US',
    'en-US-ChristopherNeural': 'en-US',
    'en-US-EricNeural': 'en-US',
    'en-US-GuyNeural': 'en-US',
    'en-US-JennyNeural': 'en-US',
    'en-US-MichelleNeural': 'en-US',
    'en-ZA-LeahNeural': 'en-ZA',
    'en-ZA-LukeNeural': 'en-ZA',
    'es-AR-ElenaNeural': 'es-AR',
    'es-AR-TomasNeural': 'es-AR',
    'es-BO-MarceloNeural': 'es-BO',
    'es-BO-SofiaNeural': 'es-BO',
    'es-CL-CatalinaNeural': 'es-CL',
    'es-CL-LorenzoNeural': 'es-CL',
    'es-CO-GonzaloNeural': 'es-CO',
    'es-CO-SalomeNeural': 'es-CO',
    'es-CR-JuanNeural': 'es-CR',
    'es-CR-MariaNeural': 'es-CR',
    'es-CU-BelkysNeural': 'es-CU',
    'es-CU-ManuelNeural': 'es-CU',
    'es-DO-EmilioNeural': 'es-DO',
    'es-DO-RamonaNeural': 'es-DO',
    'es-EC-AndreaNeural': 'es-EC',
    'es-EC-LuisNeural': 'es-EC',
    'es-ES-AlvaroNeural': 'es-ES',
    'es-ES-ElviraNeural': 'es-ES',
    'es-ES-ManuelEsCUNeural': 'es-ES',
    'es-GQ-JavierNeural': 'es-GQ',
    'es-GQ-TeresaNeural': 'es-GQ',
    'es-GT-AndresNeural': 'es-GT',
    'es-GT-MartaNeural': 'es-GT',
    'es-HN-CarlosNeural': 'es-HN',
    'es-HN-KarlaNeural': 'es-HN',
    'es-MX-DaliaNeural': 'es-MX',
    'es-MX-JorgeNeural': 'es-MX',
    'es-MX-LorenzoEsCLNeural': 'es-MX',
    'es-NI-FedericoNeural': 'es-NI',
    'es-NI-YolandaNeural': 'es-NI',
    'es-PA-MargaritaNeural': 'es-PA',
    'es-PA-RobertoNeural': 'es-PA',
    'es-PE-AlexNeural': 'es-PE',
    'es-PE-CamilaNeural': 'es-PE',
    'es-PR-KarinaNeural': 'es-PR',
    'es-PR-VictorNeural': 'es-PR',
    'es-PY-MarioNeural': 'es-PY',
    'es-PY-TaniaNeural': 'es-PY',
    'es-SV-LorenaNeural': 'es-SV',
    'es-SV-RodrigoNeural': 'es-SV',
    'es-US-AlonsoNeural': 'es-US',
    'es-US-PalomaNeural': 'es-US',
    'es-UY-MateoNeural': 'es-UY',
    'es-UY-ValentinaNeural': 'es-UY',
    'es-VE-PaolaNeural': 'es-VE',
    'es-VE-SebastianNeural': 'es-VE',
    'et-EE-AnuNeural': 'et-EE',
    'et-EE-KertNeural': 'et-EE',
    'fa-IR-DilaraNeural': 'fa-IR',
    'fa-IR-FaridNeural': 'fa-IR',
    'fi-FI-HarriNeural': 'fi-FI',
    'fi-FI-NooraNeural': 'fi-FI',
    'fil-PH-AngeloNeural': 'fil-PH',
    'fil-PH-BlessicaNeural': 'fil-PH',
    'fr-BE-CharlineNeural': 'fr-BE',
    'fr-BE-GerardNeural': 'fr-BE',
    'fr-CA-AntoineNeural': 'fr-CA',
    'fr-CA-JeanNeural': 'fr-CA',
    'fr-CA-SylvieNeural': 'fr-CA',
    'fr-CH-ArianeNeural': 'fr-CH',
    'fr-CH-FabriceNeural': 'fr-CH',
    'fr-FR-DeniseNeural': 'fr-FR',
    'fr-FR-EloiseNeural': 'fr-FR',
    'fr-FR-HenriNeural': 'fr-FR',
    'ga-IE-ColmNeural': 'ga-IE',
    'ga-IE-OrlaNeural': 'ga-IE',
    'gl-ES-RoiNeural': 'gl-ES',
    'gl-ES-SabelaNeural': 'gl-ES',
    'gu-IN-DhwaniNeural': 'gu-IN',
    'gu-IN-NiranjanNeural': 'gu-IN',
    'he-IL-AvriNeural': 'he-IL',
    'he-IL-HilaNeural': 'he-IL',
    'hi-IN-MadhurNeural': 'hi-IN',
    'hi-IN-SwaraNeural': 'hi-IN',
    'hr-HR-GabrijelaNeural': 'hr-HR',
    'hr-HR-SreckoNeural': 'hr-HR',
    'hu-HU-NoemiNeural': 'hu-HU',
    'hu-HU-TamasNeural': 'hu-HU',
    'id-ID-ArdiNeural': 'id-ID',
    'id-ID-GadisNeural': 'id-ID',
    'is-IS-GudrunNeural': 'is-IS',
    'is-IS-GunnarNeural': 'is-IS',
    'it-IT-DiegoNeural': 'it-IT',
    'it-IT-ElsaNeural': 'it-IT',
    'it-IT-IsabellaNeural': 'it-IT',
    'ja-JP-KeitaNeural': 'ja-JP',
    'ja-JP-NanamiNeural': 'ja-JP',
    'jv-ID-DimasNeural': 'jv-ID',
    'jv-ID-SitiNeural': 'jv-ID',
    'ka-GE-EkaNeural': 'ka-GE',
    'ka-GE-GiorgiNeural': 'ka-GE',
    'kk-KZ-AigulNeural': 'kk-KZ',
    'kk-KZ-DauletNeural': 'kk-KZ',
    'km-KH-PisethNeural': 'km-KH',
    'km-KH-SreymomNeural': 'km-KH',
    'kn-IN-GaganNeural': 'kn-IN',
    'kn-IN-SapnaNeural': 'kn-IN',
    'ko-KR-InJoonNeural': 'ko-KR',
    'ko-KR-SunHiNeural': 'ko-KR',
    'lo-LA-ChanthavongNeural': 'lo-LA',
    'lo-LA-KeomanyNeural': 'lo-LA',
    'lt-LT-LeonasNeural': 'lt-LT',
    'lt-LT-OnaNeural': 'lt-LT',
    'lv-LV-EveritaNeural': 'lv-LV',
    'lv-LV-NilsNeural': 'lv-LV',
    'mk-MK-AleksandarNeural': 'mk-MK',
    'mk-MK-MarijaNeural': 'mk-MK',
    'ml-IN-MidhunNeural': 'ml-IN',
    'ml-IN-SobhanaNeural': 'ml-IN',
    'mn-MN-BataaNeural': 'mn-MN',
    'mn-MN-YesuiNeural': 'mn-MN',
    'mr-IN-AarohiNeural': 'mr-IN',
    'mr-IN-ManoharNeural': 'mr-IN',
    'ms-MY-OsmanNeural': 'ms-MY',
    'ms-MY-YasminNeural': 'ms-MY',
    'mt-MT-GraceNeural': 'mt-MT',
    'mt-MT-JosephNeural': 'mt-MT',
    'my-MM-NilarNeural': 'my-MM',
    'my-MM-ThihaNeural': 'my-MM',
    'nb-NO-FinnNeural': 'nb-NO',
    'nb-NO-PernilleNeural': 'nb-NO',
    'ne-NP-HemkalaNeural': 'ne-NP',
    'ne-NP-SagarNeural': 'ne-NP',
    'nl-BE-ArnaudNeural': 'nl-BE',
    'nl-BE-DenaNeural': 'nl-BE',
    'nl-NL-ColetteNeural': 'nl-NL',
    'nl-NL-FennaNeural': 'nl-NL',
    'nl-NL-MaartenNeural': 'nl-NL',
    'pl-PL-MarekNeural': 'pl-PL',
    'pl-PL-ZofiaNeural': 'pl-PL',
    'ps-AF-GulNawazNeural': 'ps-AF',
    'ps-AF-LatifaNeural': 'ps-AF',
    'pt-BR-AntonioNeural': 'pt-BR',
    'pt-BR-FranciscaNeural': 'pt-BR',
    'pt-PT-DuarteNeural': 'pt-PT',
    'pt-PT-RaquelNeural': 'pt-PT',
    'ro-RO-AlinaNeural': 'ro-RO',
    'ro-RO-EmilNeural': 'ro-RO',
    'ru-RU-DmitryNeural': 'ru-RU',
    'ru-RU-SvetlanaNeural': 'ru-RU',
    'si-LK-SameeraNeural': 'si-LK',
    'si-LK-ThiliniNeural': 'si-LK',
    'sk-SK-LukasNeural': 'sk-SK',
    'sk-SK-ViktoriaNeural': 'sk-SK',
    'sl-SI-PetraNeural': 'sl-SI',
    'sl-SI-RokNeural': 'sl-SI',
    'so-SO-MuuseNeural': 'so-SO',
    'so-SO-UbaxNeural': 'so-SO',
    'sq-AL-AnilaNeural': 'sq-AL',
    'sq-AL-IlirNeural': 'sq-AL',
    'sr-RS-NicholasNeural': 'sr-RS',
    'sr-RS-SophieNeural': 'sr-RS',
    'su-ID-JajangNeural': 'su-ID',
    'su-ID-TutiNeural': 'su-ID',
    'sv-SE-MattiasNeural': 'sv-SE',
    'sv-SE-SofieNeural': 'sv-SE',
    'sw-KE-RafikiNeural': 'sw-KE',
    'sw-KE-ZuriNeural': 'sw-KE',
    'sw-TZ-DaudiNeural': 'sw-TZ',
    'sw-TZ-RehemaNeural': 'sw-TZ',
    'ta-IN-PallaviNeural': 'ta-IN',
    'ta-IN-ValluvarNeural': 'ta-IN',
    'ta-LK-KumarNeural': 'ta-LK',
    'ta-LK-SaranyaNeural': 'ta-LK',
    'ta-MY-KaniNeural': 'ta-MY',
    'ta-MY-SuryaNeural': 'ta-MY',
    'ta-SG-AnbuNeural': 'ta-SG',
    'ta-SG-VenbaNeural': 'ta-SG',
    'te-IN-MohanNeural': 'te-IN',
    'te-IN-ShrutiNeural': 'te-IN',
    'th-TH-NiwatNeural': 'th-TH',
    'th-TH-PremwadeeNeural': 'th-TH',
    'tr-TR-AhmetNeural': 'tr-TR',
    'tr-TR-EmelNeural': 'tr-TR',
    'uk-UA-OstapNeural': 'uk-UA',
    'uk-UA-PolinaNeural': 'uk-UA',
    'ur-IN-GulNeural': 'ur-IN',
    'ur-IN-SalmanNeural': 'ur-IN',
    'ur-PK-AsadNeural': 'ur-PK',
    'ur-PK-UzmaNeural': 'ur-PK',
    'uz-UZ-MadinaNeural': 'uz-UZ',
    'uz-UZ-SardorNeural': 'uz-UZ',
    'vi-VN-HoaiMyNeural': 'vi-VN',
    'vi-VN-NamMinhNeural': 'vi-VN',
    'zu-ZA-ThandoNeural': 'zu-ZA',
    'zu-ZA-ThembaNeural': 'zu-ZA',
}
