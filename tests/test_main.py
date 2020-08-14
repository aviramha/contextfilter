import logging
import unittest
from contextvars import ContextVar

from contextfilter import ConstContextFilter, ContextFilter

first_one: ContextVar[str] = ContextVar("first_one")
second_one: ContextVar[str] = ContextVar("second_one")


class TestContextVarSanity(unittest.TestCase):
    def test_sanity(self):
        logger = logging.getLogger("test")
        cfilter = ContextFilter(test_1=first_one, test_2=second_one)
        logger.addFilter(cfilter)
        with self.assertLogs(logger, level="INFO") as output:
            logger.info("test1")
            first_one.set("test_data")
            logger.info("test2")
            second_one.set("test_data2")
            logger.info("test3")

        self.assertFalse(hasattr(output.records[0], "test_attr"))
        self.assertEqual(output.records[1].test_1, "test_data")
        self.assertEqual(output.records[2].test_2, "test_data2")

    def test_protected_attribute(self):
        with self.assertRaises(ValueError):
            ContextFilter(extra=first_one)

    def test_record_attribute_exists(self):
        logger = logging.getLogger("test2")
        cfilter = ContextFilter(lentils=first_one)
        logger.addFilter(cfilter)
        first_one.set("hi")
        with self.assertLogs(logger, level="INFO") as output:
            logger.info("test1", extra={"lentils": "test"})
        self.assertEqual(output.records[0].lentils, "test")


class TestConstFilter(unittest.TestCase):
    def test_sanity(self):
        logger = logging.getLogger("test")
        cfilter = ConstContextFilter(test_1="test_data", test_2="test_data2")
        logger.addFilter(cfilter)
        with self.assertLogs(logger, level="INFO") as output:
            logger.info("test1")
        self.assertEqual(output.records[0].test_1, "test_data")
        self.assertEqual(output.records[0].test_2, "test_data2")

    def test_protected_attribute(self):
        with self.assertRaises(ValueError):
            ConstContextFilter(extra="d")

    def test_record_attribute_exists(self):
        logger = logging.getLogger("test2")
        cfilter = ConstContextFilter(lentils="nooveride")
        logger.addFilter(cfilter)
        with self.assertLogs(logger, level="INFO") as output:
            logger.info("test1", extra={"lentils": "test"})
        self.assertEqual(output.records[0].lentils, "test")


if __name__ == "__main__":
    unittest.main()
