from unstructured.chunking.title import chunk_by_title
from .classify import classify_element


def text_chunk(elements):
    text_elements = []
    for element in elements:
        element_type = classify_element(element)

        if element_type in ("text", "title"):
            text_elements.append(element)

    return chunk_by_title(text_elements)
