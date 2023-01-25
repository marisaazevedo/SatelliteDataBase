import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
from flask import abort, render_template, Flask
import logging
import db

APP = Flask(__name__)

# Start Page
@APP.route('/')
def index():
    stats = {}
    x = db.execute('SELECT COUNT(*) AS satellites FROM SATELLITE').fetchone()
    stats.update(x)
    x = db.execute('SELECT COUNT(*) AS launchpads FROM LAUNCHPAD').fetchone()
    stats.update(x)
    x = db.execute('SELECT COUNT(*) AS manufacturer FROM MANUFACTURER').fetchone()
    stats.update(x)
    logging.info(stats)
    return render_template('index.html',stats=stats)

# Satellites
@APP.route('/satellites/')
def list_satellites():
    satellites = db.execute('''
      SELECT SatelliteId, LaunchId, Model, ManufacturerId, LaunchpadId
      FROM SATELLITE
      ORDER BY Model, LaunchId, SatelliteId
      ''').fetchall()
    return render_template('satellite-list.html', satellites=satellites)

@APP.route('/satellites/<int:id>/')
def get_satellite(id):
  satellite = db.execute('''
      SELECT SatelliteId, LaunchId, Model, LaunchpadId, ManufacturerId
      FROM SATELLITE
      WHERE SatelliteId = %s
      ''', id).fetchone()

  if satellite is None:
     abort(404, 'Satellite id {} does not exist.'.format(id))

  manufacturer = db.execute('''
    SELECT Name
    FROM MANUFACTURER NATURAL JOIN SATELLITE
    WHERE SatelliteId = %s
    ''', id).fetchone()

  launchpad = db.execute('''
    SELECT Name
    FROM LAUNCHPAD NATURAL JOIN SATELLITE
    WHERE SatelliteId = %s
    ''', id).fetchone()

  return render_template('satellite-id.html',
            satellite=satellite, manufacturer=manufacturer, launchpad=launchpad)

@APP.route('/satellites/search/<expr>/')
def search_model(expr):
  search = { 'expr': expr }
  expr = '%' + expr + '%'
  satellites = db.execute('''
      SELECT SatelliteId, Model
      FROM SATELLITE
      WHERE Model LIKE %s
      ''', expr).fetchall()
  return render_template('satellite-search.html',
           search=search,satellites=satellites)

# Manufacturer
@APP.route('/manufacturers/')
def list_manufacturers():
    manufacturers = db.execute('''
    SELECT ManufacturerId, Name, Country, Adress, Number
    FROM MANUFACTURER NATURAL JOIN CONTACTS
    ORDER BY Name
    ''').fetchall()
    return render_template('manufacturer-list.html', manufacturers=manufacturers)

@APP.route('/manufacturers/list_satellites/')
def list_manufacturers_satellites():
    manufacturers = db.execute('''
      SELECT COUNT(*) AS Satellites, Name
      FROM SATELLITE JOIN MANUFACTURER ON(SATELLITE.ManufacturerId = MANUFACTURER.ManufacturerId)
      GROUP BY Name
      ORDER BY Satellites, Name;
    ''').fetchall()
    return render_template('manufacturer-list-satellites.html', manufacturers=manufacturers)

@APP.route('/manufacturers/<int:id>/')
def view_satellite_by_manufacturer(id):
  manufacturer = db.execute('''
    SELECT Name ,ManufacturerId, Country, Adress, Number
    FROM MANUFACTURER NATURAL JOIN CONTACTS
    WHERE ManufacturerId = %s
    ''', id).fetchone()

  if manufacturer is None:
     abort(404, 'Manufacturer id {} does not exist.'.format(id))


  satellites = db.execute('''
    SELECT SatelliteId, Model
    FROM SATELLITE
    WHERE ManufacturerId = %s
    ORDER BY Model
    ''', id).fetchall()

  return render_template('manufacturer-id.html',
           manufacturer=manufacturer, satellites=satellites)

@APP.route('/manufacturers/search/<expr>/')
def search_manufacturer(expr):
  search = { 'expr': expr }
  expr = '%' + expr + '%'
  manufacturers = db.execute('''
      SELECT ManufacturerId, Name
      FROM MANUFACTURER
      WHERE Name LIKE %s
    ''', expr).fetchall()

  return render_template('manufacturer-search.html',
           search=search,manufacturers=manufacturers)

# Launchpad
@APP.route('/launchpads/')
def list_launchpads():
    launchpads = db.execute('''
      SELECT LaunchpadId, Name, Location, Country, ConstructionYear
      FROM LAUNCHPAD
      ORDER BY Name
    ''').fetchall()
    return render_template('launchpad-list.html', launchpads=launchpads)

