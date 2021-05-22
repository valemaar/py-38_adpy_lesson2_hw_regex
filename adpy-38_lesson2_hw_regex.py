import re

import csv


def read_file():
    # читаем адресную книгу в формате CSV в список contacts_list
    with open('phonebook_raw.csv', 'r', encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list


def edit_contacts_list():
    # TODO 1: выполните пункты 1-3 ДЗ
    # ваш код
    edited_list = list()
    contacts_list = read_file()
    edited_list.append(contacts_list[0])

    for contact in contacts_list[1:]:
        count = 0
        my_list = list()
        for el in contact:
            try:
                if count < 4:  # lastname,firstname,surname,organization
                    if el != '':
                        pattern = r'[ ]'
                        result = re.split(pattern, el)
                        if len(result) >= 1:
                            a = 0
                            while a < len(result):
                                my_list.append(result[a])
                                a += 1
                    else:
                        if count + 1 > len(my_list):
                            my_list.append('')
                if count == 4:  # position
                    my_list.insert(count, el)
                if count == 5:  # phone number
                    pattern = r'\+?[7,8].*?(\d{3}).*?(\d{3}).*?(\d{2}).*?(\d{2}).*?'
                    substitution = r'+7(\1)\2-\3-\4'
                    result = re.sub(pattern, substitution, el)
                    cut_result = result[:16]
                    if len(result) > 16:  # additional phone number
                        add_numb_pattern = r'.*[доб]+.*?(\d{4}).*'
                        add_result = re.findall(add_numb_pattern, result)
                        result = cut_result + ' доб.' + add_result[0]
                    my_list.insert(count, result)
                if count == 6:  # email
                    my_list.insert(count, el)
            except LookupError:  # перехватываем ошибку в индексе
                print('list index error')
            count += 1
        edited_list.append(my_list)
    return edited_list


def remove_duplicates():
    seen = []  # здесь будем хранить списки пар 'фамилия и имя'
    new_list = list()
    for lst in edit_contacts_list():
        temp = list()
        unique_value = [lst[0], lst[1]]
        if unique_value not in seen:
            temp.extend(lst)
            seen.append(unique_value)
            new_list.append(temp)
        elif unique_value in seen:
            for item in new_list:
                if item[0] == lst[0] and item[0] == lst[0]:
                    counter = range(3, 7)
                    for number in counter:
                        if lst[number] != '' and item[number] == '':
                            item[number] = lst[number]
    return new_list


def write_file():
    # TODO 2: сохраните получившиеся данные в другой файл
    # код для записи файла в формате CSV
    with open("phonebook.csv", "w", encoding='utf-16', newline='') as f:
        datawriter = csv.writer(f, delimiter=',')
    # Вместо contacts_list подставьте свой список
        datawriter.writerows(remove_duplicates())


if __name__ == '__main__':
    read_file()
    edit_contacts_list()
    remove_duplicates()
    write_file()
