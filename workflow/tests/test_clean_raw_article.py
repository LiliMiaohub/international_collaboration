import pickle
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import pandas as pd


class CleanRawArticleTest(unittest.TestCase):
    def test_writes_cleaned_articles_and_id_map(self):
        script = Path(__file__).resolve().parents[1] / "scripts/clean_raw_article.py"
        with tempfile.TemporaryDirectory() as directory:
            raw, cleaned, mapping = [Path(directory) / name for name in
                                     ("raw.txt", "cleaned.pkl", "mapping.pkl")]
            raw.write_text("uid|ost_bk|year|dis|title\nWOS:1|123|2020|7|Example\n")
            subprocess.run([sys.executable, str(script), str(raw), str(cleaned),
                            str(mapping)], check=True)
            self.assertEqual(pd.read_pickle(cleaned).to_dict("records"),
                             [{"ost_bk": 123, "year": 2020, "dis": 7, "title": "Example"}])
            with mapping.open("rb") as stream:
                self.assertEqual(pickle.load(stream), {123: "WOS:1"})


if __name__ == "__main__":
    unittest.main()
