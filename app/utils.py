import fitz


def extract_text_with_style(pdf_path):
    doc = fitz.open(pdf_path)
    text_with_style = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]

        for b in blocks:
            for l in b["lines"]:
                for s in l["spans"]:
                    text_with_style.append({
                        "text": s["text"],
                        "font_size": s["size"],
                        "font_color": s["color"],
                    })

    return text_with_style


# Example usage

import pprint


def parse_data(extracted_text, custom_style=False):
    title_text = ""
    main_title = ""
    reuslt_text = ""
    text_dict = {}
    if not custom_style:
        text_dict["story"] = []
    for item in extracted_text:

        text = item['text']

        if custom_style:
            if not item['font_color'] == 0:
                if len(reuslt_text) > 0:
                    reuslt_text = main_title + " : " + title_text + " : " + reuslt_text

                    if main_title in list(text_dict.keys()):

                        text_dict[main_title].append(reuslt_text)
                    else:
                        text_dict[main_title] = []

                    reuslt_text = ""

                main_title = text[:-1]

            elif text[0].isdigit() and text[1] == "." and len(text) > 2:
                reuslt_text = main_title + " : " + title_text + " : " + reuslt_text

                if main_title in list(text_dict.keys()):
                    text_dict[main_title].append(reuslt_text)
                else:
                    text_dict[main_title] = []

                title_text = text

                reuslt_text = ""


            elif text[0].isalpha() or text[0].isdigit() or text[0].startswith(" "):
                if text.endswith(":"):
                    reuslt_text += text + " "
                elif text[0].isdigit() and text[1] == ".":
                    reuslt_text += text + " "
                else:
                    reuslt_text += text + ", "

        else:


            text_dict["story"].append(text)

    return text_dict

# pdf_path = "/content/Copy of Foods Reciepe for farbod.pdf"
#
# extracted_text = extract_text_with_style(pdf_path)
# text_dict = parse_data(extracted_text)
#
# pprint.pprint(text_dict)
# print(len(text_dict))
