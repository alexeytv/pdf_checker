import PyPDF2

class pdf_read:
    def open_pdf(filename):
        # creating a pdf reader object
        reader = PyPDF2.PdfReader(filename)
        return reader

    def extract_dict_from_text(list1):
        list1 = list1.split("\n")
        i = 0
        res_dict = dict()
        while i < len(list1):
            tmp1 = list1[i].strip().partition(":")
            if tmp1[1] == ":":
                if tmp1[2].find(":") > 0:
                    tmp2 = tmp1[2].strip().split(" ")
                    found_separator = False
                    l_part, r_part, separator = "", "", ""
                    f = 0
                    while f < len(tmp2):
                        if tmp2[f].find(":") >= 0:
                            found_separator = True
                            if len(tmp2[f]) > 1:
                                separator = tmp2[f]
                            else:
                                separator = "" + tmp2[f-1] + tmp2[f]
                        elif found_separator:
                            r_part = r_part + tmp2[f]
                        elif (not found_separator):
                            l_part = l_part + tmp2[f]
                        f += 1
                    res_dict[tmp1[0].replace(":","").strip()] = l_part
                    res_dict[separator] = r_part
                else:
                    res_dict[tmp1[0].replace(":","").strip()] = tmp1[2]
            elif len(res_dict) == 0:
                res_dict["COMPANY"] = tmp1[0]
            i += 1
        return res_dict

    def pack_to_dict_and_check_pdf_text(list1, expected_fields):
        # разбиваем текст по строкам
        list1 = list1.split("\n")

        element_for_checking, i = 1, 1
        result_dict = dict()
        result_dict["error"] = False

        if len(list1) == 0:
            result_dict["error"] = True
            result_dict["message"] = "List too short"
            return result_dict

        result_dict["data"] = {"COMPANY": list1[0]}

        while element_for_checking < len(expected_fields):
            if list1[i].find(expected_fields[element_for_checking].strip()) == 0:
                # нашли строку в начале тестируемой строки
                result1 = list1[i].split(expected_fields[element_for_checking])
                if (len(result1) > 0) and (element_for_checking != len(expected_fields)):
                    if result1[1].find(expected_fields[element_for_checking+1].replace(":","").strip()) >= 0:
                        # во второй части строки есть вхождение ещё одного поля, делим строку ещё раз
                        result2 = result1[1].split(expected_fields[element_for_checking+1].strip())
                        result_dict["data"][str(expected_fields[element_for_checking])] = result2[0].strip()
                        if len(result2) > 1:
                            result_dict["data"][str(expected_fields[element_for_checking+1])] = result2[1].strip()
                        else:
                            result_dict["data"][str(expected_fields[element_for_checking+1])] = ""
                        element_for_checking += 1
                    else:
                        result_dict["data"][str(expected_fields[element_for_checking])] = result1[0].strip()
            elif list1[i] != " ":
                # обрабатываемый текст не соответствует шаблону, возвращаем ошибку
                result_dict["error"] = True
                result_dict["message"] = f"The list does not match to expected list. Expected: {expected_fields[element_for_checking]} but found: {list1[i]}"
                return result_dict
            else:
                element_for_checking -= 1
            # смотрим следующий элемент из списка для проверки
            element_for_checking += 1
            # смотрим следующую строку из полученного текста
            i += 1
        result_dict["data"][str(expected_fields[element_for_checking-1])] = list1[i]
        return result_dict
