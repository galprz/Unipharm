import { firestoreClient, deleteFlag } from "./init-firebase";

class DocumentNotFoundError extends Error {}

class DocumentAlreadyExistsError extends Error {}

export class FirestoreClient {
  private static fieldsExist(
    path: string,
    fields: Array<string>
  ): Promise<boolean> {
    return FirestoreClient.pathExists(path).then((res) => {
      return FirestoreClient.read(path).then((document) => {
        return (
          res &&
          fields.every((field) => Object.keys(document).indexOf(field) > -1)
        );
      });
    });
  }

  private static pathExists(path: string): Promise<boolean> {
    return firestoreClient
      .doc(path)
      .get()
      .then((data: { exists: boolean }) => data.exists);
  }

  static collectionPathExists(path: string): Promise<boolean> {
    return firestoreClient
      .collection(path)
      .limit(1)
      .get()
      .then(query => !query.empty);
  }

  static read(path: string): Promise<JSON> {
    return FirestoreClient.pathExists(path).then((res) => {
      return firestoreClient
        .doc(path)
        .get()
        .then((result: { data: () => any }) => result.data())
        .catch((error) => {
          throw new DocumentNotFoundError();
        });
    });
  }

  static update(path: string, data: JSON): Promise<void> {
    return FirestoreClient.pathExists(path).then((res) => {
      if (!res) {
        throw new DocumentNotFoundError();
      }
      return firestoreClient.doc(path).update(data);
    });
  }

  static create(path: string, data: JSON): Promise<void> {
    return FirestoreClient.pathExists(path).then((res) => {
      if (res) {
        throw new DocumentAlreadyExistsError();
      }
      return firestoreClient.doc(path).set(data);
    });
  }

  static deleteFields(path: string, fields: Array<string>): Promise<void> {
    return FirestoreClient.fieldsExist(path, fields).then((res) => {
      if (!res) {
        throw new DocumentNotFoundError();
      }
      let x: any = {};
      fields.forEach((field) => {
        x[field] = deleteFlag;
      });
      return firestoreClient.doc(path).update(x);
    });
  }

  static deleteDocument(path: string): Promise<void> {
    return FirestoreClient.pathExists(path).then((res) => {
      if (!res) {
        throw new DocumentNotFoundError();
      }
      return firestoreClient.doc(path).delete();
    });
  }
}
