users_table_query = """
CREATE TABLE users(
id serial,
username varchar(255) UNIQUE,
hashed_password varchar(80),
PRIMARY KEY (id)
);"""


messages_table_query = """
CREATE TABLE messages(
id serial,
from_id integer,
to_id integer,
text varchar(255),
creation_data timestamp default current_timestamp,
PRIMARY KEY (id),
FOREIGN KEY(from_id) REFERENCES users(id) ON DELETE CASCADE,
FOREIGN KEY(to_id) REFERENCES users(id) ON DELETE CASCADE
);"""

creation_query_list = [users_table_query, messages_table_query]
