from pathlib import Path

from unstructured.partition.pdf import partition_pdf



def partition_pdf_to_elements(file_path: str):
  path = Path(file_path)

  if not path.exists():
    raise FileNotFoundError("PDF not found: {path}")

  elements = partition_pdf(
    filename=str(path),
    strategy="hi_res",
    infer_table_structure=True,
    extract_image_block_types=['Image'],
    extract_image_block_to_payload=True
  )

  return elements


