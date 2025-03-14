from bson.objectid import ObjectId


class Case:
    case_collection = None  # Initially None

    @classmethod
    def initialize(cls):
        """Lazy initialization of the case_collection to avoid circular imports."""
        if cls.case_collection is None:
            from mongodb.client import get_case_collection  # Import only when needed

            cls.case_collection = get_case_collection()
            print("Case Collection Initialized: ", cls.case_collection)

    def __init__(
        self,
        case_id,
        title,
        description,
        type_of_crime,
        reported_location,
        reported_datetime,
        investigator_id,
        people_involved,
        evidence,
        event_ids,
        status,
    ):
        self.case_id = case_id
        self.title = title
        self.description = description
        self.type_of_crime = type_of_crime
        self.reported_location = reported_location
        self.reported_datetime = reported_datetime
        self.investigator_id = investigator_id
        self.people_involved = people_involved
        self.evidence = evidence
        self.event_ids = event_ids
        self.status = status

        # Ensure case_id is unique
        self.initialize()
        if self.case_collection.find_one({"case_id": case_id}):
            raise ValueError(f"Case with case_id {case_id} already exists.")

    def save(self):
        case = {
            "case_id": self.case_id,
            "title": self.title,
            "description": self.description,
            "type_of_crime": self.type_of_crime,
            "reported_location": self.reported_location,
            "reported_datetime": self.reported_datetime,
            "investigator_id": self.investigator_id,
            "people_involved": self.people_involved,
            "evidence": self.evidence,
            "event_ids": self.event_ids,
            "status": self.status,
        }
        self.initialize()
        result = self.case_collection.insert_one(case)
        return result.inserted_id

    @classmethod
    def find_all(cls):
        cls.initialize()
        try:
            cases = cls.case_collection.find()
            return list(cases)
        except Exception as e:
            print(e)
            return None

    @classmethod
    def find_by_id(cls, case_id):
        cls.initialize()
        try:
            # Add a return statement here to return the found document
            return cls.case_collection.find_one({"_id": ObjectId(case_id)})
        except Exception as e:
            print(e)
            return None

    @classmethod
    def find_by_case_id(cls, case_id):
        cls.initialize()
        try:
            # Add a return statement here to return the found document
            return cls.case_collection.find_one({"case_id": case_id})
        except Exception as e:
            print(e)
            return None

    @classmethod
    def delete(cls, case_id):
        cls.initialize()
        try:
            result = cls.case_collection.delete_one({"_id": ObjectId(case_id)})
            return result
        except Exception as e:
            print(e)
            return None

    @classmethod
    def update(cls, case_id, data):
        cls.initialize()
        try:
            result = cls.case_collection.update_one(
                {"_id": ObjectId(case_id)}, {"$set": data}
            )
            return result
        except Exception as e:
            print(e)
            return None
