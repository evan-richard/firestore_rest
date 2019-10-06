from firestore_utils import *

class Firestore:

    def client(self, cred):
        return Client(cred)


class Client:

    def __init__(self, cred):
        self.cred = cred

    def collection(self, collection_path):
        return Client.Collection(self.cred, collection_path)
    
    def document(self, document_path):
        return Client.Document(self.cred, document_path)

    def batch(self):
        return Client.Batch(self.cred)


    ### MARK:// these are the Client classes
    class Collection:

        def __init__(self, cred, collection_path):
            self.cred = cred
            self.path = str(collection_path)

        def document(self, document_path):
            return Client.Document(self.cred, self.path + '/' + str(document_path))

        def getPath(self):
            return self.path


    class Document:

        def __init__(self, cred, document_path):
            self.cred = cred
            self.path = str(document_path)

        def collection(self, collection_path):
            return Client.Collection(self.cred, self.path + '/' + str(collection_path))

        def getPath(self):
            return self.path

        def get(self):
            return getDocument(self.cred, self.getPath())

        def set(self, document_data):
            createMultipleDocuments(self.cred, { self.getPath(): document_data })

        def update(self, document_data):
            updateMultipleDocuments(self.cred, { self.getPath(): document_data })

        def delete(self):
            deleteDocument(self.cred, [self.getPath()])


    class Batch:

        def __init__(self, cred):
            self.cred = cred
            self.initBatch()

        def initBatch(self):
            self.batch_request = {
                'set': {},
                'update': {},
                'delete': []
            }

        def getBatch(self):
            return self.batch_request

        def set(self, doc_ref, payload):
            if doc_ref.getPath() in self.batch_request['set']:
                prevPayload = self.batch_request['set'].get(doc_ref.getPath())
                prevPayload.update(payload)
            else:
                self.batch_request['set'].update({ doc_ref.getPath(): payload })

        def update(self, doc_ref, payload):
            if doc_ref.getPath() in self.batch_request['update']:
                prevPayload = self.batch_request['update'].get(doc_ref.getPath())
                prevPayload.update(payload)
            else:
                self.batch_request['update'].update({ doc_ref.getPath(): payload })
        
        def delete(self, doc_ref):
            if doc_ref.getPath() not in self.batch_request['delete']:
                self.batch_request['delete'].append(doc_ref.getPath())

        def commit(self):
            setRequests = self.batch_request['set']
            createMultipleDocuments(self.cred, setRequests)

            updateRequests = self.batch_request['update']
            updateMultipleDocuments(self.cred, updateRequests)

            deleteRequests = self.batch_request['delete']
            deleteDocument(self.cred, deleteRequests)

            self.initBatch()
