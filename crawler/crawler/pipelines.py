import json
from pathlib import Path

class JsonWriterPipeline:
    def open_spider(self, spider):
        self.filepath = Path("output.json")
        # If you prefer per-run outputs, include timestamped filename
        self.file = open(self.filepath, "w", encoding="utf-8")
        self.first = True
        self.file.write("[\n")

    def close_spider(self, spider):
        self.file.write("\n]\n")
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False)
        if not self.first:
            self.file.write(",\n")
        self.file.write(line)
        self.first = False
        return item