@APP.route('/launchpads/list_satellites/')
def list_launchpads_satellites():
    launchpads = db.execute('''
      SELECT COUNT(*) AS Satellites, Name
      FROM SATELLITE JOIN LAUNCHPAD ON(SATELLITE.LaunchpadId = LAUNCHPAD.LaunchpadId)
      GROUP BY Name
      ORDER BY Satellites, Name;
    ''').fetchall()
    return render_template('launchpad-list-satellites.html', launchpads=launchpads)

@APP.route('/launchpads/<int:id>/')
def view_satellite_by_launchpad(id):
  launchpad = db.execute('''
    SELECT LaunchpadId, Name, Location, Country, ConstructionYear
    FROM LAUNCHPAD
    WHERE LaunchpadId = %s
    ''', id).fetchone()

  if launchpad is None:
     abort(404, 'Launchpad id {} does not exist.'.format(id))

  satellites = db.execute('''
    SELECT SatelliteId, Model
    FROM SATELLITE
    WHERE LaunchpadId = %s
    ORDER BY Model
    ''', id).fetchall()

  return render_template('launchpad-id.html',
          launchpad=launchpad, satellites=satellites)

@APP.route('/launchpads/search/<expr>/')
def search_launchpad(expr):
  search = { 'expr': expr }
  expr = '%' + expr + '%'
  launchpads = db.execute('''
      SELECT LaunchpadId, Name
      FROM LAUNCHPAD
      WHERE Name LIKE %s
    ''', expr).fetchall()
  return render_template('launchpad-search.html',
           search=search,launchpads=launchpads)

#Orbit Info
@APP.route('/orbit_infos/')
def list_orbit_info():
    orbit_info = db.execute('''
      SELECT SatelliteId, Model, LaunchId, State, Orbit, Period, Apogee, Perigee,Inclination
      FROM ORBIT_INFO NATURAL JOIN SATELLITE
      ORDER BY Model, LaunchId
    ''').fetchall()
    return render_template('orbit_info-list.html',orbit_info=orbit_info)

@APP.route('/orbit_infos/<int:id>/')
def view_satellite_by_orbit_info(id):
  orbit_info = db.execute('''
    SELECT SatelliteId, Model, LaunchId, State,Orbit, Period, Apogee, Perigee, Inclination
    FROM ORBIT_INFO NATURAL JOIN SATELLITE
    WHERE SATELLITE.SatelliteId = %s
    ''', id).fetchone()

  if orbit_info is None:
     abort(404, 'Otbit_info id {} does not exist.'.format(id))

  return render_template('orbit_info-id.html',
          orbit_info=orbit_info)

@APP.route('/orbit_infos/search/<expr>/')
def search_orbit_info(expr):
  search = { 'expr': expr }
  expr = '%' + expr + '%'
  orbit_info = db.execute('''
      SELECT SatelliteId, Model, LaunchId, State,Orbit, Period, Apogee, Perigee, Inclination
      FROM ORBIT_INFO NATURAL JOIN SATELLITE
      WHERE State LIKE %s
    ''', expr).fetchall()
  return render_template('orbit_info-search.html',
           search=search,orbit_info=orbit_info)

# Role
@APP.route('/roles/')
def list_role():
    roles = db.execute('''
      SELECT RoleId, User, Purpose
      FROM ROLE
      ORDER BY RoleId
    ''').fetchall()
    return render_template('role-list.html',roles=roles)

@APP.route('/roles/<int:id>/')
def view_satellite_by_role(id):
  roles = db.execute('''
    SELECT RoleId, User, Purpose
    FROM ROLE
    WHERE RoleId = %s
    ''', id).fetchone()

  if roles is None:
     abort(404, 'Role id {} does not exist.'.format(id))

  satellites = db.execute('''
    SELECT SatelliteId, Model
    FROM SATELLITE NATURAL JOIN SATELLITE_ROLE
    WHERE RoleId = %s
    ORDER BY Model
    ''', id).fetchall()
  return render_template('role-id.html',
          roles=roles, satellites=satellites)

@APP.route('/roles/search/user/<expr>/')
def search_role_user(expr):
  search = { 'expr': expr }
  expr = '%' + expr + '%'
  roles = db.execute('''
      SELECT SatelliteId, Model, RoleId, User, Purpose
      FROM ROLE NATURAL JOIN SATELLITE_ROLE NATURAL JOIN SATELLITE
      WHERE User LIKE %s
    ''', expr).fetchall()
  return render_template('role-search-user.html',
           search=search,roles=roles)

@APP.route('/roles/search/purpose/<expr>/')
def search_role_purpose(expr):
  search = { 'expr': expr }
  expr = '%' + expr + '%'
  roles = db.execute('''
      SELECT SatelliteId, Model, RoleId, User, Purpose
      FROM ROLE NATURAL JOIN SATELLITE_ROLE NATURAL JOIN SATELLITE
      WHERE Purpose LIKE %s
    ''', expr).fetchall()
  return render_template('role-search-purpose.html',
           search=search,roles=roles)
