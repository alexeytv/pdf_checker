from pdf_read import pdf_read

ETALON_FILE_NAME = "data/test_task.pdf"
TEST_FILE_NAME = "data/test_task.pdf"

# Читаем данные из файла
reader = pdf_read.open_pdf(ETALON_FILE_NAME)

# Получаем данные из эталонного файла
etalon_dict = pdf_read.extract_dict_from_text(reader.pages[0].extract_text())

# сравниваем схему данных из "другого" файла с эталонным
reader_alternative = pdf_read.open_pdf(TEST_FILE_NAME)
result_dict = pdf_read.pack_to_dict_and_check_pdf_text(reader_alternative.pages[0].extract_text(), list(etalon_dict))

if result_dict["error"] == True:
    print("Ошибка попытки сравнения файла с шаблоном: ", result_dict["message"])
else:
    print("Извлечение и проверка данных прошли успешно.\nРезультат: ", result_dict['data'])
