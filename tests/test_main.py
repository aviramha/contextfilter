import logging
import unittest

from contextfilter import ContextFilter, reset, set_entries, set_entry


class TestSanity(unittest.TestCase):
    def test_sanity(self):
        logger = logging.getLogger("test")
        logger.addFilter(ContextFilter())
        with self.assertLogs(logger, level="INFO") as output:
            logger.info("test1")
            set_entries(test_attr="test_data")
            logger.info("test2")
            reset()
            logger.info("test3")

        self.assertIsNone(getattr(output.records[0], "test_attr", None))
        self.assertEquals(output.records[1].test_attr, "test_data")
        self.assertIsNone(getattr(output.records[2], "test_attr", None))

    def test_protected_attribute(self):
        with self.assertRaises(ValueError):
            set_entry("msecs", 1)


if __name__ == "__main__":
    unittest.main()
