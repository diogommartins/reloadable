from unittest import TestCase
from reloadable import configure
from reloadable import config


class ConfigureTest(TestCase):
    def setUp(self):
        self.save_old_config()

    def tearDown(self):
        self.restore_old_config()

    def test_changes_config(self):
        setattr(config, 'WTF', True)

        configure(wtf=False)

        self.assertEqual(False, config.WTF)

    def test_searches_only_for_uppercase_configs(self):
        setattr(config, 'wtf', True)

        with self.assertRaises(ValueError) as ex:
            configure(wtf=False)

        self.assertEqual("Option 'WTF' doesn't exist for reloadable",
                         str(ex.exception))

    def test_raises_error_if_option_doesnt_exist(self):
        self.assertRaises(ValueError, configure, spam=1)

    def save_old_config(self):
        self.old_config = self.get_configs()

    def restore_old_config(self):
        # delete all configs
        for config_name, _ in self.get_configs().items():
            delattr(config, config_name)

        # restore old configs
        for config_name, config_value in self.old_config.items():
            setattr(config, config_name, config_value)

    def get_configs(self):
        return {config_name: getattr(config, config_name)
                for config_name in dir(config)}
