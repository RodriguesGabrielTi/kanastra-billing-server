db = db.getSiblingDB('kanastra_billing');  // Create or switch to the kanastra_billing database

// Create the user with readWrite permissions
db.createUser({
  user: 'mongo_user',
  pwd: 'mongo_password',
  roles: [{ role: 'readWrite', db: 'kanastra_billing' }]
});

// Create the collection with a unique index on debt_id
db.createCollection('billing_debts');  // Creating the collection 'billing_debts'

// Create a unique index on the debt_id field
db.debts.createIndex({ debt_id: 1 }, { unique: true });
