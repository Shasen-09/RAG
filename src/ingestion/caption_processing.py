from .classify import classify_element


def process_caption(elements):
    caption_units = []

    for element in elements:
        if classify_element(element) != "caption":
            continue

        caption_units.append({
            "type": "caption",
            "text": getattr(element, "text", ""),
            "metadata": element.metadata.to_dict() if hasattr(element.metadata, "to_dict") else {},
            "element": element
        })

    return caption_units
