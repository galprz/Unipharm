import pyodbc 
import unittest
import logging
from datetime import datetime
from colorama import Fore, Style

padding = 17

class DatabaseQueries:
	def __init__(self):
		server = 'tcp:192.168.100.70' 
		database = 'unip' 
		username = 'techviewer' 
		password = 'XPlnqcN1FH8zt' 
		cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
		self.cursor = cnxn.cursor()

	def get_material(self, location_id, pallet): # whenever we have all parts (material, location, pallet)
		try:
			self.cursor.execute("SELECT SERIALNAME FROM unip.dbo.TECH_WarhsBal WHERE LOCNAME = '" + location_id + "' AND PALLETNAME = '" + pallet + "'")
			for row in self.cursor: 
				return row[0] # returns the result
		except Exception as e:
			logging.exception(e, exc_info=True)
		return None

	def get_material_by_location(self, location_id):
		try:
			self.cursor.execute("SELECT SERIALNAME FROM unip.dbo.TECH_WarhsBal WHERE LOCNAME = '" + location_id + "'")
			for row in self.cursor:
				return row[0] # returns the result
		except Exception as e:
			logging.exception(e, exc_info=True)
		return None

	def get_material_by_pallet(self, pallet):
		try:
			self.cursor.execute("SELECT SERIALNAME FROM unip.dbo.TECH_WarhsBal WHERE PALLETNAME = '" + pallet + "'")
			for row in self.cursor:
				return row[0] # returns the result
		except Exception as e:
			logging.exception(e, exc_info=True)
		return None

	def get_pallet_by_location(self, location):
		try:
			self.cursor.execute("SELECT PALLETNAME FROM unip.dbo.TECH_WarhsBal WHERE LOCNAME = '" + location + "'")
			for row in self.cursor:
				return row[0] # returns the result
		except Exception as e:
			logging.exception(e, exc_info=True)
		return None

	def check_box_status(self, location_id, material_expected, pallet):
		if location_id and material_expected and pallet: # if we have all fields
			material_found = self.get_material(location_id, pallet)
			with open('log.txt', 'a') as outfile:
				outfile.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " | " + location_id.ljust(padding) + " | " + material_expected.ljust(padding) + " | " + pallet + "\n") # write we saw
			if material_expected != material_found: # if we found in the DB a material different from what we saw in the videos
				found = " " + material_found.ljust(padding) + " | " if material_found else " NO_MATERIAL_FOUND | " 
				with open('log_errors.txt', 'a') as outfile:
						outfile.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " | " + location_id.ljust(padding) + " | " + material_expected.ljust(padding) + found + pallet + "\n") # write information including error
				return False
		elif not pallet:
			material_found = self.get_material_by_location(location_id)
			with open('log.txt', 'a') as outfile:
				outfile.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " | " + location_id.ljust(padding) + " | " + material_expected.ljust(padding) + " | NO_PALLET_FOUND\n")
			if material_expected != material_found:
				found = " " + material_found.ljust(padding) + " | " if material_found else " NO_MATERIAL_FOUND | "
				with open('log_errors.txt', 'a') as outfile:
						outfile.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " | " + location_id.ljust(padding) + " | " + material_expected.ljust(padding) + found + "NO_PALLET_FOUND\n")
				return False
		elif not location_id:
			material_found = self.get_material_by_pallet(pallet)
			with open('log.txt', 'a') as outfile:
				outfile.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " | NO_LOCATION_FOUND | " + material_expected.ljust(padding) + " | " + pallet + "\n")
			if material_expected != material_found:
				found = " " + material_found.ljust(padding) + " | " if material_found else " NO_MATERIAL_FOUND | "
				with open('log_errors.txt', 'a') as outfile:
						outfile.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " | NO_LOCATION_FOUND | " + material_expected.ljust(padding) + found + pallet + "\n")
				return False
		elif not material_expected:
			pallet_found = self.get_pallet_by_location(location_id)
			with open('log.txt', 'a') as outfile:
				outfile.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " | " + location_id.ljust(padding) + " | NO_MATERIAL_FOUND | " + pallet + "\n")
			if pallet != pallet_found:
				found = " " + pallet_found.ljust(padding) + " | " if pallet_found else " NO_PALLET_FOUND | "
				with open('log_errors.txt', 'a') as outfile:
						outfile.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " | " + location_id.ljust(padding) + " | " + pallet.ljust(padding) + found + "NO_MATERIAL_FOUND \n")
				return False
		return True


class TestDB(unittest.TestCase):
	def test(self):
		db = DatabaseQueries()
		self.assertTrue(db.check_box_status("D-05-00", "92103005", "W00023823"))
		self.assertFalse(db.check_box_status("C-07-01", "92103007", "W00024864"))
		self.assertTrue(db.check_box_status(None, "201001200", "W00026052"))
		self.assertTrue(db.check_box_status('B-34-06', '201001202', 'W00021413'))
		self.assertTrue(db.check_box_status("D-19-06", "92103009", None))
		self.assertFalse(db.check_box_status(None, "92103090", "W00024897"))
		self.assertFalse(db.check_box_status("D-02-04", None, "W00024838"))
		self.assertFalse(db.check_box_status("E-33-06", "92103011", None))
		self.assertFalse(db.check_box_status("C-11-01", "92103012", "W00025406"))
		self.assertFalse(db.check_box_status("C-35-07", "92103012", "W00025406"))
		self.assertFalse(db.check_box_status(None, "92103013", "W00025414"))
		self.assertFalse(db.check_box_status("D-32-05", None, "W00025415"))
		self.assertFalse(db.check_box_status("E-24-04", "92103013", None))


if __name__ == '__main__':
	unittest.main()
