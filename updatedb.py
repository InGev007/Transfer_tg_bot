updatesql="""
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER NOT NULL UNIQUE,
	"first_name"	TEXT,
	"last_name"	TEXT,
	"username"	TEXT,
	"language_code"	BLOB,
	"number" TEXT,
	"chatbot"	NUMERIC,
	"priv"	INTEGER,
	PRIMARY KEY("id")
);
INSERT OR IGNORE INTO "users" ("id","username","number","chatbot","priv") VALUES (786607486,'ingev123','+380000000000',0,1);
CREATE TABLE IF NOT EXISTS "faq" (
	"name"	TEXT NOT NULL UNIQUE,
	"text"	TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "nlp" (
	"word"	TEXT NOT NULL UNIQUE,
	"faq"	TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "mat" (
	"mat"	TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "dialoga" (
	"id"	INTEGER UNIQUE,
	"idu"	INTEGER NOT NULL,
	"answer"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "dialog" (
	"idu"	INTEGER NOT NULL,
	"dialog"	INTEGER NOT NULL UNIQUE,
	"answer"	TEXT
);
CREATE TABLE IF NOT EXISTS "commands" (
	"commands"	TEXT NOT NULL UNIQUE,
	"dialog"	TEXT NOT NULL,
	"faq"	TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "dialogt" (
	"id"	INTEGER NOT NULL,
	"text"	TEXT NOT NULL,
	"next"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL
);
INSERT OR IGNORE INTO "faq" ("name","text") VALUES ('price','Цена Украина-Латвия 150евро, Украина-Литва 120евро, Украина-Польша 100евро. Багаж бесплатно. Животные бесплатно. Передача посылки 50евро.');
INSERT OR IGNORE INTO "faq" ("name","text") VALUES ('info','Бот для заказа поездок а так-же просмотра информации о рейсах и текущих ценах на билеты');
INSERT OR IGNORE INTO "nlp" ("word","faq") VALUES ('цена','price');
INSERT OR IGNORE INTO "nlp" ("word","faq") VALUES ('цены','price');
INSERT OR IGNORE INTO "nlp" ("word","faq") VALUES ('стоимость','price');
INSERT OR IGNORE INTO "nlp" ("word","faq") VALUES ('сколько стоит','price');
INSERT OR IGNORE INTO "nlp" ("word","faq") VALUES ('по чём','price');
INSERT OR IGNORE INTO "nlp" ("word","faq") VALUES ('по чем','price');
INSERT OR IGNORE INTO "mat" ("mat") VALUES ('сука');
INSERT OR IGNORE INTO "mat" ("mat") VALUES ('пидар');
INSERT OR IGNORE INTO "mat" ("mat") VALUES ('пидор');
INSERT OR IGNORE INTO "mat" ("mat") VALUES ('гандон');
INSERT OR IGNORE INTO "mat" ("mat") VALUES ('хуй');
INSERT OR IGNORE INTO "mat" ("mat") VALUES ('бля');
INSERT OR IGNORE INTO "commands" ("commands","dialog","faq") VALUES ('price','0','price');
INSERT OR IGNORE INTO "commands" ("commands","dialog","faq") VALUES ('заказ','order','0');
INSERT OR IGNORE INTO "commands" ("commands","dialog","faq") VALUES ('order','order','0');
INSERT OR IGNORE INTO "dialogt" ("id","text","next","name") VALUES (1,'С какого города вас забрать? Например: Шауляй',2,'order');
INSERT OR IGNORE INTO "dialogt" ("id","text","next","name") VALUES (2,'В какой город едем? Например: Киев',3,'order');
INSERT OR IGNORE INTO "dialogt" ("id","text","next","name") VALUES (3,'Ваш номер телефона для связи? Например: +380666256625',4,'order');
INSERT OR IGNORE INTO "dialogt" ("id","text","next","name") VALUES (4,'Спасибо за Вашу запись. Мы обязательно Вас наберём в ближайшее рабочее время.',0,'order');
COMMIT;
"""
