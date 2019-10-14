from firestore_utils import *

def test_format_1():
    test_payload = {
        "strTest": "cats",
        "intTest": 5,
        "boolTest": False,
        "doubTest": 5.0,
        "nullTest": None
    }
    update_fields = []
    formatted_payload = formatDictType(test_payload, update_fields)

    assert('strTest' in update_fields)
    assert('intTest' in update_fields)
    assert('boolTest' in update_fields)
    assert('doubTest' in update_fields)
    assert('nullTest' in update_fields)

    assert(formatted_payload == {
        'intTest': {
            'integerValue': 5
        },
        'boolTest': {
            'booleanValue': False
        },
        'strTest': {
            'stringValue': 'cats'
        },
        'doubTest': {
            'doubleValue': 5.0
        },
        'nullTest': {
            "nullValue": None
        }
    })

# def test_format_2():
#     test_payload = {
#         "timestampTest":
#     }
    # update_fields = []
    # formatted_payload = formatDictType(test_payload, update_fields)

def test_format_3():
    test_payload = {
        "arrayTest": ["5", 6, True]
    }
    update_fields = []
    formatted_payload = formatDictType(test_payload, update_fields)
    
    assert('arrayTest' in update_fields)

    assert(formatted_payload == {
        'arrayTest': {
            'arrayValue': {
                "values": [
                    {
                        "stringValue": "5"
                    },
                    {
                        "integerValue": 6
                    },
                    {
                        "booleanValue": True
                    }
                ]
            }
        }
    })

def test_format_4():
    test_payload = {
        "dictTest": {
            "t1": 1,
            "t2": None
        }
    }
    update_fields = []
    formatted_payload = formatDictType(test_payload, update_fields)

    assert('dictTest' in update_fields)
    assert('dictTest.t1' in update_fields)
    assert('dictTest.t2' in update_fields)

    assert(formatted_payload == {
        'dictTest': {
            'mapValue': {
                "fields": {
                    "t1": {
                        "integerValue": 1
                    },
                    "t2": {
                        "nullValue": None
                    }
                }
            }
        }
    })

def test_format_5():
    test_payload = {
        "nestedArrayTest": [
            "1",
            True,
            [1.0, 3, False]
        ],
        "nestedDictTest": {
            "a1": {
                "b1": {
                    "innerTest": None
                },
                "doubTest": 5.0,
                "boolTest": False
            },
            "a2": {
                "strTest": "cats"
            }
        },
        "nestedInceptionTest": {
            "testInnerArray": [
                {
                    "testInnerDict": {
                        "testStr": "cats",
                        "testBool": True
                    }
                },
                5,
                None
            ]
        }
    }
    update_fields = []
    formatted_payload = formatDictType(test_payload, update_fields)

    assert('nestedArrayTest' in update_fields)
    assert('nestedDictTest' in update_fields)
    assert('nestedDictTest.a1' in update_fields)
    assert('nestedDictTest.a1.b1' in update_fields)
    assert('nestedDictTest.a2' in update_fields)
    assert('nestedInceptionTest' in update_fields)

    assert(formatted_payload == {
        'nestedArrayTest': {
            'arrayValue': {
                "values": [
                    {
                        "stringValue": "1"
                    },
                    {
                        "booleanValue": True
                    },
                    {
                        "arrayValue": {
                            "values": [
                                {
                                    "doubleValue": 1.0
                                },
                                {
                                    "integerValue": 3
                                },
                                {
                                    "booleanValue": False
                                }
                            ]
                        }
                    }
                ]
            }
        },
        "nestedDictTest": {
            "mapValue": {
                "fields": {
                    "a1": {
                        "mapValue": {
                            "fields": {
                                "b1": {
                                    "mapValue": {
                                        "fields": {
                                            "innerTest": {
                                                "nullValue": None
                                            }
                                        }
                                    }
                                },
                                "doubTest": {
                                    "doubleValue": 5.0
                                },
                                "boolTest": {
                                    "booleanValue": False
                                }
                            }
                        }
                    },
                    "a2": {
                        "mapValue": {
                            "fields": {
                                "strTest": {
                                    "stringValue": "cats"
                                }
                            }
                        }
                    }
                }
            }
        },
        "nestedInceptionTest": {
            "mapValue": {
                "fields": {
                    "testInnerArray": {
                        "arrayValue": {
                            "values": [
                                {
                                    "mapValue": {
                                        "fields": {
                                            "testInnerDict": {
                                                "mapValue": {
                                                    "fields": {
                                                        "testStr": {
                                                            "stringValue": "cats"
                                                        },
                                                        "testBool": {
                                                            "booleanValue": True
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                },
                                {
                                    "integerValue": 5
                                },
                                {
                                    "nullValue": None
                                }
                            ]
                        }
                    }
                }
            }
        }
    })

def test_format_6():
    test_payload = {
        "strTest": "",
        "intTest": 0,
        "boolTest": False,
        "doubTest": 0.0,
        "nullTest": None,
        "arrayTest": [],
        "dictTest": {}
    }
    update_fields = []
    formatted_payload = formatDictType(test_payload, update_fields)

    assert('strTest' in update_fields)
    assert('intTest' in update_fields)
    assert('boolTest' in update_fields)
    assert('doubTest' in update_fields)
    assert('nullTest' in update_fields)
    assert('arrayTest' in update_fields)
    assert('dictTest' in update_fields)

    assert(formatted_payload == {
        'intTest': {
            'integerValue': 0
        },
        'boolTest': {
            'booleanValue': False
        },
        'strTest': {
            'stringValue': ""
        },
        'doubTest': {
            'doubleValue': 0.0
        },
        'dictTest': {
            'mapValue': {
                'fields': {

                }
            }
        },
        'nullTest': {
            'nullValue': None
        },
        'arrayTest': {
            'arrayValue': {
                'values': [

                ]
            }
        }
    })

def main():
    test_format_1()
    # test_format_2()
    test_format_3()
    test_format_4()
    test_format_5()
    test_format_6()

if __name__ == "__main__":
    main()