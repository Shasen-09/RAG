from .classify import classify_element


def process_image(elements):
    image_units = []

    for element in elements:
        if classify_element(element) != "image":
            continue

        image_units.append({
            "type": "image",
            "text": getattr(element, "text", ""),
            "metadata": element.metadata.to_dict() if hasattr(element.metadata, "to_dict") else {},
            "element": element
        })

    return image_units
