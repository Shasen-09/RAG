from unstructured.documents.elements import Title


def assign_section(elements):
    current_section = None

    for element in elements:

        text = getattr(element, "text", "").strip()

        if isinstance(element, Title):
            current_section = text

        element.metadata.section = current_section

    return elements
