users_table_query = """
CREATE TABLE users(
id serial,
username varchar(255),
hashed_password varchar(80),
PRIMARY KEY (id)
)"""


messages_table_query = """
CREATE TABLE messages(
from_id integer,
to_id integer,
creation_data timestamp,
PRIMARY KEY (id),
FOREIGN KEY(from_id) REFERENCES users(id)
FOREIGN KEY(to_id) REFERENCES users(id)
)"""

creation_query_list = [users_table_query, messages_table_query]
