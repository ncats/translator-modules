from unittest import TestCase

from translator_modules.core.data_transfer_model import Identifier

mock_identifier_xmlns = "HGNC"
mock_identifier_object_id = '3582'
mock_identifier_version = '1'
mock_identifier_name = 'FA complementation group A'
mock_identifier_symbol = 'FANCA'

mock_identifier_xmlns_2 = "MONDO"
mock_identifier_object_id_2= '0019391'
mock_identifier_version_2= '2'
mock_identifier_name_2 = 'Fanconi Anemia'
mock_identifier_symbol_2 = 'FA'


def mock_identifier():
    return Identifier(
        mock_identifier_xmlns,
        mock_identifier_object_id,
        mock_identifier_name,
        mock_identifier_symbol,
        mock_identifier_version,
    )


def mock_identifier_2():
    return Identifier(
        mock_identifier_xmlns_2,
        mock_identifier_object_id_2,
        mock_identifier_name_2,
        mock_identifier_symbol_2,
        mock_identifier_version_2,
    )


class TestIdentifier(TestCase):

    def test_identifier_creation(self):

        i = mock_identifier()

        self.assertEqual(i.xmlns, mock_identifier_xmlns, 'Identifier xmlns set')
        self.assertEqual(i.object_id, mock_identifier_object_id, 'Identifier object_id set')
        self.assertEqual(i.name, mock_identifier_name, 'Identifier name set')
        self.assertEqual(i.symbol, mock_identifier_symbol, 'Identifier symbol set')

    def test_identifier_to_json(self):
        i = mock_identifier()
        print("\n\nIdentifier JSON output: \n", i.to_json())

    def test_curie(self):
        i = mock_identifier()
        self.assertEqual(
            i.curie(),
            mock_identifier_xmlns+':'+mock_identifier_object_id+'.'+mock_identifier_version,
            "Identifier CURIE is properly constructed"
        )

    def test_parse_succeed(self):
        test_curie = mock_identifier_xmlns+":"+mock_identifier_object_id
        i = Identifier.parse(test_curie)
        print("\n\nIdentifier JSON output: \n", i.to_json())

    def test_parse_fail(self):
        not_a_curie = 'not a curie'
        try:
            i = Identifier.parse(not_a_curie)
            print("\n\nI should not see this JSON output: \n", i.to_json())
        except RuntimeError as re:
            print("\n", re)
