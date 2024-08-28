"""Test cases for nautobot_capacity_metrics app metric function registry."""

from django.test import TestCase

from nautobot_capacity_metrics import __REGISTRY__, register_metric_func


class RegistryTests(TestCase):
    """Test cases for ensuring the registry is working properly."""

    def test_register_metric_func(self):
        """Ensure the function to add functions to the registry is working properly."""

        def myfunction():
            """Dummy metric function."""

        self.assertRaises(TypeError, register_metric_func, "test")
        self.assertRaises(TypeError, register_metric_func, {"test": "test"})
        self.assertRaises(TypeError, register_metric_func, [1, 2, 3])

        register_metric_func(myfunction)
        self.assertEqual(__REGISTRY__[-1], myfunction)
