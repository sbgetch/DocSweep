from excel.reader import ExcelReader

reader = ExcelReader()

documents = reader.read("input/Drawing Tracker.xlsx")

for document in documents[:10]:
    print(document)