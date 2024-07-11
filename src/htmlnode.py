text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

class HTMLNode:
	def __init__(self, tag=None, value=None, children=None,props=None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def to_html(self):
		raise NotImplementedError("to_html method not implemented")

	def props_to_html(self):
		if self.props is None:
			return ""
		props_html = ""
		for k,v in self.props.items():
			props_html += f' {k}="{v}"'
		return props_html

	def __repr__(self):
		return f"HTMLNode({self.tag},{self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
	def __init__(self, tag, value, props=None):
		super().__init__(tag, value, None, props)

	def to_html(self):
		if self.value is None:
			raise ValueError("No value on leaf")
		if self.tag is None:
			return self.value
		return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

	def __repr__(self):
		return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
	def __init__(self, tag, children, props=None):
		super().__init__(tag, None, children, props)

	def to_html(self):
		if self.tag is None:
			raise ValueError("No tag provided")
		if self.children is None:
			raise ValueError("No children provided")
		
		op_tag = f"<{self.tag}>"
		c_tag = f"</{self.tag}>"

		children_html = ""
		for child in self.children:
			children_html += child.to_html()

		return op_tag + children_html + c_tag
	
	def __repr__(self):
		return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
