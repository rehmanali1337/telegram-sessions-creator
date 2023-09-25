import os
from typing import Dict, Any
import toml


GeneralDict = Dict[str, Any]


class TomlReaderGenerator:
    def __init__(self, toml_file: str):
        self._outdir = "GeneratedTomlReader"
        os.makedirs(self._outdir, exist_ok=True)
        self._toml_file = toml_file
        self._data = toml.load(toml_file)

        self.vt_defaults = {
            "str": "''",
            "None": "''",
            "NoneType": "''",
            "int": str(0),
            "list": str([]),
            "dict": str({}),
            "bool": "False",
        }
        self._cast_prohibited_types = ["None", "Any"]
        self.generate_init_vars(self._data)

    def get_vt_default(self, vt: str) -> str:
        try:
            return self.vt_defaults[vt]
        except KeyError:
            return "None"

    def _proper_name(self, name: str) -> str:
        return "".join([p.capitalize() for p in name.split("_")])

    def generate_init_vars(self, data: GeneralDict) -> str:
        _head = """
import toml

class config:
    
"""

        indentation = " " * 4
        _init_vars = f'{_head}\n{indentation}data = toml.load("config.toml")'
        for k, v in data.items():
            # if isinstance(v, dict):
            #     name = self._proper_name(k)
            #     self.generate_init_vars(self._proper_name(k), v)
            #     _in = f"{indentation}cls.{k}: {name} = {name}(data.get(\"{name}\", dict()))"
            #     _init_vars = f"""{_init_vars}\n{_in}"""
            #     continue

            vt = type(v).__name__
            if str(vt).strip() == "NoneType":
                vt = "Any"

            _in = f'{indentation}{k} = data.get("{k}", {self.get_vt_default(vt)})'
            _init_vars = f"""{_init_vars}\n{_in}"""

        complete = f"{_init_vars}"
        with open(f"{self._outdir}/config_reader.py", encoding="utf-8", mode="w") as f:
            f.write(complete)

        return complete


if __name__ == "__main__":
    gen = TomlReaderGenerator("config.toml")
