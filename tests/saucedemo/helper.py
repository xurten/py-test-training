def sum_list_of_strings(number_list):
    count = 0
    for element in number_list:
        count = count + int(element)
    return str(count)

def remove_html_tags_from_string(message:str):
    import re
    CLEANR = re.compile('<.*?>')
    clean_text = re.sub(CLEANR, '', message)
    return clean_text