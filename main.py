import base64
import fitz


def pdf_from_bytes(bytes_):
    return fitz.Document(filetype="pdf", stream=bytes_)


def pdf_to_svgs(pdf: fitz.Document):
    svgs = []
    mat = fitz.Matrix(120 / 72, 120 / 72)
    for page in pdf.pages():
        page: fitz.DisplayList = page
        pixmap: fitz.Pixmap = page.get_pixmap(matrix=mat)
        img_bytes: bytes = pixmap.tobytes()
        b64_string = base64.b64encode(img_bytes).decode('utf-8')
        svgs.append(b64_string)
    pdf.close()
    return svgs


def pdf_to_html(file_name: str, path: fitz.Document, night=False):
    svgs = pdf_to_svgs(path)
    joined_divs = ""
    for svg in svgs:
        img = f'<img src="data:image/png;base64,{svg}" alt="Red dot" />'
        joined_divs += f"<div>{img}</div>"

    night_css = ""

    if night:
        night_css = \
            """
            <style>
                html{
                    background-color: black;
                }     
                body{
                    background-color: black;
                }             
                img {
                   -webkit-filter: invert(1);
                   filter: invert(1);
               }
           </style>
           """

    return f"<html>" \
           f"<head>" \
           f"<title>{file_name}</title>" \
           f"{night_css}" \
           f"</head>" \
           f"<body>" \
           f"{joined_divs}" \
           f"</body>" \
           f"</html>"
