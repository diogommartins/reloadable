from unittest import TestCase, mock
from reloadable import configure
from reloadable.decorators import reloadable
from reloadable.config import STOP_CONDITION_EXCEPTION


class ReloadableDecoratorTests(TestCase):
    def setUp(self):
        self.exception_callback = mock.Mock()

    def test_it_recovers_from_exception_until_KeyboardInterrupt(self):
        func = mock.Mock(side_effect=[ValueError, STOP_CONDITION_EXCEPTION])
        reloadable_func = reloadable()(func)

        with self.assertRaises(STOP_CONDITION_EXCEPTION):
            reloadable_func()

        self.assertEqual(func.call_count, 2)

    def test_it_recovers_from_multiple_exceptions_until_KeyboardInterrupt(self):
        exceptions = [ValueError,
                      TypeError,
                      IndexError,
                      KeyError,
                      BrokenPipeError,
                      AttributeError,
                      Exception,
                      STOP_CONDITION_EXCEPTION]
        func = mock.Mock(side_effect=exceptions)
        reloadable_func = reloadable()(func)

        with self.assertRaises(STOP_CONDITION_EXCEPTION):
            reloadable_func()

        self.assertEqual(func.call_count, len(exceptions))

    def test_it_calls_the_exception_callback(self):
        exceptions = [ValueError,
                      TypeError,
                      IndexError,
                      KeyError,
                      BrokenPipeError,
                      AttributeError,
                      Exception,
                      STOP_CONDITION_EXCEPTION]
        func = mock.Mock(side_effect=exceptions)
        mock_callback = mock.Mock()
        reloadable_func = reloadable(exception_callback=mock_callback)(func)

        with self.assertRaises(STOP_CONDITION_EXCEPTION):
            reloadable_func()

        for index, exception_cls in enumerate(exceptions[:-1]):
            self.assertIsInstance(mock_callback.call_args_list[index][0][0],
                                  exception_cls)

    def test_disable_reloadable(self):
        configure(enabled=False)

        @reloadable()
        def not_reloadable():
            raise Exception('Oops')

        with self.assertRaises(Exception) as ex:
            not_reloadable()

        self.assertEqual('Oops', str(ex.exception))

        configure(enabled=True)

    def test_stops_on_custom_stop_condition(self):
        configure(stop_condition_exception=BlockingIOError)

        @reloadable()
        def not_reloadable():
            raise BlockingIOError('Oops')

        with self.assertRaises(BlockingIOError) as ex:
            not_reloadable()

        self.assertEqual('Oops', str(ex.exception))

        configure(enabled=KeyboardInterrupt)
