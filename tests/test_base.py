import unittest

from faker import Faker

import config
from pseudonomizer.global_dict import init


class BaseTest(unittest.TestCase):
    __test__ = False

    @classmethod
    def setUp(cls):
        init('../../')
        cls.faker = Faker(config.fake_locale)


if __name__ == '__main__':
    unittest.main()
