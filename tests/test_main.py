import logging
import unittest

from contextfilter import ContextFilter


class TestSanity(unittest.TestCase):
    def test_sanity(self):
        logger = logging.getLogger("test")
        cfilter = ContextFilter()
        logger.addFilter(cfilter)
        with self.assertLogs(logger, level="INFO") as output:
            logger.info("test1")
            cfilter.set_entries(test_attr="test_data")
            logger.info("test2")
            cfilter.reset()
            logger.info("test3")

        self.assertIsNone(getattr(output.records[0], "test_attr", None))
        self.assertEqual(output.records[1].test_attr, "test_data")
        self.assertIsNone(getattr(output.records[2], "test_attr", None))

    def test_protected_attribute(self):
        cfilter = ContextFilter()
        with self.assertRaises(ValueError):
            cfilter.set_entry("msecs", 1)


if __name__ == "__main__":
    unittest.main()
