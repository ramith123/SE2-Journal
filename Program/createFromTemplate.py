import os

# import sys
from datetime import datetime


class FileManager:
    TEMPLATE_FOLDER = "../Template/"
    DAILY_ENTRIES_FOLDER = "./"

    def getMdFilesFromFolder(self, folder=DAILY_ENTRIES_FOLDER):
        mdFiles = []
        mdFiles = self.getMdFilenamesFromFolder(folder)

        return [folder + x + ".md" for x in mdFiles]

    def getMdFilenamesFromFolder(self, folder=DAILY_ENTRIES_FOLDER):
        return [x.replace(".md", "") for x in os.listdir(folder) if x.endswith(".md")]


class DiaryDate:
    DATE_STRING_FORMAT = "%A %d %B, %Y"
    DATE_STRING_FORMAT_FOR_OUTPUT_FILE = "%d%m%Y"
    date = None

    def __init__(self, date=None):
        if date is not None:
            self.date = datetime.strptime(date, self.DATE_STRING_FORMAT_FOR_OUTPUT_FILE)
        else:
            self.date = datetime.now()

    def getDateFormatForOutputfile(self):
        return self.date.strftime(self.DATE_STRING_FORMAT_FOR_OUTPUT_FILE)

    def getLongDateFormat(self):
        return self.date.strftime(self.DATE_STRING_FORMAT)

    # @staticmethod
    # def createDateObj():
    #     return datetime.now()


class DiaryEntry:
    variableList = {}

    def __init__(self, dateObj):
        self.variableList["DiaryDate"] = dateObj.getLongDateFormat()

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
    dateObj = DiaryDate()
    entry = DiaryEntry(dateObj)
    variableList = entry.getVariableList()
    fileManager = FileManager()

    filename = dateObj.getDateFormatForOutputfile()
    templateFile = fileManager.getMdFilesFromFolder(fileManager.TEMPLATE_FOLDER)[0]
    filesInDateEntry = fileManager.getMdFilenamesFromFolder()

    if filename not in filesInDateEntry:
        createNewDataFromTemplate(
            variableList, templateFile, fileManager.DAILY_ENTRIES_FOLDER + filename
        )
