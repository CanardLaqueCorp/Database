import csv
from datetime import datetime

# We read the csv file and we create a list of cars

with open('data/data2023.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    cars = []

    for line in csv_reader:
        line = line[0].split(';')

        maxBioEthanol = line[29]
        if (maxBioEthanol == ''):
            maxBioEthanol = 0
        
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

        # We create a car object using the right data

        car = {
            'brand': line[2],
            'model': line[3],
            'cylinder': line[7],
            'transmission': line[8],
            'transmissionTypeCode': line[21],
            'transmissionTypeLabel': line[22],
            'driveSystemCode': line[27],
            'driveSystemLabel': line[28],
            'gears': line[24],
            'cityFuel': line[15],
            'highwayFuel': line[16],
            'combinedFuel': line[17],
            'guzzler': guzzler,
            'startAndStop': startAndStop,
            'maxBioEthanol': maxBioEthanol,
            'fuelTypeCode': line[32],
            'fuelTypeLabel': line[33],
            'annualFuelCost': line[44],
            'carLineCode': line[68],
            'carLineLabel': line[69],
            'fuelRate' : line[131],
            'ghgRate' : line[132],
            'smogRate' : line[135],
            'spendOnFiveYears' : line[151],
            'cityCarbon' : line[152],
            'highwayCarbon' : line[153],
            'combinedCarbon' : line[154],
        }
        cars.append(car)

    # We create the sql script

    script = ""
    for car in cars :
        script += "INSERT INTO car_th (brand, model, cylinder, car_transmission, city_fuel, highway_fuel, combined_fuel, has_guzzler, gears, max_bio_fuel, annual_fuel_cost, spend_on_five_years, has_start_and_stop, fe_rating, ghg_rating, smog_rating, city_carbon, highway_carbon, combined_carbon) VALUES "
        script += "(" + "'" + car['brand'] + "', '" + car['model'] + "', '" + car['cylinder'] + "', '" + car['transmissionTypeLabel'] + "', '" + car['cityFuel'] + "', '" + car['highwayFuel'] + "', '" + car['combinedFuel'] + "', '" + str(car['guzzler']) + "', '" + car['gears'] + "', '" + str(car['maxBioEthanol']) + "', '" + car['annualFuelCost'] + "', '" + car['spendOnFiveYears'] + "', '" + str(car['startAndStop']) + "', '" + car['fuelRate'] + "', '" + car['ghgRate'] + "', '" + car['smogRate'] + "', '" + car['cityCarbon'] + "', '" + car['highwayCarbon'] + "', '" + car['combinedCarbon'] + "');\n"
    
    # We create the file
    
    now = datetime.now()
    fileName = "carsTH-" + now.strftime("%d%m%Y%H%M%S") + ".sql"
    file = open('exports/' + fileName, 'w')
    file.write(script)
    file.close()





    