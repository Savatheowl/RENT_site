BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "agencies" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(200) NOT NULL,
	"description"	TEXT,
	"logo"	VARCHAR(255),
	"city"	VARCHAR(100) NOT NULL,
	"phone"	VARCHAR(20),
	"email"	VARCHAR(120),
	"created_at"	DATETIME,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "favorites" (
	"id"	INTEGER NOT NULL,
	"user_id"	INTEGER NOT NULL,
	"property_id"	INTEGER NOT NULL,
	"created_at"	DATETIME,
	PRIMARY KEY("id"),
	UNIQUE("user_id","property_id"),
	FOREIGN KEY("property_id") REFERENCES "properties"("id"),
	FOREIGN KEY("user_id") REFERENCES "users"("id")
);
CREATE TABLE IF NOT EXISTS "properties" (
	"id"	INTEGER NOT NULL,
	"landlord_id"	INTEGER NOT NULL,
	"agency_id"	INTEGER,
	"title"	VARCHAR(200) NOT NULL,
	"description"	TEXT NOT NULL,
	"price"	INTEGER NOT NULL,
	"price_type"	VARCHAR(20) NOT NULL,
	"property_type"	VARCHAR(20) NOT NULL,
	"city"	VARCHAR(100) NOT NULL,
	"address"	VARCHAR(255) NOT NULL,
	"rooms"	INTEGER,
	"area"	FLOAT,
	"floor"	INTEGER,
	"max_floor"	INTEGER,
	"lat"	FLOAT,
	"lng"	FLOAT,
	"status"	VARCHAR(20),
	"created_at"	DATETIME,
	"updated_at"	DATETIME,
	PRIMARY KEY("id"),
	FOREIGN KEY("agency_id") REFERENCES "agencies"("id"),
	FOREIGN KEY("landlord_id") REFERENCES "users"("id")
);
CREATE TABLE IF NOT EXISTS "property_images" (
	"id"	INTEGER NOT NULL,
	"property_id"	INTEGER NOT NULL,
	"filename"	VARCHAR(255) NOT NULL,
	"is_main"	BOOLEAN,
	PRIMARY KEY("id"),
	FOREIGN KEY("property_id") REFERENCES "properties"("id")
);
CREATE TABLE IF NOT EXISTS "requests" (
	"id"	INTEGER NOT NULL,
	"tenant_id"	INTEGER NOT NULL,
	"property_id"	INTEGER NOT NULL,
	"message"	TEXT,
	"status"	VARCHAR(20),
	"created_at"	DATETIME,
	PRIMARY KEY("id"),
	FOREIGN KEY("property_id") REFERENCES "properties"("id"),
	FOREIGN KEY("tenant_id") REFERENCES "users"("id")
);
CREATE TABLE IF NOT EXISTS "reviews" (
	"id"	INTEGER NOT NULL,
	"author_id"	INTEGER NOT NULL,
	"landlord_id"	INTEGER NOT NULL,
	"rating"	INTEGER NOT NULL,
	"text"	TEXT,
	"created_at"	DATETIME,
	UNIQUE("author_id","landlord_id"),
	PRIMARY KEY("id"),
	FOREIGN KEY("author_id") REFERENCES "users"("id"),
	FOREIGN KEY("landlord_id") REFERENCES "users"("id")
);
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER NOT NULL,
	"email"	VARCHAR(120) NOT NULL,
	"password_hash"	VARCHAR(256) NOT NULL,
	"role"	VARCHAR(20) NOT NULL,
	"name"	VARCHAR(100) NOT NULL,
	"phone"	VARCHAR(20),
	"avatar"	VARCHAR(255),
	"is_banned"	BOOLEAN,
	"created_at"	DATETIME,
	UNIQUE("email"),
	PRIMARY KEY("id")
);
COMMIT;
