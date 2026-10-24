from .classify import classify_element


def process_table(elements):
    table_units = []

    for element in elements:
        if classify_element(element) != "table":
            continue

        table_units.append({
            "type": "table",
            "text": getattr(element, "text"),
            "metadata": element.metadata.to_dict() if hasattr(element.metadata, "to_dict") else {},
            "element": element
        })
    return table_units
