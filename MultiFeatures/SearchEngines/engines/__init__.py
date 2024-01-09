from .aol import Aol
from .ask import Ask
from .bing import Bing
from .brave import Brave
from .dogpile import Dogpile
from .duckduckgo import Duckduckgo
from .google import Google
from .mojeek import Mojeek
from .qwant import Qwant
from .startpage import Startpage
from .torch import Torch
from .yahoo import Yahoo

search_engines_dict = {
    'google': Google,
    'bing': Bing,
    'yahoo': Yahoo,
    'aol': Aol,
    'duckduckgo': Duckduckgo,
    'startpage': Startpage,
    'dogpile': Dogpile,
    'ask': Ask,
    'mojeek': Mojeek,
    'qwant': Qwant,
    'brave': Brave,
    'torch': Torch
}
