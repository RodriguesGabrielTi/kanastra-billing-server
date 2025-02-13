#!/bin/bash

# Load environment variables
MONGO_HOST="${MONGO_HOST:-mongo}"
MONGO_PORT="${MONGO_PORT:-27017}"
MONGO_INITDB_ROOT_USERNAME="${MONGO_INITDB_ROOT_USERNAME:-mongo_user}"
MONGO_INITDB_ROOT_PASSWORD="${MONGO_INITDB_ROOT_PASSWORD:-mongo_password}"
APP_DB="${APP_DB:-kanastra_billing}"
APP_USER="${APP_USER:-app_user}"
APP_PASSWORD="${APP_PASSWORD:-app_password}"
COLLECTION_NAME="${COLLECTION_NAME:-billing_debts}"

# Function to wait for MongoDB
wait_for_mongo() {
    echo "⏳ Waiting for MongoDB to be ready..."
    until mongosh --host "$MONGO_HOST" --port "$MONGO_PORT" --eval "db.adminCommand('ping')" &>/dev/null; do
        sleep 3
        echo "🔄 Still waiting for MongoDB..."
    done
    echo "✅ MongoDB is up and running!"
}

# Wait for MongoDB
wait_for_mongo

# Create Database, User, Collection, and Indexes
echo "🚀 Initializing MongoDB database and user..."
mongosh --host "$MONGO_HOST" --port "$MONGO_PORT" -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_INITDB_ROOT_PASSWORD" --authenticationDatabase admin <<EOF
    use $APP_DB;

    db.createUser({
        user: "$APP_USER",
        pwd: "$APP_PASSWORD",
        roles: [{ role: "readWrite", db: "$APP_DB" }]
    });

    db.createCollection("$COLLECTION_NAME");

    db.$COLLECTION_NAME.createIndex({ debt_id: 1 }, { unique: true });

    print("✅ MongoDB database setup completed!");
EOF
