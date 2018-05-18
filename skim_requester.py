#!/usr/bin/env python3

import requests

import skim_utils
import skim_writer_io


class SkimRequester:
    '''
    Handle sending HTTP requests and parsing HTTP responses.
    '''
    def send_request(self, url):
        '''g
        Take url, send HTTP request then process through logic according to response.
        '''
        try:
            import toolbag
            import skim_cms_filter
            import skim_controller
            headers = toolbag.Toolbag().get_headers("ie")
            writer = skim_writer_io.Skim_writer_io().writer
            http_timeout = skim_controller.SkimController().http_timeout
            utils = skim_utils.SkimUitls()
            cms = skim_cms_filter.SkimCmsFilter()
            url = str(url)
            res = requests.get(url, headers=headers, timeout=http_timeout)
            code = res.status_code
            if code == 200:
                writer(url, "up")
                utils.manage_content(url, res.text)

                #short circuit, if one CMS then not another, in order of probability
                if not cms.is_it_sharepoint(url, res.headers):
                    if not cms.is_it_wordpress(url, res.headers):
                        if not cms.is_it_drupal(url, res.headers, res.text):
                            cms.is_it_joomla(url, res.headers)
                        else:
                            pass
                    else:
                        pass
                else:
                    #Uncomment to show performance stats
                    #utils.lint(str(url) + " Perf Manage Content: " + str(utils.perf_manage_content))
                    #utils.lint(str(url) + ": Perf Drupal: " + str(cms.perf_is_it_drupal))
                    #utils.lint(str(url) + ": Perf Wordpress: " + str(cms.perf_is_it_wordpress))
                    #utils.lint(str(url) + ": Perf_sharepoint: " + str(cms.perf_is_it_sharepoint))
                    #utils.lint(str(url) + ": Perf_Joomla: " + str(cms.perf_is_it_joomla))
                    return True
            else:
                res.raise_for_status()

        except requests.ConnectTimeout as ct:
            writer = skim_writer_io.Skim_writer_io().writer
            lint = skim_utils.SkimUitls().lint
            if "SSL" in str(ct):
                lint(url + " - SSL Error!!! " + str(ct) + "\n")
                writer(url, "ssl")
                return True
            else:
                lint(url + " - Connect Timeout!!! " + str(ct) + "\n")
                writer(url, "not_responding")
                return True

        except requests.ConnectionError as c:
            writer = skim_writer_io.Skim_writer_io().writer
            lint = skim_utils.SkimUitls().lint
            if "SSSLError" in str(c):
                lint(url + " - SSL Error !!! \n")
                writer(url, "ssl")
                return True

            elif "503" in str(c):
                lint(url + " - 503 Transaction error!! \n")
                writer(url, "up")
                return True

            elif "Max retries exceeded with url" in str(c):
                lint(url + " - site not responding\n")
                writer(url, "not_responding")
                return True
            else:
                lint(url + " - Connection Error !!! " + "\n")
                writer(url, "not_responding")
                return True

        except requests.ReadTimeout as rt:
            lint = skim_utils.SkimUitls().lint
            writer = skim_writer_io.Skim_writer_io().writer
            lint(url + " !!! Read Timeout!!! " + str(rt) + "\n")
            writer(url, "investigate")
            return True

        except requests.URLRequired as ur:
            lint = skim_utils.SkimUitls().lint
            writer = skim_writer_io.Skim_writer_io().writer
            lint(url + " !!! URLRequired Error!!! " + str(ur) + "\n")
            writer(url, "investigate")
            return True

        except requests.TooManyRedirects as tmr:
            lint = skim_utils.SkimUitls().lint
            writer = skim_writer_io.Skim_writer_io().writer
            lint(url + " !!! TooManyRedirects Error!!! " + str(tmr) + "\n")
            writer(url, "investigate")
            return True

        except requests.RequestsDependencyWarning as d:
            lint = skim_utils.SkimUitls().lint
            writer = skim_writer_io.Skim_writer_io().writer
            lint(url + " !!! RequestsDependencyWarning Error!!! " + str(d) + "\n")
            writer(url, "investigate")
            return True

        except requests.HTTPError as h:
            lint = skim_utils.SkimUitls().lint
            writer = skim_writer_io.Skim_writer_io().writer
            if "Authorization Required" in str(h):
                writer = skim_writer_io.Skim_writer_io().writer
                lint(url + " !!! 401 Auth required !!! " + str(h) + "\n")
                writer(url, "up")
                return True

            elif "Client Error: Forbidden for url" in str(h):
                lint(url + " !!! 403 Forbidden !!! " + str(h) + "\n")
                writer(url, "up")
                return True

            elif "404 Client Error: Not Found for url " in str(h):
                lint(url + " !!! 404 Not Found !!! " + str(h) + "\n")
                writer(url, "not_responding")
                return True

            elif "500 Server Error: INTERNAL SERVER ERROR" in str(h):
                lint(url + " !!! 500 INTERNAL SERVER ERROR !!! " + str(h) + "\n")
                writer(url, "up")
                return True

            elif "503 Server Error: Your transaction has failed." in str(h):
                lint(url + " !!! 503 Transaction Failed !!! " + str(h) + "\n")
                writer(url, "up")
                return True
            else:
                lint(url + " !!! HTTPError !!! " + str(h) + "\n")
                writer(url, "http_errors")
                return True

        except requests.Timeout as t:
            lint = skim_utils.SkimUitls().lint
            writer = skim_writer_io.Skim_writer_io().writer
            lint(url + " !!!Timeout!!! " + str(t) + "\n")
            writer(url, "investigate")
            return True

        except requests.RequestException as r:
            lint = skim_utils.SkimUitls().lint
            writer = skim_writer_io.Skim_writer_io().writer
            if "URL has an invalid label" in str(r):
                lint(url + " - URL has an invalid label\n")
                writer(url, "up")
                return True
            else:
                lint(url + " !!! request exception!!!! " + str(r) + "\n")
                writer(url, "investigate")
                return True

        except Exception as e:
            lint = skim_utils.SkimUitls().lint
            writer = skim_writer_io.Skim_writer_io().writer
            lint(url + " !!! Investigate !!!" + str(e) + "\n")
            writer(url, "investigate")
            return True
