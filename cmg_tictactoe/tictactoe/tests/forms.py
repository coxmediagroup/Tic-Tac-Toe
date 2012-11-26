from django.test import TestCase

from ..forms import GridFormField


class GridFormFieldTestCase(TestCase):

    def test_prepare_value(self):
        grid_str = u'xooxx_xoo'
        prepd_grid_str = GridFormField().prepare_value(grid_str)
        self.assertEqual(prepd_grid_str, u'xoo\r\nxx_\r\nxoo')

    def test_clean_newlines(self):
        grid_str = u'xoo\r\nxx_\r\nxoo'
        clean_grid_str = GridFormField().clean(grid_str)
        self.assertEqual(clean_grid_str, u'xooxx_xoo')

    def test_clean_case(self):
        grid_str = u'Xoo\r\nxx_\r\nxOo'
        clean_grid_str = GridFormField().clean(grid_str)
        self.assertEqual(clean_grid_str, u'xooxx_xoo')
