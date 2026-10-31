import json
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable, List, Optional, Tuple, Union

_DECLARATION_RE = re.compile(r"^\s*(<\?xml[^>]*\?>)")
_ENCODING_RE = re.compile(r"""encoding\s*=\s*(?:"[^"]*"|'[^']*')""")


@dataclass
class UserDefaultEntry:
    """One ``<entry key="...">text</entry>`` of ``UserDefault.xml``."""

    key: str
    text: Optional[str] = None


UserDefaultValue = Union[str, int, float, bool, dict, list]


def _serialize(value: UserDefaultValue) -> str:
    """Strings are stored as they are, anything else as JSON (``true``, ``12``, ``{"a":1}``)."""
    if isinstance(value, str):
        return value

    return json.dumps(value, separators=(",", ":"), ensure_ascii=False)


class UserDefault:
    """Reads and edits the ``UserDefault.xml`` preferences file of the game client."""

    def __init__(self, file_path: Union[str, Path]) -> None:
        self.file_path = Path(file_path)

    def _read(self) -> Tuple[ET.ElementTree, Optional[str]]:
        data = self.file_path.read_bytes()
        match = _DECLARATION_RE.match(data.decode("utf-8-sig", errors="replace"))
        declaration = _ENCODING_RE.sub('encoding="utf-8"', match.group(1)) if match else None
        return ET.ElementTree(ET.fromstring(data)), declaration

    def _write(self, tree: ET.ElementTree, declaration: Optional[str]) -> None:
        root = tree.getroot()
        ET.indent(root, space="    ")
        body = ET.tostring(root, encoding="unicode", short_empty_elements=True)
        self.file_path.write_text(f"{declaration}\n{body}" if declaration else body, encoding="utf-8")

    @staticmethod
    def _entries(tree: ET.ElementTree) -> List[ET.Element]:
        return list(tree.getroot().findall("entry"))

    def read_raw(self) -> ET.ElementTree:
        """The parsed XML document."""
        return self._read()[0]

    def get_entries(self) -> List[UserDefaultEntry]:
        return [
            UserDefaultEntry(key=entry.get("key", ""), text=entry.text if entry.text else None)
            for entry in self._entries(self._read()[0])
        ]

    def get(self, key: str) -> Optional[str]:
        for entry in self.get_entries():
            if entry.key == key:
                return entry.text

        return None

    def list_by_prefix(self, prefix: str) -> List[UserDefaultEntry]:
        return [entry for entry in self.get_entries() if entry.key.startswith(prefix)]

    def list_by_include(self, include: str) -> List[UserDefaultEntry]:
        return [entry for entry in self.get_entries() if include in entry.key]

    def set(self, key: str, value: UserDefaultValue) -> None:
        self.set_many([(key, value)])

    def set_many(self, values: Iterable[Tuple[str, UserDefaultValue]]) -> None:
        """Sets several keys reading and writing the file only once."""
        tree, declaration = self._read()
        root = tree.getroot()

        for key, value in values:
            serialized = _serialize(value)
            existing = next((entry for entry in root.findall("entry") if entry.get("key") == key), None)

            if existing is not None:
                existing.text = serialized
            else:
                entry = ET.SubElement(root, "entry", {"key": key})
                entry.text = serialized

        self._write(tree, declaration)

    def delete(self, key: str) -> None:
        self.delete_many([key])

    def delete_many(self, keys: Iterable[str]) -> None:
        """Deletes several keys reading and writing the file only once."""
        wanted = set(keys)
        tree, declaration = self._read()
        root = tree.getroot()

        for entry in root.findall("entry"):
            if entry.get("key") in wanted:
                root.remove(entry)

        self._write(tree, declaration)

    def update_where(self, predicate: Callable[[str], bool], value: UserDefaultValue) -> None:
        """Sets ``value`` on every existing key accepted by ``predicate``."""
        self.set_many((entry.key, value) for entry in self.get_entries() if predicate(entry.key))
