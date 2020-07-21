import re
import json


class Parser():

    def parse_links(self, desc) -> str:
        return re.sub(r'([\[]([^\]^\[]*)?[\]])([\(]([^\]^\[]*)?[\)])', r'<a href="\g<4>">\g<2></a>', desc)

    def parse_json(self, content):
        try:
            data = json.loads(content)
            return data
        except json.JSONDecodeError as exc:
            return (False, exc.args)

    def isvalid_string(self, string, allow_empty=False) -> bool:
        if str is not type(string):
            return False
        elif allow_empty is False:
            return bool(string and string.strip())
        else:
            return True

    def parse_file_hierarchy(self, files) -> list:
        parsed_files = []

        epic_count = -1
        for file in files:
            parsed_path = file[file.index('workitems/') + 10:]       # remove '*/workitems/' from path so path is consistent b/t run and test
            parsed_path = parsed_path.replace('\\', '/')             # remove '\\' in windows paths
            parsed_path = re.split('/', parsed_path)

            if (len(parsed_path)) == 3:
                epic_count += 1
                feature_count = -1

                parsed_files.append({'epic': file})
            elif (len(parsed_path)) == 4:
                feature_count += 1
                story_count = -1

                if feature_count == 0:
                    parsed_files[epic_count]["features"] = []

                parsed_files[epic_count]["features"].append({'feature': file})
            elif (len(parsed_path)) == 5:
                story_count += 1
                task_count = -1

                if story_count == 0:
                    parsed_files[epic_count]["features"][feature_count]["stories"] = []

                parsed_files[epic_count]["features"][feature_count]["stories"].append({'story': file})
            elif (len(parsed_path)) == 6:
                task_count += 1

                if task_count == 0:
                    parsed_files[epic_count]["features"][feature_count]["stories"][story_count]["tasks"] = []

                parsed_files[epic_count]["features"][feature_count]["stories"][story_count]["tasks"].append({'task': file})

        return parsed_files
