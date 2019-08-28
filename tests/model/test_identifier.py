from unittest import TestCase


from translator_modules.core.data_transfer_model import Identifier

mock_identifier_xmlns = "HGNC"
mock_identifier_object_id = '1234'


def mock_identifier():
    return Identifier(mock_identifier_xmlns, mock_identifier_object_id)


class TestIdentifier(TestCase):

    def test_identifier_creation(self):

        i = mock_identifier()

        self.assertEqual(i.xmlns, mock_identifier_xmlns, 'Identifier xmlns set')
        self.assertEqual(i.object_id, mock_identifier_object_id, 'Identifier object_id set')

    def test_identifier_to_json(self):
        i = mock_identifier()
        print("\n\nIdentifier JSON output: \n", i.to_json())

    def test_curie(self):
        i = mock_identifier()
        self.assertEqual(
            i.curie(),
            mock_identifier_xmlns+":"+mock_identifier_object_id,
            "Identifier CURIE is properly constructed"
        )

    def test_parse_succeed(self):
        test_curie = 'HGNC:4567'
        i = Identifier.parse(test_curie)
        print("\n\nIdentifier JSON output: \n", i.to_json())

    def test_parse_fail(self):
        not_a_curie = 'not a curie'
        try:
            i = Identifier.parse(not_a_curie)
            print("\n\nI should not see this JSON output: \n", i.to_json())
        except RuntimeError as re:
            print("\n", re)
