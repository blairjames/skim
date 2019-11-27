#!/usr/bin/env python3


class Skim_conf:
    '''
    Configuration Items
    '''
    def show_banner(self):
        import toolbag
        '''
        Print the banner
        '''
        tb = toolbag.Toolbag()
        color = "green"
        print(tb.color("\n\n   ▄████████    ▄█   ▄█▄  ▄█    ▄▄▄▄███▄▄▄▄   ", color))
        print(tb.color("  ███    ███   ███ ▄███▀ ███  ▄██▀▀▀███▀▀▀██▄ ", color))
        print(tb.color("  ███    █▀    ███▐██▀   ███▌ ███   ███   ███ ", color))
        print(tb.color("  ███         ▄█████▀    ███▌ ███   ███   ███ ", color))
        print(tb.color("▀███████████ ▀▀█████▄    ███▌ ███   ███   ███ ", color))
        print(tb.color("         ███   ███▐██▄   ███  ███   ███   ███ ", color))
        print(tb.color("   ▄█    ███   ███ ▀███▄ ███  ███   ███   ███ ", color))
        print(tb.color(" ▄████████▀    ███   ▀█▀ █▀    ▀█   ███   █▀ ", color))

        print(tb.color("\n\nOnly domains which are not responding 200OK are printed.\n", color))


    def whitelist_domains(self):
        '''
        Whitelist "List" data type containing domains which are not used or not applicable to track content.
        '''
        whitelist_domains = [ ]
        return whitelist_domains

