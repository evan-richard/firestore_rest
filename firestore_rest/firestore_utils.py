import requests
import time
from datetime import datetime
import json

def formatDictType(payload, updateFields, parentKey=''):
    """
        Used to refactor python dictionaries to fit
        the expected format of Firestore.
        
        ***********************************************************
        Supports dictionaries containing the following types:
        None, int, float, string, unicode, boolean, datetime, list, and (nested) dictionaries
        ***********************************************************

        @param payload: python dictionary to be formatted
        @param parentKey: this helps deal with nested dictionaries, do not explicitly use this parameter
        @return formatted Firestore dictionary
    """
    for key in payload.keys():
        updateFields.append(parentKey + str(key))
    data = {}
    for key, val in payload.iteritems():
        valueType = type(val)
        key = str(key)
        if val is None:
            data.update({ key: { 'nullValue': None } })
        elif valueType is int:
            data.update({ key: { 'integerValue': val } })
        elif valueType is float:
            data.update({ key: { 'doubleValue': val } })
        elif valueType is str:
            data.update({ key: { 'stringValue': val } })
        elif valueType is unicode:
            data.update({ key: { 'stringValue': str(val) } })
        elif valueType is bool:
            data.update({ key: { 'booleanValue': val } })
        elif valueType is datetime:
           data.update({ key: { 'timestampValue': str(val).replace(' ', 'T') } })
        elif valueType is list:
            formattedList = formatListType(val, updateFields)
            data.update({ key: { 'arrayValue':  formattedList } })
        elif valueType is dict:
            formattedDict = formatDictType(val, updateFields, (parentKey + key + '.'))
            data.update({ key: { 'mapValue': { 'fields': formattedDict } } })
    return data

def formatListType(lst, updateFields):
    """
        Used to refactor python lists to fit
        the expected format of Firestore.
        
        ***********************************************************
        Supports lists containing the following types:
        None, int, float, string, unicode, boolean, datetime, dictionaries, and (nested) lists
        ***********************************************************

        @param lst: python list to be formatted
        @return formatted Firestore list
    """
    data = {'values': []}
    for val in lst:
        valueType = type(val)
        if val is None:
            data['values'].append({ 'nullValue': None })
        elif valueType is int:
            data['values'].append({ 'integerValue': val })
        elif valueType is float:
            data['values'].append({ 'doubleValue': val })
        elif valueType is str:
            data['values'].append({ 'stringValue': val })
        elif valueType is unicode:
            data['values'].append({ 'stringValue': str(val) })
        elif valueType is bool:
            data['values'].append({ 'booleanValue': val })
        elif valueType is datetime:
            data['values'].append({ 'timestampValue': str(val).replace(' ', 'T') })
        elif valueType is list:
            formattedList = formatListType(val, updateFields)
            data['values'].append({ 'arrayValue': formattedList })
        elif valueType is dict:
            formattedDict = formatDictType(val, updateFields)
            data['values'].append({ 'mapValue': { 'fields': formattedDict } })
    return data

def createFirestoreDataObject(cred, path, fieldData):
    """
        @param path: string representing the path to the document
        (i.e. 'gameChars/mario/friends/luigi' represents the document luigi
        under collection 'friends' inside document 'mario' under collection 'gameChars')

        NOTE: if the path does not exist in the DB, it will be created

        @param fieldData: python dictionary containing data to update fields inside the document
    """
    updateDict = { 'update': {} }

    updateFields = []
    formattedData = formatDictType(fieldData, updateFields)

    updateDict['update']['name'] = cred.base_path + 'documents/{0}'.format(path)
    updateDict['update']['fields'] = formattedData
    updateDict['updateMask'] = { 'fieldPaths': updateFields }

    return updateDict

def makeRequest(cred, url, requestType, body=None, retries=3):
    headers = {
        'Content-type': 'application/json'
    }

    # determine if access token is expired
    if time.time() > cred.claims['exp']:
        cred.get_access_token()

    headers['Authorization'] = 'Bearer {0}'.format(cred.access_token["access_token"])

    if requestType == 'GET':
        resp = requests.get(url, headers=headers, verify=True)
    if requestType == 'PUT':
        if body:
            resp = requests.put(url, headers=headers, data=json.dumps(body), verify=True)
        else:
            resp = requests.put(url, headers=headers, verify=True)
    if requestType == 'POST':
        if body:
            resp = requests.post(url, headers=headers, data=json.dumps(body), verify=True)
        else:
            resp = requests.post(url, headers=headers, verify=True)
    if requestType == 'DELETE':
        resp = requests.delete(url, headers=headers, verify=True)
    
    if resp.status_code == 401 and retries > 0:
        # Need to catch expired access token case
        cred.get_access_token()
        headers['Authorization'] = 'Bearer {0}'.format(cred.access_token["access_token"])
        makeRequest(cred, url, requestType, body, retries-1)
    elif resp.status_code != 200:
        raise RuntimeError("Could not establish connection with firestore. Reason for failure: {0}"\
            .format(resp.content))
    
    return resp.json()


def deleteDocument(cred, documentPaths):
    """
        Delete the document specified at the document path

        @param documentPath: path/to/document
    """
    for documentPath in documentPaths:
        url = cred.base_url + "documents/" + documentPath

        makeRequest(cred, url, 'DELETE')


def runQuery(cred, structuredQuery):
    """
        Run the structured query defined according to the Firestore rest API docs, see NetFlowPingApp getItems()
        function as an example

        @param structuredQuery: query the firestore database according to the structure defined by...
        https://firebase.google.com/docs/firestore/reference/rest/v1/StructuredQuery
    """
    url = cred.base_url + "documents:runQuery"

    makeRequest(cred, url, 'POST', structuredQuery)

def getDocument(cred, documentPath):
    """
        Get the document at the specified path.
    """
    url = cred.base_url + "documents/" + documentPath

    return makeRequest(cred, url, 'GET')
    

def createMultipleDocuments(cred, payload):
    """
        Send the requested payload to Firestore
        authorized with a valid access token.
        Overwrites existing records in document

        @param payload: python dictionary where...
        key=path/to/firestore/document, value=dictionary of field data to patch

        NOTE: as of v1 REST api, Firestore can only update a maximum of 500 fields in one request
    """
    url = cred.base_url + "documents:commit"
    data = { 'writes': [] }

    for path, fieldData in payload.iteritems():
        pathData = createFirestoreDataObject(cred, path, fieldData)
        del pathData['updateMask']
        data['writes'].append(pathData)

    makeRequest(cred, url, 'POST', data)

def updateMultipleDocuments(cred, payload):
    """
        Send the requested payload to Firestore
        authorized with a valid access token.
        Appends data to existing records in document.

        @param payload: python dictionary where...
        key=path/to/firestore/document, value=dictionary of field data to patch

        NOTE: as of v1 REST api, Firestore can only update a maximum of 500 fields in one request

        Example
        **********************************************************************
        {
            'gameChars/mario': {
                'name': 'Mario',
                'age': 23,
                'fiends': ['Peach', 'Bowser']
            },
            'gameChars/luigi': {
                'name': 'Luigi'
            }
        }
        **********************************************************************
    """

    url = cred.base_url + "documents:commit"
    data = { 'writes': [] }

    for path, fieldData in payload.iteritems():
        pathData = createFirestoreDataObject(cred, path, fieldData)
        data['writes'].append(pathData)
    
    makeRequest(cred, url, 'POST', data)