from unittest import TestCase

from django.core.exceptions import ValidationError
from django.core.validators import EMPTY_VALUES


class LocalFlavorTestCase(TestCase):
    def assertFieldOutput(self, fieldclass, valid, invalid):
        """Asserts that a field behaves correctly with various inputs.

        Args:
            fieldclass: the class of the field to be tested.
            valid: a dictionary mapping valid inputs to their expected
                    cleaned values.
            invalid: a dictionary mapping invalid inputs to one or more
                    raised error messages.
        """

        required = fieldclass()
        optional = fieldclass(required=False)
        # test valid inputs
        for input, output in valid.items():
            self.assertEqual(required.clean(input), output)
            self.assertEqual(optional.clean(input), output)
        # test invalid inputs
        for input, errors in invalid.items():
            try:
                required.clean(input)
            except ValidationError, e:
                self.assertTrue(unicode(errors) in unicode(e))
            else:
                self.fail()
            try:
                optional.clean(input)
            except ValidationError, e:
                self.assertTrue(unicode(errors) in unicode(e))
            else:
                self.fail()
        # test required inputs
        error_required = u'This field is required'
        for val in EMPTY_VALUES:
            try:
                required.clean(val)
            except ValidationError, e:
                self.assertTrue(error_required in unicode(e))
            else:
                self.fail()
            self.assertEqual(optional.clean(val), u'')
