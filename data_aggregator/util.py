from typing import List


def capitalise_text(l: List[str]) -> List[str]:
    new_list = []

    def capitalise(text: str):
        return text[:1].upper() + text[1:].lower()

    for elem in l:
        new_elem = " ".join([capitalise(word) for word in elem.split()])
        new_list.append(new_elem)

    return new_list


def write_to_data_file(company_data: List[str], category: str, file_name: str) -> None:
    file_path = realpath(__file__)
    data_path = "{}/data/{}/{}".format(dirname(dirname(file_path)), category, file_name)
    with open(data_path, "w") as f:
        f.write("\n".join(company_data))
        f.write("\n")
