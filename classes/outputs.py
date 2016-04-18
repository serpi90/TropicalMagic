import xlsxwriter

class PrintOutput:
    def start(self):
        pass

    def write(self, items):
        print "\t".join(map(str,items))

    def stop(self):
        pass

class ExcelOutput:
    def __init__(self, filename, headers):
        self.filename = filename
        self.headers = map(str,headers)
        self.row = 0

    def start(self):
        self.book = xlsxwriter.Workbook(self.filename)
        self.sheet = self.book.add_worksheet("Results")
        self.write( self.headers )

    def write(self, items):
        for item in enumerate(map(str,items)):
            self.sheet.write( self.row, item[0], item[1])
        self.row = self.row + 1

    def stop(self):
        self.book.close()

