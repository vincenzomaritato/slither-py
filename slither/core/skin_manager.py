import importlib
import pkgutil
import os

SKINS_PATH = os.path.join(os.path.dirname(__file__), '../skins')

class SkinManager:
    def __init__(self):
        self.skins = self._load_skins()
        self.skin_names = list(self.skins.keys())
        self.active_index = 0

    def _load_skins(self):
        skins = {}
        for _, modname, _ in pkgutil.iter_modules([SKINS_PATH]):
            mod = importlib.import_module(f'slither.skins.{modname}')
            skins[mod.SKIN['name']] = mod.SKIN
        return skins

    def get_active_skin(self):
        return self.skins[self.skin_names[self.active_index]]

    def next_skin(self):
        self.active_index = (self.active_index + 1) % len(self.skin_names)

    def prev_skin(self):
        self.active_index = (self.active_index - 1) % len(self.skin_names)

    def set_skin_by_name(self, name):
        if name in self.skins:
            self.active_index = self.skin_names.index(name) 