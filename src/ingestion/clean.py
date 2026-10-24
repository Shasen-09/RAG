from unstructured.documents.elements import Image, Table, Header, Footer


def cleaned_element(elements):
    cleaned = []

    for element in elements:
        page_number = getattr(element.metadata, "page_number", None)
        text = getattr(element, "text", "").strip()
        if isinstance(element, (Image, Table)):
            cleaned.append(element)
        if not text:
            continue
        if isinstance(element, (Footer, Header)):
            continue
        if page_number == 1:
            if text in {
                "3",
                "2023",
                "2",
                "0",
                "1",
                ":",
                "v",
                "arXiv",
                "i",
                "X",
                "r",
                "a",
            }:
                continue
        cleaned.append(element)

    return cleaned
