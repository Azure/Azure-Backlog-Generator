from .parser import Parser


class Validation():

    def _validateTitle(self, path, meta) -> []:
        if "title" not in meta:
            return (False, f"'title' property not found in metadata '{path}'")
        if not Parser().validString(meta["title"]):
            return (False, f"'title' property not formatted correctly in metadata '{path}'")
        return True

    def _validateDescription(self, path, meta) -> []:
        if "description" not in meta:
            return (False, f"'description' property not found in metadata '{path}'")
        if not Parser().validString(meta["description"]):
            return (False, f"'description' property not formatted correctly in metadata '{path}'")
        return True

    def _validateTags(self, path, meta, config) -> []:
        if "tags" not in meta:
            return (False, f"'tags' property not found in metadata '{path}'")

        if not isinstance(meta["tags"], list):
            return (False, f"'tags' property is not in correct format in metadata '{path}'")

        for prop in meta["tags"]:
            if prop not in config["tags"]:
                return (False, f"invalid tag '{prop}' in metadata '{path}'")

        return True

    def _validateRoles(self, path, meta, config) -> []:
        if "roles" not in meta:
            return (False, f"'roles' property not found in metadata '{path}'")

        if not isinstance(meta["roles"], list):
            return (False, f"'roles' property is not in correct format in metadata '{path}'")

        for prop in meta["roles"]:
            if prop not in config["roles"]:
                return (False, f"invalid role '{prop}' in metadata '{path}'")

        return True

    def validateMetadata(self, path, json, config) -> []:
        if json is None:
            return (False, f"metadata in '{path}' is empty")

        validTitle = self._validateTitle(path, json)
        if (validTitle is not True):
            return validTitle

        validDesc = self._validateDescription(path, json)
        if (validDesc is not True):
            return validDesc

        validTags = self._validateTags(path, json, config)
        if (validTags is not True):
            return validTags

        validRoles = self._validateRoles(path, json, config)
        if (validRoles is not True):
            return validRoles

        return True

    def validateConfig(self, path, json) -> []:
        allowedConfig = [
            "tags",
            "roles"
        ]

        if json is None:
            return (False, f"configuration in '{path}' is empty")

        for key in json.keys():
            if key not in allowedConfig:
                return (False, f"value '{key}' not allowed in configuration '{path}'")

        for key in allowedConfig:
            if key not in json.keys():
                return (False, f"expected value '{key}' not found in configuration '{path}'")

        return True
