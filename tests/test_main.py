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

    def test_multi_filters(self):
        logger1 = logging.getLogger("test")
        logger2 = logging.getLogger("test2")
        cfilter1 = ContextFilter()
        cfilter2 = ContextFilter()
        logger1.addFilter(cfilter1)
        logger2.addFilter(cfilter2)
        cfilter1.set_entries(a=1)
        cfilter2.set_entries(a=2)
        with self.assertLogs(logger1, level="INFO") as output:
            logger1.info("test")
        self.assertEqual(output.records[0].a, 1)

        with self.assertLogs(logger2, level="INFO") as output:
            logger2.info("test")
        self.assertEqual(output.records[0].a, 2)


if __name__ == "__main__":
    unittest.main()
