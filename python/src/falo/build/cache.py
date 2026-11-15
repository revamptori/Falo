from pathlib import Path
import json, hashlib, time

class BuildCache:
    def __init__(self, root: Path):
        self.root = root
        root.mkdir(parents=True, exist_ok=True)
        self.index = root / "index.json"
        self.data = {}
        if self.index.exists():
            try: self.data = json.loads(self.index.read_text())
            except: self.data = {}

    def is_hit(self, key: str) -> bool:
        rec = self.data.get(key)
        if not rec: return False
        # hit if less than 1 hour and files still exist
        return (time.time() - rec.get("time",0)) < 3600

    def store(self, key: str, meta: dict):
        self.data[key] = {"time": time.time(), **meta}
        try: self.index.write_text(json.dumps(self.data, indent=2))
        except: pass
