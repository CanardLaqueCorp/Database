import csv
import os
from datetime import datetime

cars = []
fuelTypes = []
carLineTypes = []
transmissionTypes = []
driveSystemTypes = []
brands = []

bestBioFuel = 0
bestCombinedFuel = 0
bestCombinedCarbon = 10000

# Returns the id of the transmission type and add it to the list if it is a new transmission type
def getTransmissionId(transmissionTypeCode, transmissionTypeLabel) :
    # if we find the transmission in the list we return the id
    for transmissionType in transmissionTypes :
        if (transmissionType['code'] == transmissionTypeCode) :
            return transmissionType['id']
    # if we don't find the transmission in the list we add it and we return the id
    transmissionTypes.append({'id' : len(transmissionTypes) + 1, 'code' : transmissionTypeCode, 'label' : transmissionTypeLabel})
    return len(transmissionTypes)

# Returns the id of the fuel type and add it to the list if it is a new fuel type
def getFuelTypeId(fuelTypeCode, fuelTypeLabel) :
    # if we find the fuel type in the list we return the id
    for fuelType in fuelTypes :
        if (fuelType['code'] == fuelTypeCode) :
            return fuelType['id']
    # if we don't find the fuel type in the list we add it and we return the id
    fuelTypes.append({'id' : len(fuelTypes) + 1, 'code' : fuelTypeCode, 'label' : fuelTypeLabel})
    return len(fuelTypes)

# Returns the id of the carline type and add it to the list if it is a new carline type
def getCarLineId(carLineCode, carLineLabel) :
    # if we find the car line in the list we return the id
    for carLine in carLineTypes :
        if (carLine['code'] == carLineCode) :
            return carLine['id']
    # if we don't find the car line in the list we add it and we return the id
    carLineTypes.append({'id' : len(carLineTypes) + 1, 'code' : carLineCode, 'label' : carLineLabel})
    return len(carLineTypes)

# Returns the id of the drive system and add it to the list if it is a new drive system type
def getDriveSystemId(driveSystemCode, driveSystemLabel) :
    # if we find the drive system in the list we return the id
    for driveSystem in driveSystemTypes :
        if (driveSystem['code'] == driveSystemCode) :
            return driveSystem['id']
    # if we don't find the drive system in the list we add it and we return the id
    driveSystemTypes.append({'id' : len(driveSystemTypes) + 1, 'code' : driveSystemCode, 'label' : driveSystemLabel})
    return len(driveSystemTypes)

# Returns the id of the brand and add it to the list if it is a new brand
def getBrandId(brandLabel) :
    # if we find the brand in the list we return the id
    for brand in brands :
        if (brand['label'] == brandLabel) :
            return brand['id']
    # if we don't find the brand in the list we add it and we return the id
    brands.append({'id' : len(brands) + 1, 'label' : brandLabel})
    return len(brands)

# We read the csv file and we create a list of cars

