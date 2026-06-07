import csv


myInventoryList = []
myVehicle = {
    "vin" : "<empty>",
    "make" : "<empty>" ,
    "model" : "<empty>" ,
    "year" : 0,
    "range" : 0,
    "topSpeed" : 0,
    "zeroSixty" : 0.0,
    "mileage" : 0
}

# print(myVehicle.keys())

for key123, value456 in myVehicle.items():
    print("{} : {}".format(key123,value456))