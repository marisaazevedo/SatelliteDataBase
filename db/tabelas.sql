USE guest;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS LAUNCHPAD;
DROP TABLE IF EXISTS MANUFACTURER;
DROP TABLE IF EXISTS ORBIT_INFO;
DROP TABLE IF EXISTS SATELLITE;
DROP TABLE IF EXISTS CONTACTS;
DROP TABLE IF EXISTS ROLE;
DROP TABLE IF EXISTS SATELLITE_ROLE;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE IF NOT EXISTS LAUNCHPAD
(
  LaunchpadId     INT NOT NULL AUTO_INCREMENT,
  Name            varchar(255) NOT NULL,
  Location        varchar(255),
  Country         varchar(255) NOT NULL,
  ConstructionYear INT NOT NULL,
  PRIMARY KEY (LaunchpadId)
);

CREATE TABLE IF NOT EXISTS MANUFACTURER
(
  ManufacturerId INT NOT NULL AUTO_INCREMENT,
  Name           longtext NOT NULL,
  Country        longtext NOT NULL,
  Adress         longtext NOT NULL,
  PRIMARY KEY (ManufacturerId)
);

CREATE TABLE IF NOT EXISTS ORBIT_INFO
(
  LaunchId    VARCHAR(255) NOT NULL,
  State       longtext NOT NULL,
  Orbit       longtext,
  Period      longtext,
  Apogee      longtext,
  Perigee     longtext,
  Inclination longtext,
  PRIMARY KEY (LaunchId)
);

CREATE TABLE IF NOT EXISTS SATELLITE
(
  SatelliteId    INT NOT NULL,
  LaunchId       VARCHAR(255) NOT NULL,
  Model          longtext NOT NULL,
  ManufacturerId INT NOT NULL,
  LaunchpadId    INT NOT NULL,
  PRIMARY KEY (SatelliteId),
  FOREIGN KEY (LaunchpadId) REFERENCES LAUNCHPAD(LaunchpadId),
  FOREIGN KEY (ManufacturerId) REFERENCES MANUFACTURER(ManufacturerId),
  FOREIGN KEY (LaunchId) REFERENCES ORBIT_INFO(LaunchId)
);

CREATE TABLE IF NOT EXISTS CONTACTS
(
  ManufacturerId INT NOT NULL AUTO_INCREMENT,
  Number         longtext,
  PRIMARY KEY (ManufacturerId),
  FOREIGN KEY (ManufacturerId) REFERENCES MANUFACTURER(ManufacturerId)
);

CREATE TABLE IF NOT EXISTS ROLE
(
  RoleId  INT NOT NULL AUTO_INCREMENT,
  User    varchar(30) NOT NULL,
  Purpose varchar(30) NOT NULL,
  PRIMARY KEY (RoleId)
);

CREATE TABLE IF NOT EXISTS SATELLITE_ROLE
(
  SatelliteId INT NOT NULL,
  RoleId      INT NOT NULL,
  PRIMARY KEY (SatelliteId, RoleId),
  FOREIGN KEY (SatelliteId) REFERENCES SATELLITE(SatelliteId),
  FOREIGN KEY (RoleId) REFERENCES ROLE(RoleId)
);
