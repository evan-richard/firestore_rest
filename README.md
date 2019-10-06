# Python Firestore REST Package

A simple package to manage requests to and from the Google Cloud Firestore REST api. This package is designed to be used with Python 2.6. If you are using a newer version of python, please refer to https://firebase.google.com/docs/firestore/use-rest-api for the official python SDK.

## Dependencies

Dependencies:

* jwt
* requests

## Documentation

### Authentication

Authentication is managed through the service account keys produced in the Firestore console. See https://firebase.google.com/docs/firestore/quickstart for more information on how to generate and store your private keys.

To begin, you will need to pass your service account keys to *credentials*

```
from firestore_rest import credentials, firestore

credentials.set_credentials("path/to/serviceAccount.json")
credentials.initialize_app()
```

### Client

After authenticating, pass the *credentials* to the Firestore Client. The client manages all requests to and from the Firestore database

```
from firestore_rest import credentials, firestore

credentials.set_credentials("path/to/serviceAccount.json")
credentials.initialize_app()

db = firestore.client(credentials)
```

### Collection

This class represents *Firestore Collections*

To retrieve a reference to a new collection, call the **collection** method of the client.

```
col_ref = db.collection('collectionName')
```

A collection can also be spawned from an instance of a *Document (see below)*

```
col_ref = doc_ref.collection('collectionName')
```

#### Properties

* Path: a collection's path can be retrieve via the getPath() method

```
col_ref.getPath()

# returns the fully-qualified pathname to the collection e.g. 'col/doc/subCol'
```

### Document

This class represents *Firestore Documents*

To retrieve a reference to a new document, call the **document** method of the client.

```
doc_ref = db.document('collectionName/documentName')
```

Similar to a collection, a document can also be spawned from an instance of a *Collection*

```
col_ref = col_ref.document('documentName')
```

#### Properties

* Path: a document's path can be retrieve via the getPath() method

```
doc_ref.getPath()

# returns the fully-qualified pathname to the document e.g. 'col/doc/subCol/subDoc'
```

#### Get

Retrieve a snapshot of the current document.

**get**()

```
doc_ref.get()
```

#### Set

Creates a new document with the specified fields. *Note: if a document already exists with the same pathName, the contents of that document will be replace with the contents of the **set** request*

**set**(payload: dict)

```
doc_ref.set({ 'name' : 'Mario', 'Age' : 24 })
```

#### Update

Updates the document with the specified fields. *Note: if a document already exists with the same pathName, the contents of that document will persist and the contents of the **update** request will be be appended to the document.*

**update**(payload: dict)

```
doc_ref.update({ 'Friends' : ['Peach', 'Toad'] })
```

#### Delete

Deletes the current document. This does nothing if the document does not already exist.

**delete**()

```
doc_ref.delete()
```

### Batch

This is a helper to make batch requests to the Firestore database. Batch requests allow you to update multiple documents at once. Up to 200 records can be altered from each type of request (**set**, **update**, **delete**). *Note: although the batch seemingly commits all requests at once, currently each type of request is a seperate transaction (i.e. all update requests happen in one transaction and all delete requests happen in a seperate transaction)*

To spawn a new batch object

```
batch = db.batch()
```

#### Get

Retrieves the current entries in the batch request.

**getBatch**()

```
batch.getBatch()
```

#### Set

Adds a **set** request to the current batch.

**set**(doc_ref: str, payload: dict)

```
batch.set(doc_ref, { 'name' : 'Mario', 'Age' : 24 })
```

#### Update

Adds an **update** request to the current batch.

**update**(doc_ref: str, payload: dict)

```
batch.update(doc_ref, { 'name' : 'Mario', 'Age' : 24 })
```

#### Delete

Adds a **delete** request to the current batch.

**delete**(doc_ref: str)

```
batch.delete(doc_ref)
```

#### Commit

Commits all current batch requests to the Firestore database. This also clears the batch for the next use.

**commit**()

```
batch.commit()
```

## Contributing

If you would like to help improve/add features to the package. Please feel free to branch off the github repository https://github.com/evan-richard/firestore_rest. I will try to make updates and review merge requests as soon as possible.

## Disclaimer

This software is provided free of charge. The software is not in conjunction with, reviewed by, or a representation of, the Google Cloud Services Platform. It is intended only to be used at the risk of the developer. I am not responsible for lost or corrupted data, and it is recommended that you test your requests in a development environment before altering any production level database.