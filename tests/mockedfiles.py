class MockedFiles():
    @staticmethod
    def _mock_correct_file_system(fs):
        fs.create_file('./workitems/correct/config.json',
                       contents='{ \
                                    "description": "Sample description", \
                                    "tags" : [ \
                                        "01_Folder", \
                                        "02_Folder", \
                                        "03_Folder" \
                                    ], \
                                    "roles": [ \
                                        "Infra", \
                                        "AppDev" \
                                    ], \
                                    "tagcolors": [ \
                                        "d73a4a", \
                                        "0075ca", \
                                        "cfd3d7", \
                                        "a2eeef", \
                                        "7057ff" \
                                    ] \
                                }')
        fs.create_file('./workitems/correct/01_epic/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 01_folder", \
                                    "tags": ["01_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./workitems/correct/01_epic/attachment.doc')
        fs.create_file('./workitems/correct/01_epic/01_feature/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 01_folder/01_folder", \
                                    "tags": ["01_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./workitems/correct/01_epic/01_feature/01_story/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 01_folder/01_folder/01_story", \
                                    "tags": ["01_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./workitems/correct/01_epic/01_feature/01_story/01_task/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 01_folder/01_folder/01_story/01_task", \
                                    "tags": ["01_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./workitems/correct/01_epic/01_feature/01_story/02_task/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 01_folder/01_folder/01_story02_task", \
                                    "tags": ["01_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./workitems/correct/01_epic/01_feature/02_story/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 01_folder/01_folder/02_story", \
                                    "tags": ["01_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./workitems/correct/01_epic/01_feature/02_story/01_task/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 01_folder/01_folder/02_story/01_task", \
                                    "tags": ["01_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./workitems/correct/01_epic/02_feature/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 01_folder/02_folder", \
                                    "tags": ["01_Folder", "02_Folder"], \
                                    "roles": ["AppDev"] \
                                }')
        fs.create_file('./workitems/correct/01_epic/03_feature/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 01_folder/03_folder", \
                                    "tags": ["01_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./workitems/correct/01_epic/03_feature/attachment.doc')
        fs.create_file('./workitems/correct/02_epic/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 02_folder", \
                                    "tags": ["02_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./workitems/correct/02_epic/01_feature/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 02_folder/01_folder", \
                                    "tags": ["02_Folder", "01_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./workitems/correct/02_epic/01_feature/01_story/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 02_folder/01_folder/01_story", \
                                    "tags": ["02_Folder", "01_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./workitems/correct/02_epic/01_feature/01_story/01_task/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 02_folder/01_folder/01_story/01_task", \
                                    "tags": ["02_Folder", "01_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./workitems/correct/02_epic/01_feature/01_story/02_task/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 02_folder/01_folder/01_story/02_task", \
                                    "tags": ["02_Folder", "01_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./workitems/correct/02_epic/01_feature/02_story/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 02_folder/01_folder/02_story", \
                                    "tags": ["02_Folder", "01_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./workitems/correct/02_epic/01_feature/02_story/01_task/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 02_folder/01_folder/02_story", \
                                    "tags": ["02_Folder", "01_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./workitems/correct/02_epic/02_feature/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 02_folder/02_folder", \
                                    "tags": ["02_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./workitems/correct/03_epic/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 03_folder", \
                                    "tags": ["03_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./workitems/correct/03_epic/01_feature/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 03_folder/03_folder", \
                                    "tags": ["03_Folder"], \
                                    "roles": [] \
                                }')
        fs.create_file('./workitems/correct/04_epic/metadata.json',
                       contents='{ \
                                    "title": "Foo bar", \
                                    "description": "Lorem Ipsum 04_folder", \
                                    "tags": ["03_Folder"], \
                                    "roles": [] \
                                }')

    @staticmethod
    def _mock_parent_path_has_file_file_system(fs):
        fs.create_file('./parentPathHasFile/metadata.json')
        fs.create_file('./parentPathHasFile/01_folder/metadata.json')
        fs.create_file('./parentPathHasFile/01_folder/01_folder/metadata.json')

    @staticmethod
    def _mock_path_has_no_metadata_file_system(fs):
        fs.create_file('./pathHasNoMetadata/01_folder/01_folder/metadata.json')

    @staticmethod
    def _mock_file_list():
        files = [
            './workitems/correct/01_epic/metadata.json',
            './workitems/correct/01_epic/01_feature/metadata.json',
            './workitems/correct/01_epic/01_feature/01_story/metadata.json',
            './workitems/correct/01_epic/01_feature/01_story/01_task/metadata.json',
            './workitems/correct/01_epic/01_feature/01_story/02_task/metadata.json',
            './workitems/correct/01_epic/01_feature/02_story/metadata.json',
            './workitems/correct/01_epic/01_feature/02_story/01_task/metadata.json',
            './workitems/correct/01_epic/02_feature/metadata.json',
            './workitems/correct/01_epic/03_feature/metadata.json',
            './workitems/correct/02_epic/metadata.json',
            './workitems/correct/02_epic/01_feature/metadata.json',
            './workitems/correct/02_epic/01_feature/01_story/metadata.json',
            './workitems/correct/02_epic/01_feature/01_story/01_task/metadata.json',
            './workitems/correct/02_epic/01_feature/01_story/02_task/metadata.json',
            './workitems/correct/02_epic/01_feature/02_story/metadata.json',
            './workitems/correct/02_epic/01_feature/02_story/01_task/metadata.json',
            './workitems/correct/02_epic/02_feature/metadata.json',
            './workitems/correct/03_epic/metadata.json',
            './workitems/correct/03_epic/01_feature/metadata.json',
            './workitems/correct/04_epic/metadata.json'
        ]

        return files

    @staticmethod
    def _mock_config():
        return {
            "description": 'Sample description',
            "tags": [
                "01_Folder",
                "02_Folder",
                "03_Folder"
            ],
            "roles": [
                "Infra",
                "AppDev"
            ],
            "tagcolors": [
                "d73a4a",
                "0075ca",
                "cfd3d7",
                "a2eeef",
                "7057ff"
            ]
        }

    @staticmethod
    def _mock_parsed_file_list():
        result = [
            {
                'epic': './workitems/correct/01_epic/metadata.json',
                'features': [
                    {
                        'feature': './workitems/correct/01_epic/01_feature/metadata.json',
                        'stories': [
                            {
                                'story': './workitems/correct/01_epic/01_feature/01_story/metadata.json',
                                'tasks': [
                                    {'task': './workitems/correct/01_epic/01_feature/01_story/01_task/metadata.json'},
                                    {'task': './workitems/correct/01_epic/01_feature/01_story/02_task/metadata.json'}
                                ]
                            },
                            {
                                'story': './workitems/correct/01_epic/01_feature/02_story/metadata.json',
                                'tasks': [
                                    {'task': './workitems/correct/01_epic/01_feature/02_story/01_task/metadata.json'}
                                ]
                            }
                        ]
                    },
                    {'feature': './workitems/correct/01_epic/02_feature/metadata.json'},
                    {'feature': './workitems/correct/01_epic/03_feature/metadata.json'}
                ]
            },
            {
                'epic': './workitems/correct/02_epic/metadata.json',
                'features': [
                    {
                        'feature': './workitems/correct/02_epic/01_feature/metadata.json',
                        'stories': [
                            {
                                'story': './workitems/correct/02_epic/01_feature/01_story/metadata.json',
                                'tasks': [
                                    {'task': './workitems/correct/02_epic/01_feature/01_story/01_task/metadata.json'},
                                    {'task': './workitems/correct/02_epic/01_feature/01_story/02_task/metadata.json'}
                                ]
                            },
                            {
                                'story': './workitems/correct/02_epic/01_feature/02_story/metadata.json',
                                'tasks': [
                                    {'task': './workitems/correct/02_epic/01_feature/02_story/01_task/metadata.json'}
                                ]
                            }
                        ]
                    },
                    {'feature': './workitems/correct/02_epic/02_feature/metadata.json'}
                ]
            },
            {
                'epic': './workitems/correct/03_epic/metadata.json',
                'features': [
                    {'feature': './workitems/correct/03_epic/01_feature/metadata.json'}
                ]
            },
            {'epic': './workitems/correct/04_epic/metadata.json'}
        ]

        return result
