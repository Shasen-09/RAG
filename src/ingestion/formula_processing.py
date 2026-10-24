from .classify import classify_element


def process_formulas(elements):
    formula_units = []

    for element in elements:
        if classify_element(element) != "formula":
            continue

        formula_units.append({
            "type": "table",
            "text": getattr(element, "text"),
            "metadata": element.metadata.to_dict() if hasattr(element.metadata, "to_dict") else {},
            "element": element
        })
    return formula_units
