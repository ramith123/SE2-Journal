import os

# import sys
from datetime import datetime


class MdFileManager:
    TEMPLATE_FOLDER = "../Template/"
    DAILY_ENTRIES_FOLDER = "./"

    def __init__(self, folder=DAILY_ENTRIES_FOLDER):
        self.folder = folder
        self.mdFileNamesFromFolder = self.getMdFilenamesFromFolder()
        self.mdFileLocations = self.getMdFilesLocationFromFolder()

    def getMdFilesLocationFromFolder(self):
        return [self.folder + x + ".md" for x in self.mdFileNamesFromFolder]

    def getMdFilenamesFromFolder(self):
        return [
            x.replace(".md", "") for x in os.listdir(self.folder) if x.endswith(".md")
        ]

    def getFileFromLocationWithTitle(self, title):
        if title in self.mdFileNamesFromFolder:
            return self.mdFileLocations[self.mdFileNamesFromFolder.index(title)]
        return None


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


class DiaryEntry(DiaryFile):
    variableList = {}

    def __init__(self, date=datetime.now()):
        super().__init__(date)
        self.variableList["DiaryDate"] = self.getLongDateFormat()

    def getVariableList(self):
        return self.variableList


def getLinesFromFile(file):
    with open(file, "r") as fs:
        return fs.readlines()


def updateVariablesInLineslines(variableList, lines):
    for var in variableList:
        for x, line in enumerate(lines):
            if "<{}>".format(var) in line:
                lines[x] = line.replace("<{}>".format(var), variableList[var])


def createNewDateEntryInLocation(filename, lines):
    with open(filename + ".md", "w") as fs:
        fs.writelines(lines)


def createNewDataFromTemplate(variableList, templateFile, filename):
    lines = getLinesFromFile(templateFile)
    updateVariablesInLineslines(variableList, lines)
    createNewDateEntryInLocation(filename, lines)


if __name__ == "__main__":
    diaryEntry = DiaryEntry("25021999")
    print(diaryEntry.variableList)

    # fileManager = FileManager()

    # templateFile = fileManager.getMdFilesFromFolder(fileManager.TEMPLATE_FOLDER)[0]
    # filesInDateEntry = fileManager.getMdFilenamesFromFolder()

    # if filename not in filesInDateEntry:
    #     createNewDataFromTemplate(
    #         variableList, templateFile, fileManager.DAILY_ENTRIES_FOLDER + filename
    #     )
