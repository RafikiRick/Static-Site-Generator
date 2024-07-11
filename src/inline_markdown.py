import re
from textnode import(
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
	text_type_image,
)

def text_to_textnodes(text):
	nodes = [TextNode(text, text_type_text)]
	nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
	nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
	nodes = split_nodes_delimiter(nodes, "`", text_type_code)
	nodes = split_nodes_image(nodes)
	nodes = split_nodes_link(nodes)
	return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
	new_nodes = []
	for node in old_nodes:
		if node.text_type != text_type_text:
			new_nodes.append(node)
			continue
		split_nodes = []
		sections = node.text.split(delimiter)
		if len(sections) % 2 == 0:
			raise ValueError("Invlaid markdown, formatted section not closed")
		for i in range(len(sections)):
			if sections[i] == "":
				continue
			if i % 2 == 0:
				split_nodes.append(TextNode(sections[i], text_type_text))
			else:
				split_nodes.append(TextNode(sections[i], text_type))
		new_nodes.extend(split_nodes)
	return new_nodes

def split_nodes_image(old_nodes):
	new_nodes = []
	for node in old_nodes:
		if node.text_type != text_type_text:
			new_nodes.append(node)
			continue

		images = extract_markdown_images(node.text)
		split_nodes = []
		original_text = node.text
		for image_text, image_url in images:
			parts = original_text.split(f"![{image_text}]({image_url})", 1)

			if parts[0]:
				split_nodes.append(TextNode(parts[0], text_type_text))
			
			split_nodes.append(TextNode(image_text, text_type_image, image_url))
			original_text = parts[-1]
		if original_text:
			split_nodes.append(TextNode(original_text, text_type_text))

		new_nodes.extend(split_nodes)
	return new_nodes
		

def split_nodes_link(old_nodes):
	new_nodes = []
	for node in old_nodes:
		if node.text_type != text_type_text:
			new_nodes.append(node)
			continue
			
		links = extract_markdown_links(node.text)
		split_nodes = []
		original_text = node.text
		for link_text, link_url in links:
			parts = original_text.split(f"[{link_text}]({link_url})",1)

			if parts[0]:
				split_nodes.append(TextNode(parts[0], text_type_text))
			
			split_nodes.append(TextNode(link_text, text_type_link, link_url))
			original_text = parts[-1]
		
		if original_text:
			split_nodes.append(TextNode(original_text, text_type_text))

		new_nodes.extend(split_nodes)
	return new_nodes

def extract_markdown_images(text):
	return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
	return re.findall(r"\[(.*?)\]\((.*?)\)", text)


