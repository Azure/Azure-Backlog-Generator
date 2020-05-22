class MockedFiles():
    @staticmethod
    def _mockCorrectFileSystem(fs):
        fs.create_file('./correct/config.json',
                       contents='{ \
                                    "tags" : [ \
                                        "01_Folder", \
                                        "02_Folder", \
                                        "03_Folder" \
                                    ], \
                                    "roles": [ \
                                        "Infra", \
                                        "AppDev" \
                                    ] \
                                }')
        fs.create_file('./correct/01_epic/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 01_folder", \
                                    "tags": ["01_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./correct/01_epic/attachment.doc')
        fs.create_file('./correct/01_epic/01_feature/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 01_folder/01_folder", \
                                    "tags": ["01_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./correct/01_epic/01_feature/01_story/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 01_folder/01_folder/01_story", \
                                    "tags": ["01_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./correct/01_epic/01_feature/01_story/01_task/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 01_folder/01_folder/01_story/01_task", \
                                    "tags": ["01_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./correct/01_epic/01_feature/01_story/02_task/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 01_folder/01_folder/01_story02_task", \
                                    "tags": ["01_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./correct/01_epic/01_feature/02_story/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 01_folder/01_folder/02_story", \
                                    "tags": ["01_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./correct/01_epic/01_feature/02_story/01_task/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 01_folder/01_folder/02_story/01_task", \
                                    "tags": ["01_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./correct/01_epic/02_feature/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 01_folder/02_folder", \
                                    "tags": ["01_Folder", "02_Folder"], \
                                    "roles": ["AppDev"] \
                                }')
        fs.create_file('./correct/01_epic/03_feature/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 01_folder/03_folder", \
                                    "tags": ["01_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./correct/01_epic/03_feature/attachment.doc')
        fs.create_file('./correct/02_epic/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 02_folder", \
                                    "tags": ["02_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./correct/02_epic/01_feature/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 02_folder/01_folder", \
                                    "tags": ["02_Folder", "01_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./correct/02_epic/01_feature/01_story/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 02_folder/01_folder/01_story", \
                                    "tags": ["02_Folder", "01_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./correct/02_epic/01_feature/01_story/01_task/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 02_folder/01_folder/01_story/01_task", \
                                    "tags": ["02_Folder", "01_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./correct/02_epic/01_feature/01_story/02_task/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 02_folder/01_folder/01_story/02_task", \
                                    "tags": ["02_Folder", "01_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./correct/02_epic/01_feature/02_story/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 02_folder/01_folder/02_story", \
                                    "tags": ["02_Folder", "01_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./correct/02_epic/01_feature/02_story/01_task/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 02_folder/01_folder/02_story", \
                                    "tags": ["02_Folder", "01_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./correct/02_epic/02_feature/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 02_folder/02_folder", \
                                    "tags": ["02_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./correct/03_epic/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 03_folder", \
                                    "tags": ["03_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./correct/03_epic/01_feature/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 03_folder/03_folder", \
                                    "tags": ["03_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./correct/04_epic/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 04_folder", \
                                    "tags": ["03_Folder"], \
                                    "roles": [] \
                                }')

    @staticmethod
    def _mockParentPathHasFileFileSystem(fs):
        fs.create_file('./parentPathHasFile/metadata.json')
        fs.create_file('./parentPathHasFile/01_folder/metadata.json')
        fs.create_file('./parentPathHasFile/01_folder/01_folder/metadata.json')

    @staticmethod
    def _mockPathHasNoMetadataFileSystem(fs):
        fs.create_file('./pathHasNoMetadata/01_folder/01_folder/metadata.json')

    @staticmethod
    def _mockFileList():
        files = [
            './correct/01_epic/metadata.json',
            './correct/01_epic/01_feature/metadata.json',
            './correct/01_epic/01_feature/01_story/metadata.json',
            './correct/01_epic/01_feature/01_story/01_task/metadata.json',
            './correct/01_epic/01_feature/01_story/02_task/metadata.json',
            './correct/01_epic/01_feature/02_story/metadata.json',
            './correct/01_epic/01_feature/02_story/01_task/metadata.json',
            './correct/01_epic/02_feature/metadata.json',
            './correct/01_epic/03_feature/metadata.json',
            './correct/02_epic/metadata.json',
            './correct/02_epic/01_feature/metadata.json',
            './correct/02_epic/01_feature/01_story/metadata.json',
            './correct/02_epic/01_feature/01_story/01_task/metadata.json',
            './correct/02_epic/01_feature/01_story/02_task/metadata.json',
            './correct/02_epic/01_feature/02_story/metadata.json',
            './correct/02_epic/01_feature/02_story/01_task/metadata.json',
            './correct/02_epic/02_feature/metadata.json',
            './correct/03_epic/metadata.json',
            './correct/03_epic/01_feature/metadata.json',
            './correct/04_epic/metadata.json'
        ]

        return files

    @staticmethod
    def _mockConfig():
        return {
            "tags": [
                "01_Folder",
                "02_Folder",
                "03_Folder"
            ],
            "roles": [
                "Infra",
                "AppDev"
            ]
        }

    @staticmethod
    def _mockParsedFileList():
        result = [
            {
                'epic': './correct/01_epic/metadata.json',
                'features': [
                    {
                        'feature': './correct/01_epic/01_feature/metadata.json',
                        'stories': [
                            {
                                'story': './correct/01_epic/01_feature/01_story/metadata.json',
                                'tasks': [
                                    {'task': './correct/01_epic/01_feature/01_story/01_task/metadata.json'},
                                    {'task': './correct/01_epic/01_feature/01_story/02_task/metadata.json'}
                                ]
                            },
                            {
                                'story': './correct/01_epic/01_feature/02_story/metadata.json',
                                'tasks': [
                                    {'task': './correct/01_epic/01_feature/02_story/01_task/metadata.json'}
                                ]
                            }
                        ]
                    },
                    {'feature': './correct/01_epic/02_feature/metadata.json'},
                    {'feature': './correct/01_epic/03_feature/metadata.json'}
                ]
            },
            {
                'epic': './correct/02_epic/metadata.json',
                'features': [
                    {
                        'feature': './correct/02_epic/01_feature/metadata.json',
                        'stories': [
                            {
                                'story': './correct/02_epic/01_feature/01_story/metadata.json',
                                'tasks': [
                                    {'task': './correct/02_epic/01_feature/01_story/01_task/metadata.json'},
                                    {'task': './correct/02_epic/01_feature/01_story/02_task/metadata.json'}
                                ]
                            },
                            {
                                'story': './correct/02_epic/01_feature/02_story/metadata.json',
                                'tasks': [
                                    {'task': './correct/02_epic/01_feature/02_story/01_task/metadata.json'}
                                ]
                            }
                        ]
                    },
                    {'feature': './correct/02_epic/02_feature/metadata.json'}
                ]
            },
            {
                'epic': './correct/03_epic/metadata.json',
                'features': [
                    {'feature': './correct/03_epic/01_feature/metadata.json'}
                ]
            },
            {'epic': './correct/04_epic/metadata.json'}
        ]

        return result
