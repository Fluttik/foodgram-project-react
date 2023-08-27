from pathlib import Path

from borb.pdf import OrderedList
from borb.pdf import Document
from borb.pdf import Page
from borb.pdf import SingleColumnLayout
from borb.pdf import Paragraph
from borb.pdf import PDF
from borb.pdf import Alignment
from borb.pdf.canvas.font.simple_font.true_type_font import TrueTypeFont
from borb.pdf.canvas.color.color import HexColor  
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.image.barcode import Barcode, BarcodeType
from decimal import Decimal
from borb.pdf.canvas.layout.table.flexible_column_width_table import FlexibleColumnWidthTable


def create_pdf(text):
    # create an empty Document
    pdf = Document()
    dir_path = Path(__file__).resolve().parents[1]
    font_path = Path(dir_path, "Arimo-Regular.ttf")
    custom_font = TrueTypeFont.true_type_font_from_file(font_path)
    # add an empty Page
    page = Page()
    pdf.add_page(page)

    # use a PageLayout (SingleColumnLayout in this case)
    layout = SingleColumnLayout(page)

    qr_code = Barcode(
        data="https://github.com/Fluttik",
        width=Decimal(64),
        height=Decimal(64),
        type=BarcodeType.QR,)

    layout.add(Paragraph('Список покупок',
                         font=custom_font,
                         horizontal_alignment=Alignment.CENTERED,
                         font_size=Decimal(20)))

    # layout.add(Paragraph(text,
    #            font=custom_font,
    #            font_size=Decimal(14))
    #            )
    for ingr in text:
        t = (
            f'{ingr["recipe__recipe_ingredients__ingredient__name"]} - '
            f'{ingr["amount"]} '
            f'({ingr["recipe__recipe_ingredients__ingredient__measurement_unit"]}) \n'
        )
        layout.add(Paragraph(t,
                             font=custom_font,
                             font_size=Decimal(14)))

    layout.add(
        FlexibleColumnWidthTable(number_of_columns=2, number_of_rows=1)
        .add(qr_code)
        .add(
            Paragraph(
                """
                Николай Королёв
                Github аккаунт
                """,
                font=custom_font,
                padding_top=Decimal(12),
                respect_newlines_in_text=True,
                font_color=HexColor("#666666"),
                font_size=Decimal(10),
                horizontal_alignment=Alignment.LEFT
            )
        )
        .no_borders()
    )
    with open(Path("file.pdf"), "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, pdf)

    return Path("file.pdf")

