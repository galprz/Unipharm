import { firestoreClient as db } from "../init-firebase";
import { FirestoreClient } from "../firestore";

class CollectionNotFoundError extends Error {}
class MaterialDoesNotExistError extends Error {}

type Loc = number;
type Material = string;

export interface ItemJSON extends JSON {
    loc: Loc;
    material: Material;
}

export class ManagementClient {
    private static readonly acualLocationsPath = "actual_locations";
    private static readonly locField = "loc";
    private static readonly materialField = "material";

    private static docPath(item: ItemJSON): string {
        return this.acualLocationsPath + "/" + item.loc.toString();     // the locations are unique, so they can be the identifiers
    }

    static add(item: ItemJSON): Promise<void> {
        let path = this.docPath(item);
        return FirestoreClient.create(path, item);
    }

    static update(item: ItemJSON): Promise<void> {
        let path = this.docPath(item);
        return FirestoreClient.update(path, item);
    }

    static delete(item: ItemJSON): Promise<void> {
        let path = this.docPath(item);
        return FirestoreClient.deleteDocument(path);
    }

    static getMaterialByLocation(loc: Loc): Promise<Material> {
        return FirestoreClient.collectionPathExists(this.acualLocationsPath)
            .then(
                (exists) => {
                    if (!exists) {
                        throw new CollectionNotFoundError();
                    }
                    let acualLocationsRef = db.collection(this.acualLocationsPath);
                    return acualLocationsRef
                        .where(this.locField, "==", loc)
                        .limit(1)   // it has to be unique anyway
                        .get()
                        .then(
                            (querySnapshot) => {
                                if (querySnapshot.empty) {
                                    throw new MaterialDoesNotExistError();
                                }
                                let doc = querySnapshot.docs[0];
                                return doc.get(this.materialField);
                            }
                        )
                }
            );
    }

    static searchLocationsOfMaterial(material: Material): Promise<Array<Loc>> {
        return FirestoreClient.collectionPathExists(this.acualLocationsPath)
            .then(
                (exists) => {
                    if (!exists) {
                        throw new CollectionNotFoundError();
                    }
                    let acualLocationsRef = db.collection(this.acualLocationsPath);
                    return acualLocationsRef
                        .where(this.materialField, "==", material)
                        .get()
                        .then(
                            (querySnapshot) => {
                                if (querySnapshot.empty) {
                                    throw new MaterialDoesNotExistError();
                                }
                                let locations = new Array<Loc>();
                                querySnapshot.forEach(
                                    (doc) => locations.push(doc.get(this.locField))
                                );
                                return locations;
                            }
                        )
                }
            );
    }
}
