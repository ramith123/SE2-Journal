import os

# import sys
from datetime import datetime


class DiaryDate:
    DATE_STRING_FORMAT_LONG = "%A %d %B, %Y"
    DATE_STRING_FORMAT_FOR_OUTPUT_FILE = "%d%m%Y"
    date = None
    filename = ""

    def __init__(self, date):
        self.date = date

    def getDateFormatForOutputfile(self):
        return self.date.strftime(self.DATE_STRING_FORMAT_FOR_OUTPUT_FILE)

    def getLongDateFormat(self):
        return self.date.strftime(self.DATE_STRING_FORMAT_LONG)

    # @staticmethod
    # def createDateObj():
    #     return datetime.now()


class DiaryFile(DiaryDate):
    def __init__(self, date):
        if type(date) != datetime:
            date = datetime.strptime(date, super().DATE_STRING_FORMAT_FOR_OUTPUT_FILE)

        super().__init__(date)
        self.filename = self.getDateFormatForOutputfile()


class MdFileManager:
    TEMPLATE_FOLDER = "../Template/"
    DAILY_ENTRIES_FOLDER = "./"
    diaryEntry = None
    templateFile = ""
    lines = []

    def __init__(
        self,
        date=datetime.now(),
        folder=TEMPLATE_FOLDER,
        templateFileName="JournalTemplate1",
        variableList={},
    ):
        self.folder = folder
        self.mdFileNamesFromFolder = self.getMdFilenamesFromFolder()
        self.mdFileLocations = self.getMdFilesLocationFromFolder()
        self.diaryEntry = DiaryFile(date)
        self.templateFile = self.getFileLocationWithTitle(templateFileName)
        self.lines = self.getLinesFromFile()
        self.variableList = variableList
        self.variableList["DiaryDate"] = self.diaryEntry.getLongDateFormat()

    def getMdFilesLocationFromFolder(self):
        return [self.folder + x + ".md" for x in self.mdFileNamesFromFolder]

    def getMdFilenamesFromFolder(self):
        return [
            x.replace(".md", "") for x in os.listdir(self.folder) if x.endswith(".md")
        ]

    def getFileLocationWithTitle(self, title):
        if title in self.mdFileNamesFromFolder:
            return self.mdFileLocations[self.mdFileNamesFromFolder.index(title)]
        return None

    # file manipulation
    def getLinesFromFile(self):
        with open(self.templateFile, "r") as fs:
            return fs.readlines()

    def updateVariablesInLines(self):
        for var in self.variableList:
            for x, line in enumerate(self.lines):
                if "<{}>".format(var) in line:
                    self.lines[x] = line.replace(
                        "<{}>".format(var), self.variableList[var]
                    )

    def createNewDateEntryInLocation(self):
        file = self.DAILY_ENTRIES_FOLDER + self.diaryEntry.filename + ".md"
        if os.path.exists(file):
            os.rename(file, file + datetime.strftime(datetime.now(), "%H%M%S") + ".bck")

        with open(file, "w") as fs:
            fs.writelines(self.lines)

    def createNewDataFromTemplate(self):
        self.updateVariablesInLines()
        self.createNewDateEntryInLocation()


if __name__ == "__main__":
    file = MdFileManager(variableList={"HoursWorked": "7"})
    file.createNewDataFromTemplate()
