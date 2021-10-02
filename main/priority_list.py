def get_list(text):
    final_list = []
    symbol_list = text.split(',')
    for i in symbol_list:
        print(i)
        if i.strip(' ').isdigit():
            final_list.append(int(i))
    return final_list
