# Import built-in modules
from pprint import pformat

# Import third-party modules
from cerberus import Validator

# Import local modules
from rayvision_api.file_operator import read_yaml
from rayvision_api.paths import get_schema_file


class DataValidator(object):
    """The validator of data."""

    def __init__(self, data, schema_name, schema=None):
        self._data = data
        self._schema_name = schema_name
        self._api_version = data.get("api_version", 1)
        self._schema = schema or self._get_schema()

    def _get_schema(self):
        """dict: get the schema form current api version."""
        file_path = get_schema_file(self._schema_name)
        try:
            return read_yaml(file_path)
        except IOError:
            raise ValueError("No schema found that matches the current "
                             "{}.".format(self._schema_name))

    def validate(self, ignore_required=False):
        """Validate itself against the internal schema.

        Args:
            ignore_required (bool): If True, required fields won't be checked.
                Necessary when checking all mappings against the schema.

        Raises:
            ValueError: If validation fails.

        """
        validator = Validator(self._schema)
        validator.allow_unknown = True

        def _validate(dict_, update):
            """Run the actual validator.

            Args:
                dict_ (dict): The data to validate_data.
                update (bool): If True, required fields won't be checked.

            Raises:
                ValueError: If validation fails.

            """
            if not validator.validate(dict_, update=update):
                msg = 'Validation failure(s): {0}'.format(
                    validator.errors)
                raise ValueError(msg)

        _validate(self.data, ignore_required)

    def __repr__(self):
        """dict: Format the main data make it more readable."""
        return pformat(self.data)

    @property
    def data(self):
        return self._data


def validate_data(data, schema_name):
    """Validate the given data.

    Args:
        data (dict): The data to be verified.
        schema_name (str): The name of the schema.

    Returns:
        dict: The validated data.

    """
    config = DataValidator(data, schema_name)
    config.validate()
    return config.data
