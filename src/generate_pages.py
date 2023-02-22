from pathlib import Path
from jinja2 import Template
import pandas as pd

HERE = Path(__file__).parent.resolve()
DATA = HERE.parent.joinpath("data").resolve()
DOCS = HERE.parent.joinpath("docs").resolve()


def main():
    content = """
    <p>Unnoficial reference for the Google Product Taxonomy.</p>

    <p> Based on  Google_Product_Taxonomy_Version: 2021-09-21 <p>

    """
    template = Template(DATA.joinpath("index.html.jinja").read_text())

    index_page = template.render(page_content=content)
    DOCS.joinpath("index.html").write_text(index_page)

    code_list = [
        "da-DK",
        "pt-BR",
        "tr-TR",
        "it-IT",
        "de-DE",
        "en-GB",
        "en-AU",
        "es-ES",
        "ja-JP",
        "fr-CH",
        "it-CH",
        "de-CH",
        "fr-FR",
        "pl-PL",
        "nl-NL",
        "cs-CZ",
        "ru-RU",
        "en-US",
        "sv-SE",
        "no-NO",
    ]

    labels = {}
    for code in code_list:
        taxonomy = get_product_df_from_language_code(code)

        for i, row in taxonomy.iterrows():
            if row["id"] in labels:
                labels[row["id"]][code] = row["description"]
            else:
                labels[row["id"]] = {}
                labels[row["id"]][code] = row["description"]

    for key, value in labels.items():
        google_code = key
        dict_for_terms = labels[google_code]

        sorted_keys = sorted(dict_for_terms.keys())
        content = """
        <table>
        <tr>
          <th> Language Code </th>
          <th> Term in language </th>
        </tr>
        
        """
        for language_code in sorted_keys:
            content += f"""
            <tr>
             <td> {language_code}  </td>
             <td> {dict_for_terms[language_code]} </td>
            </tr>            
                """
        content += """
                </table>
"""
        page_for_term = template.render(page_content=content)
        DOCS.joinpath(f"{key}.html").write_text(page_for_term)


def get_product_df_from_language_code(code="en-GB"):
    df = pd.read_excel(
        f"https://www.google.com/basepages/producttype/taxonomy-with-ids.{code}.xls",
        header=None,
    )
    df.columns = "id cat_1 cat_2 cat_3 cat_4 cat_5 cat_6 cat_7".split()
    df["id"] = df["id"].astype(str)

    df["description"] = df[df.columns].apply(
        lambda row: " > ".join(row.values.astype(str)), axis=1
    )

    df["description"] = [a.replace("> nan", "").strip() for a in df["description"]]
    df["description"] = [a.replace(">", "-", 1).strip() for a in df["description"]]

    labels = []
    for i, row in df.iterrows():
        for i in range(7, 0, -1):
            row_name = f"cat_{str(i)}"

            entry = row[row_name]

            if entry == entry:  # test nan
                labels.append(entry)
                break
    df["label"] = labels

    df = df[["id", "description", "label"]]

    return df


if __name__ == "__main__":
    main()
