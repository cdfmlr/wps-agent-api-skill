import argparse
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import wps_docs


BAD = {"id": "1", "title": "bad", "path": "/bad", "source": "dms"}
GOOD = {"id": "2", "title": "good", "path": "/good", "source": "dms"}


def run_sync(out, docs=(BAD,), fail_titles=("bad",)):
    args = argparse.Namespace(out=out, lang="zh-CN", workers=1)

    def fetch(doc, lang):
        if doc["title"] in fail_titles:
            raise RuntimeError("boom")
        return "# ok"

    with mock.patch.object(wps_docs, "flatten", return_value=list(docs)), \
            mock.patch.object(wps_docs, "doc_markdown", side_effect=fetch):
        with redirect_stderr(io.StringIO()) as err, redirect_stdout(io.StringIO()) as out_io:
            try:
                wps_docs.cmd_sync(args)
                code = 0
            except SystemExit as exc:
                code = exc.code
    return code, err.getvalue(), out_io.getvalue()


class SyncTest(unittest.TestCase):
    def test_all_failures_write_stderr_and_exit_nonzero(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, err, out = run_sync(tmp)
            self.assertNotEqual(code, 0)
            self.assertIn("FAILED bad: boom", err)
            self.assertIn("synced 0 docs", out)
            self.assertFalse((Path(tmp) / "index.json").exists())

    def test_partial_failure_still_succeeds(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, err, _ = run_sync(tmp, docs=(BAD, GOOD))
            index = json.loads((Path(tmp) / "index.json").read_text())
            self.assertEqual(code, 0)
            self.assertIn("FAILED bad: boom", err)
            self.assertEqual([item["id"] for item in index], ["2"])


if __name__ == "__main__":
    unittest.main()
