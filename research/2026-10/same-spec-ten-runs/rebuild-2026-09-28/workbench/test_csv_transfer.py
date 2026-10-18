"""Oracle checks for the bounded CSV teaching example."""
import unittest
import csv_transfer as demo


class CSVTransferTests(unittest.TestCase):
    def setUp(self):
        self.cases = demo.fixtures()

    def test_accepts_crlf(self):
        self.assertTrue(demo.contract_accepts(self.cases["valid_crlf"]))

    def test_accepts_lf(self):
        self.assertTrue(demo.contract_accepts(self.cases["valid_lf"]))

    def test_rejects_wrong_header(self):
        self.assertFalse(demo.contract_accepts(self.cases["wrong_header"]))

    def test_rejects_wrong_order(self):
        self.assertFalse(demo.contract_accepts(self.cases["wrong_order"]))

    def test_rejects_wrong_value(self):
        self.assertFalse(demo.contract_accepts(self.cases["wrong_value"]))

    def test_rejects_deduplication(self):
        self.assertFalse(demo.contract_accepts(self.cases["deduplicated"]))

    def test_exact_bytes_rejects_legal_alternative(self):
        self.assertNotEqual(self.cases["valid_lf"], self.cases["valid_crlf"])
        self.assertEqual(demo.parse(self.cases["valid_lf"]), demo.parse(self.cases["valid_crlf"]))

    def test_parse_alone_accepts_wrong_content(self):
        for name in ("deduplicated", "wrong_header", "wrong_order", "wrong_value"):
            with self.subTest(name=name):
                self.assertTrue(demo.parse_only(self.cases[name]))

    def test_preserves_comma_embedded_newline_empty_date_and_duplicates(self):
        rows = demo.parse(self.cases["valid_lf"])
        self.assertEqual(rows[1], ["王,小明", "", "第一行\n第二行"])
        self.assertEqual(rows[2:], [["李", "2026-09-28", ""], ["李", "2026-09-28", ""]])

    def test_rejects_invalid_utf8(self):
        self.assertFalse(demo.contract_accepts(b"\xff"))

    def test_rejects_unclosed_quote(self):
        self.assertFalse(demo.contract_accepts(b'name,date,note\n"unterminated'))


if __name__ == "__main__":
    unittest.main()
