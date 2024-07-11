import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class testHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "Paragraph", ["ol", "li", "li"],)
        node2 = HTMLNode("p", "Paragraph", ["ol", "li", "li"],)
        self.assertListEqual(node.children, node2.children)

    def test_eq_None(self):
        node = HTMLNode("h1", "Heading")
        node2 = HTMLNode("b", "bolded words")
        self.assertIsNone(node.props,node2.props)


    def test_eq_props(self):
        node = HTMLNode("a", "Boot.dev", [], {"href":"https://www.google.com","target":"_blank"})
        node2 = HTMLNode("a", "Boot.dev", [], {"href":"https://www.google.com","target":"_blank"})
        self.assertEqual(node.props_to_html(),node2.props_to_html())

    def test_dict_props(self):
        node1 = HTMLNode("a", "Boot.dev", [], {"href":"https://www.tryhackme.com","target":"_blank"})
        node2 = HTMLNode("a", "Boot.dev", [], {"href":"https://www.tryhackme.com","target":"_blank"})
        self.assertDictEqual(node1.props, node2.props)

    def test_to_html_props(self):
        node = HTMLNode("div", "hello, world!", None, {"class": "greeting", "href": "https://boot.dev"},)
        self.assertEqual(node.props_to_html(), ' class="greeting" href="https://boot.dev"',)

class testLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), node2.to_html())
    def test_to_html(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

class testParentNode(unittest.TestCase):
    def test_eq(self):
        node1 = ParentNode(
            "div",
            [
                LeafNode("h1", "Header Text"),
                ParentNode("ul",
                           [
                               LeafNode("li", "Item 1"),
                               LeafNode("li", "Item 2")
                            ]
                ),
                LeafNode("p", "Paragraph text")
            ]
        )
        self.assertEqual(node1.to_html(), "<div><h1>Header Text</h1><ul><li>Item 1</li><li>Item 2</li></ul><p>Paragraph text</p></div>")

    def test_to_html(self):
        node2 = ParentNode(
            "section",
            [
                ParentNode(
                    "div",
                    [
                        LeafNode("p", "Inner paragraph"),
                        ParentNode(
                            "span",
                            [LeafNode(None, "Innermost content")]
                        )
                    ]
                )
            ]
        )
        self.assertEqual(node2.to_html(), "<section><div><p>Inner paragraph</p><span>Innermost content</span></div></section>")
      

if __name__=="__main__":
    unittest.main()
