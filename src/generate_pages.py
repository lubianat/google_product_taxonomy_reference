from pathlib import Path
from jinja2 import Template
import pandas as pd

HERE = Path(__file__).parent.resolve()
DATA = HERE.parent.joinpath("data").resolve()
DOCS = HERE.parent.joinpath("docs").resolve()


template = Template(DATA.joinpath("index.html.jinja").read_text())

content = """
<p>Unnoficial reference for the Google Product Taxonomy.</p>

<p> Based on  Google_Product_Taxonomy_Version: 2021-09-21 <p>

"""
index_page = template.render(page_content=content)

DOCS.joinpath("index.html").write_text(index_page)

taxonomy = pd.read_csv(
    DATA.joinpath("taxonomy_en_us.csv"),
    on_bad_lines="skip",
    dtype={"id": object},
)


for i, row in taxonomy.iterrows():
    full_label = row["description"]
    content = f"""
    <p>{full_label}</p>
    """
    index_page = template.render(page_content=content)

    try:
        DOCS.joinpath(f"{row['id'].strip()}.html").write_text(index_page)
    except:
        pass
