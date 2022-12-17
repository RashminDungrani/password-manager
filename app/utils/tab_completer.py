import readline
import rlcompleter


### Indenting
class TabCompleter(rlcompleter.Completer):
    """Completer that supports indenting"""

    def __init__(self, commands: list[str] = []):
        self.commands = commands

    def complete(self, text, state):

        options = [i for i in self.commands if i.startswith(text)]
        if state < len(options):
            return options[state]
        else:
            return None

        # if not text:
        #     return ("    ", None)[state]
        # else:
        #     return rlcompleter.Completer.complete(self, text, state)


### Add autocompletion
if "libedit" in readline.__doc__:  # type: ignore
    readline.parse_and_bind("bind -e")
    readline.parse_and_bind("bind '\t' rl_complete")
else:
    readline.parse_and_bind("tab: complete")
