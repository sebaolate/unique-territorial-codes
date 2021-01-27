from enum import IntEnum
from xlrd import open_workbook
import pymongo
import os

username = os.environ.get('UNIQUE_TERRITORIAL_CODES_MONGODB_USER')
password = os.environ.get('UNIQUE_TERRITORIAL_CODES_MONGODB_PASS')

# connection_path = "mongodb+srv://{}:{}@unique-territorial-code.o8xa6.mongodb.net/unique_territorial_db?retryWrites=true&w=majority".format(username, password)

connection_path = "mongodb://localhost:27017/unique_territorial_db?retryWrites=true&w=majority".format(username, password)

print("Connecting database..., connection path:")
print(connection_path)

client = pymongo.MongoClient(connection_path)

print("Connected.")

db = client.unique_territorial_db

class Field(IntEnum):
    REGION_CODE = 0
    REGION_NAME  = 1
    REGION_SHORT_NAME = 2    
    PROVINCE_CODE = 3
    PROVINCE_NAME = 4
    COMMUNE_CODE = 5
    COMMUNE_NAME = 6

created_regions = []
created_provinces = []
created_communes = []
region_ids = {}
provinces_ids = {}

def read_excel():
    wb = open_workbook('CUT_2018_v04.xls')
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)

    nrows = sheet.nrows
    ncols = sheet.ncols

    for row in range(1, nrows):
        values = []
        for col in range(ncols):
            values.append(sheet.cell(row,col).value)
        
        if values[Field.REGION_CODE] not in created_regions:
            region = {
                'code': values[Field.REGION_CODE],
                'name': values[Field.REGION_NAME],
                'short_name': values[Field.REGION_SHORT_NAME]
            }
            _id = db.regions.insert_one(region).inserted_id
            region_ids[region['code']] = _id
            created_regions.append(region['code'])

        if values[Field.PROVINCE_CODE] not in created_provinces:
            province = {
                'code': values[Field.PROVINCE_CODE],
                'name': values[Field.PROVINCE_NAME],
                'region_id': region_ids[values[Field.REGION_CODE]]
            }
            _id = db.provinces.insert_one(province).inserted_id
            provinces_ids[province['code']] = _id
            created_provinces.append(province['code'])

        if values[Field.COMMUNE_CODE] not in created_communes:
            commune = {
                'code': values[Field.COMMUNE_CODE],
                'name': values[Field.COMMUNE_NAME],
                'province_id': provinces_ids[values[Field.PROVINCE_CODE]]
            }
            db.communes.insert_one(commune)
            created_communes.append(commune['code'])
        

def main():
    print("Reading excel and importing data...")
    read_excel()
    print("Data imported. Summary:")
    print("")
    print("Regions imported   : {}".format(len(created_regions)))
    print("Provinces imported : {}".format(len(created_provinces)))
    print("Communes imported  : {}".format(len(created_communes)))
    print("")
    print("Finished")

if __name__ == "__main__":
    main()