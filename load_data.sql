USE guest;

LOAD DATA INFILE '/Users/marisa.azevedo/Desktop/basededados trabalho/pt2/csv/launchpad.csv'
INTO TABLE LAUNCHPAD
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';

LOAD DATA INFILE '/Users/marisa.azevedo/Desktop/basededados trabalho/pt2/csv/manufacturer.csv'
INTO TABLE MANUFACTURER
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';

LOAD DATA INFILE '/Users/marisa.azevedo/Desktop/basededados trabalho/pt2/csv/orbit_info.csv'
INTO TABLE ORBIT_INFO
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';

LOAD DATA INFILE '/Users/marisa.azevedo/Desktop/basededados trabalho/pt2/csv/satellite.csv'
INTO TABLE SATELLITE
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';

LOAD DATA INFILE '/Users/marisa.azevedo/Desktop/basededados trabalho/pt2/csv/contacts.csv'
INTO TABLE CONTACTS
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';

LOAD DATA INFILE '/Users/marisa.azevedo/Desktop/basededados trabalho/pt2/csv/role.csv'
INTO TABLE ROLE
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';

LOAD DATA INFILE '/Users/marisa.azevedo/Desktop/basededados trabalho/pt2/csv/satellite_role.csv'
INTO TABLE SATELLITE_ROLE
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
