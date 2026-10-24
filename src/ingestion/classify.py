from unstructured.documents.elements import Text, Table, Image, Title, FigureCaption, Formula, Header, NarrativeText, ListItem


def classify_element(element):
    if isinstance(element, Image):
        return "image"
    if isinstance(element, Table):
        return "table"
    if isinstance(element, Title):
        return "title"
    if isinstance(element, FigureCaption):
        return "caption"
    if isinstance(element, Formula):
        return "formula"
    if isinstance(element, Header):
        return "header"
    if isinstance(element, (Text, NarrativeText, ListItem)):
        return "text"
    return "other"