with open('data/data2023.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    for line in csv_reader:
        line = line[0].split(';')

        maxBioFuel = line[29]
        if (maxBioFuel == ''):
            maxBioFuel = 0
        
        guzzler = line[18]
        if (guzzler == 'G') :
            guzzler = 1
        else :
            guzzler = 0
        
        startAndStop = line[119]
        if (startAndStop == 'Y') :
            startAndStop = 1
        else :
            startAndStop = 0

        # Transimission type

        transmissionTypeCode = line[21]
        transmissionTypeLabel = line[22]
        transmissionTypeId = getTransmissionId(transmissionTypeCode, transmissionTypeLabel)

        # Fuel type

        fuelTypeCode = line[32]
        fuelTypeLabel = line[33]
        fuelTypeId = getFuelTypeId(fuelTypeCode, fuelTypeLabel)

        # Car line

        carLineCode = line[68]
        carLineLabel = line[69]
        carLineId = getCarLineId(carLineCode, carLineLabel)

        # Drive system

        driveSystemCode = line[27]
        driveSystemLabel = line[28]
        driveSystemId = getDriveSystemId(driveSystemCode, driveSystemLabel)

        # Brand

        brandId = getBrandId(line[2])
            
        # We create a car object using the right data

        car = {
            'brandId': brandId,
            'model': line[3],
            'cylinder': line[7],
            'transmission': line[8],
            'transmissionTypeId': transmissionTypeId,
            'driveSystemId' : driveSystemId,
            'gears': line[24],
            'cityFuel': line[15],
            'highwayFuel': line[16],
            'combinedFuel': line[17],
            'guzzler': guzzler,
            'startAndStop': startAndStop,
            'maxBioFuel': maxBioFuel,
            'fuelTypeId': fuelTypeId,
            'annualFuelCost': line[44],
            'carLineId': carLineId,
            'fuelRate' : line[131],
            'ghgRate' : line[132],
            'smogRate' : line[135],
            'spendOnFiveYears' : line[151],
            'cityCarbon' : line[152],
            'highwayCarbon' : line[153],
            'combinedCarbon' : line[154],
        }

        if (car['combinedFuel'] != '' and float(car['combinedFuel']) > bestCombinedFuel) :
            bestCombinedFuel = float(car['combinedFuel'])
        
        if (car['combinedCarbon'] != '' and float(car['combinedCarbon']) < bestCombinedCarbon) :
            bestCombinedCarbon = float(car['combinedCarbon'])

        if (car['maxBioFuel'] != '' and float(car['maxBioFuel']) > bestBioFuel) :
            bestBioFuel = float(car['maxBioFuel'])

        cars.append(car)


    # move the files from the "exports" directory to the "old_exports" directory

    for file in os.listdir('exports'):
        os.rename('exports/' + file, 'old_exports/' + file)

    # We create the sql script fro the cars_th table

    script = ""
    bestBioFuel = float(bestBioFuel)
    bestCombinedFuel = float(bestCombinedFuel)
    bestCombinedCarbon = float(bestCombinedCarbon)
    for car in cars :

        # We calculate the eco score

        bioFuelDelta = float(car['maxBioFuel']) / bestBioFuel
        combinedFuelDelta = float(car['combinedFuel']) / bestCombinedFuel
        combinedCarbonDelta = 1 - bestCombinedCarbon / float(car['combinedCarbon'])
        fuelRate = float(car['fuelRate']) / 10
        ghgRate = float(car['ghgRate']) / 10
        smogRate = float(car['smogRate']) / 10

        ecoScore = bioFuelDelta + 2 * combinedFuelDelta + 2 * combinedCarbonDelta + 3 * fuelRate + 3 * ghgRate + 3 * smogRate
        ecoScore = ecoScore / 14

        if(int(car['startAndStop']) == 1) :
            ecoScore *= 1.05
        
        if(int(car['guzzler']) == 1) :
            ecoScore *= 0.95

        ecoScore = round(ecoScore * 100)

        if (ecoScore > 100) :
            ecoScore = 100

        script += "INSERT INTO car_th (eco_score, car_transmission_type_id, car_drive_system_id, car_fuel_id, car_line_type_id, car_brand_id, model, cylinder, car_transmission, city_fuel, highway_fuel, combined_fuel, has_guzzler, gears, max_bio_fuel, annual_fuel_cost, spend_on_five_years, has_start_and_stop, fe_rating, ghg_rating, smog_rating, city_carbon, highway_carbon, combined_carbon) VALUES "
        script += "(" + str(ecoScore) + ", " + str(car['transmissionTypeId']) + ", " + str(car['driveSystemId']) + ", " + str(car['fuelTypeId']) + ", " + str(car['carLineId']) + ", " + str(car['brandId']) + ", '" + car['model'] + "', '" + car['cylinder'] + "', '" + car['transmission'] + "', '" + car['cityFuel'] + "', '" + car['highwayFuel'] + "', '" + car['combinedFuel'] + "', '" + str(car['guzzler']) + "', '" + car['gears'] + "', '" + str(car['maxBioFuel']) + "', '" + car['annualFuelCost'] + "', '" + car['spendOnFiveYears'] + "', '" + str(car['startAndStop']) + "', '" + car['fuelRate'] + "', '" + car['ghgRate'] + "', '" + car['smogRate'] + "', '" + car['cityCarbon'] + "', '" + car['highwayCarbon'] + "', '" + car['combinedCarbon'] + "');\n"
    
    # We create the file
    
    now = datetime.now()
    fileName = "carsTH-" + now.strftime("%d%m%Y%H%M%S") + ".sql"
    file = open('exports/' + fileName, 'w')
    file.write(script)
    file.close()

    # we create the sql script for the car_transmission table

    script = ""
    for transmissionType in transmissionTypes :
        script += "INSERT INTO transmission (id, code, label) VALUES "
        script += "(" + str(transmissionType['id']) + ", '" + transmissionType['code'] + "', '" + transmissionType['label'] + "');\n"

    # We create the file

    now = datetime.now()
    fileName = "transmissions-" + now.strftime("%d%m%Y%H%M%S") + ".sql"
    file = open('exports/' + fileName, 'w')
    file.write(script)
    file.close()

    # we create the sql script for the fuel table

    script = ""
    for fuelType in fuelTypes :
        script += "INSERT INTO fuel (id, code, label) VALUES "
        script += "(" + str(fuelType['id']) + ", '" + fuelType['code'] + "', '" + fuelType['label'] + "');\n"

    # We create the file

    now = datetime.now()
    fileName = "fuels-" + now.strftime("%d%m%Y%H%M%S") + ".sql"
    file = open('exports/' + fileName, 'w')
    file.write(script)

    # we create the sql script for the car_type table

    script = ""
    for carLine in carLineTypes :
        script += "INSERT INTO car_type (id, label) VALUES "
        script += "(" + str(carLine['id']) + ", '" + carLine['label'] + "');\n"

    # We create the file

    now = datetime.now()
    fileName = "carTypes-" + now.strftime("%d%m%Y%H%M%S") + ".sql"
    file = open('exports/' + fileName, 'w')
    file.write(script)
    file.close()


    # we create the sql script for the drive_system table

    script = ""
    for driveSystem in driveSystemTypes :
        script += "INSERT INTO drive_system (id, code, label) VALUES "
        script += "(" + str(driveSystem['id']) + ", '" + driveSystem['code'] + "', '" + driveSystem['label'] + "');\n"

    # We create the file

    now = datetime.now()
    fileName = "driveSystems-" + now.strftime("%d%m%Y%H%M%S") + ".sql"
    file = open('exports/' + fileName, 'w')
    file.write(script)
    file.close()

    # we create the sql script for the brand table

    script = ""
    for brand in brands :
        script += "INSERT INTO brand (id, label) VALUES "
        script += "(" + str(brand['id']) + ", '" + brand['label'] + "');\n"
    
    # We create the file

    # now = datetime.now()
    fileName = "brands-" + now.strftime("%d%m%Y%H%M%S") + ".sql"
    file = open('exports/' + fileName, 'w')
    file.write(script)
    file.close()
    