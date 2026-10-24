from typing import Any


def normalize_elements(text_chunk, table_units, image_units, formula_units, caption_units) -> list[dict[str, Any]]:
    retrieval_units = []
    for i, chunk in enumerate(text_chunk, 1):
        retrieval_units.append({
            "id": f"text_{i}",
            "type": "text",
            "content": chunk.text,
            "metadata": chunk.metadata.to_dict()})
    for i, table in enumerate(table_units, 1):
        retrieval_units.append({
            "id": f"table_{i}",
            "type": "table",
            "content": table["text"],
            "metadata": table["metadata"]
        })
    for i, image in enumerate(image_units, 1):
        retrieval_units.append({
            "id": f"image_{i}",
            "type": "image",
            "content": image["text"],
            "metadata": image["metadata"]
        })
    for i, formula in enumerate(formula_units, 1):
        retrieval_units.append({
            "id": f"formula_{i}",
            "type": "formula",
            "content": formula["text"],
            "metadata": formula["metadata"]
        })
    for i, caption in enumerate(caption_units, 1):
        retrieval_units.append({
            "id": f"caption_{i}",
            "type": "caption",
            "content": caption["text"],
            "metadata": caption["metadata"]
        })

    return retrieval_units
