from pymongo import MongoClient, errors
import os
import time

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo_user:mongo_password@mongo:27017/kanastra_billing?authSource=admin")


def wait_for_mongo():
    """Waits for MongoDB to be ready."""
    retries = 15
    for i in range(retries):
        try:
            client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
            client.admin.command("ping")  # Ensure authentication works
            print("✅ MongoDB is ready!")
            return client
        except errors.ServerSelectionTimeoutError:
            print(f"⏳ Waiting for MongoDB... ({i+1}/{retries})")
            time.sleep(5)
    raise Exception("❌ MongoDB is not available after multiple attempts.")


def initialize_database():
    """Ensures MongoDB is initialized properly."""
    try:
        client = wait_for_mongo()
        db = client.get_database("kanastra_billing")

        # Explicitly authenticate against admin before listing collections
        client.admin.command("ping")

        # Check if collection exists
        existing_collections = db.list_collection_names()
        if "billing_debts" not in existing_collections:
            db.create_collection("billing_debts")
            print("✅ Collection 'billing_debts' created.")

        # Ensure index exists
        existing_indexes = db.billing_debts.index_information()
        if "debt_id_1" not in existing_indexes:
            db.billing_debts.create_index("debt_id", unique=True)
            print("✅ Unique index on 'debt_id' created.")

        print("🚀 MongoDB initialization completed successfully!")

    except errors.OperationFailure as e:
        print(f"❌ MongoDB authentication failed: {e}")
    except errors.ConnectionFailure as e:
        print(f"❌ MongoDB connection error: {e}")
    except errors.PyMongoError as e:
        print(f"❌ MongoDB initialization error: {e}")


if __name__ == "__main__":
    initialize_database()
