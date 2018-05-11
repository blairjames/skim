#!/bin/python3


class Hasher():
    '''
    Hasher takes responsibility for filtering and hashing content.

    Dynamic_content is the "List" of dynamic elements that cause false positive alerts.
    '''
    def __init__(self):
        self.dynamic_content = [

            "__REQUESTDIGEST",
            "window[\"_csrf_\"] ",
            "/resume/idp/prp.ping",
            "<div id=\"fws_",
            "formDigestElement.value",
            "var _spRegionalSettings",
            "_fV4UI=true;var",
            "__VIEWSTATE",
            "formDigestElement.value",
            "var heightArray ",
            "var titleArray ",
            "var descriptionArray",
            "var linkArray ",
            "var pictureArray",
            "ScriptResource.axd?",
            "WebResource.axd?",
            "PlaceHolderSearchArea",
            "SPWebPartManager1",
            "__EVENTVALIDATION",
            "g_ViewIdToViewCounterMap",
            "fallbackSort",
            "ctx.ctxId",
            "g_ctxDict",
            "ctx;",
            "<small style=\"color",
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
            "<title>Department of Education, Training and Employment</title>",
            "__RequestVerificationToken",
            "WebPartWPQ5",
            "autoplay\" id=\"",
            "data-prime-desktop-src=",
            "prime-ajax-image",
            "data-prime-tablet-src",
            "data-prime-mobile",
            "<div class=\"flex-caption",
            "<div class=\"caption\">",
            "<div class=\"clear",
            "</div>",
            "moodle-core-formautosubmit",
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
            "wp-emoji-release.min.js?ver=",
            "wp-includes/js/wp-embed.min.js?ver=",
            "alyeska/assets/js/alyeska.min.js?ver=",
            "class=\"hidden\">Version 1.0.2.0 ("
        ]

    def checker(self, line: str) -> bool:
        '''
        Checks each element of the dynamic_content "List" against the "line" parameter and return bool
        '''
        try:
            line = str(line)
            cont = self.dynamic_content
            for el in cont:
                if str(el) in line:
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
            content = str(content)
            for line in content.splitlines():
                test = self.checker(line)
                if not test:
                    modded.append(str(line))
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

