from unittest import TestCase
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

from reloadable import configure
from reloadable.decorators import reloadable, retry_on_error
from reloadable.config import STOP_CONDITION_EXCEPTION


class ReloadableDecoratorTests(TestCase):
    def setUp(self):
        self.exception_callback = Mock()

    def test_it_recovers_from_exception_until_KeyboardInterrupt(self):
        func = Mock(side_effect=[ValueError, STOP_CONDITION_EXCEPTION], __name__='func')
        reloadable_func = reloadable()(func)

        with self.assertRaises(STOP_CONDITION_EXCEPTION):
            reloadable_func()

        self.assertEqual(func.call_count, 2)

    def test_it_recovers_from_multiple_exceptions_until_KeyboardInterrupt(self):
        exceptions = [ValueError,
                      TypeError,
                      IndexError,
                      KeyError,
                      IOError,
                      AttributeError,
                      Exception,
                      STOP_CONDITION_EXCEPTION]
        func = Mock(side_effect=exceptions, __name__='func')
        reloadable_func = reloadable()(func)

        with self.assertRaises(STOP_CONDITION_EXCEPTION):
            reloadable_func()

        self.assertEqual(func.call_count, len(exceptions))

    def test_it_calls_the_exception_callback(self):
        exceptions = [ValueError,
                      TypeError,
                      IndexError,
                      KeyError,
                      IOError,
                      AttributeError,
                      Exception,
                      STOP_CONDITION_EXCEPTION]
        func = Mock(side_effect=exceptions, __name__='func')
        mock_callback = Mock()
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

    def test_disable_reloadable_works_after_decorator_has_been_applied(self):
        @reloadable()
        def not_reloadable():
            raise Exception('Oops')

        configure(enabled=False)

        with self.assertRaises(Exception) as ex:
            not_reloadable()

        self.assertEqual('Oops', str(ex.exception))

        configure(enabled=True)

    def test_stops_on_custom_stop_condition(self):
        configure(stop_condition_exception=IOError)

        @reloadable()
        def not_reloadable():
            raise IOError('Oops')

        with self.assertRaises(IOError) as ex:
            not_reloadable()

        self.assertEqual('Oops', str(ex.exception))

        configure(stop_condition_exception=KeyboardInterrupt)

    def test_local_stop_condition_preceeds_global_config(self):
        @reloadable(stop_condition_exception=ValueError)
        def not_reloadable():
            raise ValueError('Oops')

        configure(stop_condition_exception=IOError)

        self.assertRaises(ValueError, not_reloadable)

        configure(stop_condition_exception=KeyboardInterrupt)

    def test_it_reloads_function_until_it_reaches_max_reloads(self):
        func = Mock(side_effect=[IOError, IOError, Mock()], __name__='func')
        decorated_func = reloadable(max_reloads=3, return_on_sucess=True)(func)

        decorated_func()

        self.assertEqual(func.call_count, 3)

    def test_it_raises_an_error_if_it_reaches_max_reloads_without_success(self):
        func = Mock(side_effect=IOError, __name__='func')
        decorated_func = reloadable(max_reloads=3)(func)

        with self.assertRaises(IOError):
            decorated_func()

        self.assertEqual(func.call_count, 3)

    def test_it_returns_on_sucess(self):
        expected_result = Mock()
        func = Mock(side_effect=[Exception, expected_result], __name__='func')
        decorated_func = reloadable(max_reloads=3, return_on_sucess=True)(func)

        result = decorated_func()

        self.assertEqual(func.call_count, 2)
        self.assertEqual(expected_result, result)


class RetryOnErrorDecoratorTests(TestCase):
    def test_it_returns_on_sucess(self):
        expected_result = Mock()
        func = Mock(side_effect=[Exception, expected_result], __name__='func')
        decorated_func = retry_on_error(max_reloads=3)(func)

        result = decorated_func()

        self.assertEqual(func.call_count, 2)
        self.assertEqual(expected_result, result)
