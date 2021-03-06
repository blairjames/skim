#!/usr/bin/env python3


class Hasher():
    '''
    Hasher takes responsibility for filtering and hashing content from http response data.
    Dynamic_content is the "List" of dynamic elements that cause false positive alerts.
    '''
    def __init__(self):
        self.dynamic_content = [
            "__REQUESTDIGEST",
            "window[\"_csrf_\"",
            "/resume/idp/prp.ping",
            "<div id=\"fws_",
            "formDigestElement.value",
            "var _spRegionalSettings",
            "_fV4UI=true;var",
            "__VIEWSTATE",
            "addMenuItem",
            "formDigestElement.value",
            "douglascrockford/JSON-js",
            "var heightArray ",
            "var titleArray ",
            "ML:128-PU",
            "var descriptionArray",
            "DC.date.modified",
            "secure.aadcdn.microsoftonline-p",
            "RowCount",
            "ms-rteElement-P",
            "var linkArray ",
            "var pictureArray",
            "ScriptResource.axd?",
            "WebResource.axd?",
            "PlaceHolderSearchArea",
            "login.microsoftonline.com",
            "gaq.push",
            "SPWebPartManager1",
            "__EVENTVALIDATION",
            "g_ViewIdToViewCounterMap",
            "TotalRowsIncludingDuplicates",
            "theme_token",
            "fallbackSort",
            "ctx.ctxId",
            "g_ctxDict",
            "ctx;",
            "<small style=\"color",
            "loginUrl",
            "var widthArray = ",
            "name=\"SAMLRequest\"",
            "name=\"RelayState\"",
            "var rendererModel",
            "var publicModel",
            "</script><tr><td><iframe src=\"javascript:false;\" id=\"FilterIframe",
            "\"GenerationId\"",
            "QueryErrors",
            "QueryId",
            "ObjectType_\":\"Microsoft.SharePoint.Client.Search.Query",
            "\"DocId\"",
            "\"SourceId\"",
            "PingFed",
            "authorization.ping",
            "__RequestVerificationToken",
            "WebPartWPQ5",
            "autoplay\" id=\"",
            "data-prime-desktop-src=",
            "console.info",
            "prime-ajax-image",
            "data-prime-tablet-src",
            "content=\"WordPress",
            "viewerSessionId",
            "data-prime-mobile",
            "<div class=\"flex-caption",
            "<div class=\"caption\">",
            "<div class=\"clear",
            "</div>",
            "moodle-core-formautosubmit",
            "OF THIRD PARTY NOTICE",
            "sesskey",
            "M.util.js_pending",
            "Duplicate agent injection detected",
            "fShowPersistentCookiesWarning",
            "_fV4UI",
            "960x344.jpg",
            "slideshow_item",
            "layouts/1033/styles/Themable/corev4",
            "\n",
            "29wp.org/jquery.js",
            "\"NCSRF\"",
            "ruxitagentjs",
            "$(\'#single_selec",
            "M.util.js_complete",
            "CalendarMini.init",
            "class=\"hidden\">Version 1.1.0.0",
            "wp-emoji-release.min.js?ver=",
            "wp-includes/js/wp-embed.min.js?ver=",
            "alyeska/assets/js/alyeska.min.js?ver=",
            "class=\"hidden\">Version 1.0.2.0"
        ]

    def checker(self, line: str) -> bool:
        '''
        Checks each element of the dynamic_content "List" against the "line" parameter and return bool
        '''
        try:
            import skim_utils
            lint = skim_utils.SkimUitls().lint
            line = str(line)
            cont = self.dynamic_content
            for el in cont:
                if el in line:
                    return True
            return False
        except Exception as e:
            print("Error! in Hasher.checker: " + str(e))


    def strip_digest(self, content) -> str:
        '''
        Filter out content that is always changing to stop False positives.
        If line of content is not flagged as True (in dynamic_content List) by "self.checker"
        '''
        try:
            modded = []
            apnd = modded.append
            content = str(content)
            for line in content.splitlines():
                test = self.checker(line)
                if not test:
                    apnd(line)
            return "\n".join(modded)
        except Exception as e:
            print("Error! in Hasher: " + str(e))

    def hashit(self, content):
        '''
        Once content is filtered hash it with md5
        '''
        try:
            import hashlib
            if not content:
                raise Exception
            encoded = content.encode("utf-8")
            md5 = hashlib.md5(encoded)
            md5d = md5.hexdigest()
            return str(md5d)
        except Exception as e:
            print("Error in Hasher.hashit: " + str(e))

