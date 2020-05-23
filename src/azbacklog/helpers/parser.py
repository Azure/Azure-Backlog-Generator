import re
import json


class Parser():

    def links(self, desc) -> str:
        return re.sub(r'([\[]([^\]^\[]*)?[\]])([\(]([^\]^\[]*)?[\)])', r'<a href="\g<4>">\g<2></a>', desc)

    def json(self, content):
        try:
            data = json.loads(content)
            return data
        except json.JSONDecodeError as exc:
            return (False, exc.args)

    def validString(self, string) -> bool:
        if str is not type(string):
            return False
        else:
            return bool(string and string.strip())

    def fileHierarchy(self, files) -> list:
        parsedFiles = []

        epicCnt = -1
        for file in files:
            parsedPath = file[file.index('workitems/') + 10:]      # remove '*/workitems/' from path so path is consistent b/t run and test
            parsedPath = parsedPath.replace('\\', '/')             # remove '\\' in windows paths
            parsedPath = re.split('/', parsedPath)

            if (len(parsedPath)) == 3:
                epicCnt += 1
                featureCnt = -1

                parsedFiles.append({'epic': file})
            elif (len(parsedPath)) == 4:
                featureCnt += 1
                storyCnt = -1

                if featureCnt == 0:
                    parsedFiles[epicCnt]["features"] = []

                parsedFiles[epicCnt]["features"].append({'feature': file})
            elif (len(parsedPath)) == 5:
                storyCnt += 1
                taskCnt = -1

                if storyCnt == 0:
                    parsedFiles[epicCnt]["features"][featureCnt]["stories"] = []

                parsedFiles[epicCnt]["features"][featureCnt]["stories"].append({'story': file})
            elif (len(parsedPath)) == 6:
                taskCnt += 1

                if taskCnt == 0:
                    parsedFiles[epicCnt]["features"][featureCnt]["stories"][storyCnt]["tasks"] = []

                parsedFiles[epicCnt]["features"][featureCnt]["stories"][storyCnt]["tasks"].append({'task': file})

        return parsedFiles
