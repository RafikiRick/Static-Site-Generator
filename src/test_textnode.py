import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)

class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", text_type_bold)
		node2 = TextNode("This is a text node", text_type_bold)
		node3 = TextNode("This is another text node", text_type_italic)
		self.assertEqual(node, node2)
		self.assertIsNone(node.url)
		self.assertNotEqual(node.text_type, node3.text_type)

	def test_eq_false(self):
		node = TextNode("This is a text node", text_type_text)
		node2 = TextNode("This is a text node", text_type_bold)
		self.assertNotEqual(node, node2)

	def test_eq_url(self):
		node = TextNode("This is a text node", text_type_bold, "https://www.boot.dev")
		node2 = TextNode("This is a text node", text_type_bold, "https://www.boot.dev")
		self.assertEqual(node.url, node2.url)

	def test_eq_false2(self):
		node = TextNode("This is a text node", text_type_text)
		node2 = TextNode("This is a text node2", text_type_text)
		self.assertNotEqual(node, node2)

class testTextNodetoHTMLNode(unittest.TestCase):
	def test_eq(self):
		text_node = TextNode(text="Hello World", text_type="text")
		text_node2 = TextNode(text="Link to Boot.dev", text_type="link", url="https")
		self.assertNotEqual(text_node, text_node2)
	
	def test_repr(self):
		node = TextNode("This is a text node", text_type_text, "https://www.boot.dev")
		self.assertEqual("TextNode(This is a text node, text, https://www.boot.dev)",repr(node))


if __name__ == "__main__":
	unittest.main()
