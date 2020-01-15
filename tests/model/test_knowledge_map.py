from unittest import TestCase

from ncats.translator.core.knowledge_map import KnowledgeMap as kmap


class TestKnowledgeMap(TestCase):

    def test_valid_module_category(self):
        self.assertTrue(
            kmap.get_the_knowledge_map().known_category("gene"),
            "'gene' is a known BioLink concept category"
        )

    def test_invalid_module_category(self):
        self.assertFalse(
            kmap.get_the_knowledge_map().known_category("ardvaarks"),
            "'ardvaarks' is NOT a known BioLink concept category"
        )

