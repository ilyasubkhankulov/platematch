from enum import Enum


class MatchResult(Enum):
    MATCH = 1
    MISMATCH = 2
    INVALID_PLATE = 3
    INDETERMINATE = 4
    
class ComparisonValue(Enum):
    MAKE = 1
    MODEL = 2
    YEAR = 3
    COLOUR = 4
    
   
class ComparisonResult:
    def __init__(self, match_result: MatchResult, field_name: ComparisonValue, plate_value: str, car_value: str):
        self.match_result = match_result
        self.field_name = field_name
        self.plate_value = plate_value
        self.car_value = car_value
        
class CarMatch:
    def __init__(self, overall_result: MatchResult, make_result: ComparisonResult, model_result: ComparisonResult, year_result: ComparisonResult, color_result: ComparisonResult):
        self.make_result = make_result
        self.model_result = model_result
        self.year_result = year_result
        self.color_result = color_result
        self.overall_result = overall_result
        
    def __str__(self):
        return (f"CarMatch - \nOverall Result: {self.overall_result}, \n"
                f"Make: {self.make_result.match_result},\n"
                f"   Plate Value: {self.make_result.plate_value},\n"
                f"   Car Value: {self.make_result.car_value},\n"
                f"Model: {self.model_result.match_result},\n"
                f"   Plate Value: {self.model_result.plate_value},\n"
                f"   Car Value: {self.model_result.car_value},\n"
                f"Year: {self.year_result.match_result},\n"
                f"   Plate Value: {self.year_result.plate_value},\n"
                f"   Car Value: {self.year_result.car_value},\n"
                f"Color: {self.color_result.match_result}\n"
                f"   Plate Value: {self.color_result.plate_value},\n"
                f"   Car Value: {self.color_result.car_value}\n")
        

# based on the plate lookup response and the car lookup response, determine if the car matches the plate
def match_car(plate, car) -> CarMatch:
    make_result = ComparisonResult(compare_field(ComparisonValue.MAKE, plate['vin']['make'], car['car']['make']), ComparisonValue.MAKE, plate['vin']['make'], car['car']['make'])
    model_result = ComparisonResult(compare_field(ComparisonValue.MODEL, plate['vin']['model'], car['car']['model']), ComparisonValue.MODEL, plate['vin']['model'], car['car']['model'])
    year_result = ComparisonResult(compare_field(ComparisonValue.YEAR, plate['vin']['year'], car['car']['years']), ComparisonValue.YEAR, plate['vin']['year'], car['car']['years'])
    # If the car color probability is low, we can't be sure so return indeterminate
    if car['color']['probability'] < 0.5 or plate['vin']['color']['abbreviation'] == 'UNK':
        color_result = ComparisonResult(MatchResult.INDETERMINATE, ComparisonValue.COLOUR, plate['vin']['color']['name'] , car['color']['name'])
    else:
        color_result = ComparisonResult(compare_field(ComparisonValue.COLOUR, plate['vin']['color']['name'], car['color']['name']), ComparisonValue.COLOUR, plate['vin']['color'].name , car['color']['name'])
        
    results = [make_result, model_result, year_result, color_result]
    # If any value is a mismatch, the overall result is a mismatch
    if any(result.match_result == MatchResult.MISMATCH for result in results):
        overall_result = MatchResult.MISMATCH
    # If any value is indeterminate, the overall result is indeterminate
    elif any(result.match_result == MatchResult.INDETERMINATE for result in results):
        overall_result = MatchResult.INDETERMINATE
    else:
        overall_result = MatchResult.MATCH
        
    return CarMatch(overall_result, make_result, model_result, year_result, color_result)



def compare_field(field: ComparisonValue, plate_field: str, car_field:str) -> MatchResult:
    match field:
        case ComparisonValue.YEAR:
            if "-" in car_field:
                carStartYear, carEndYear = split_years(car_field)
            else:
                carStartYear = int(car_field)
                carEndYear = int(car_field)
            if carStartYear is None or carEndYear is None or plate_field is None:
                return MatchResult.INDETERMINATE
            if carStartYear <= int(plate_field) <= carEndYear:
                return MatchResult.MATCH
            else:
                return MatchResult.MISMATCH
        case ComparisonValue.COLOUR:
            return MatchResult.INDETERMINATE
        case ComparisonValue.MAKE | ComparisonValue.MODEL:
            if plate_field is None or car_field is None:
                return MatchResult.INDETERMINATE
            elif plate_field != car_field:
                return MatchResult.MISMATCH
            else:
                return MatchResult.MATCH
            
            
def split_years(years_range):
    start_year_str, end_year_str = years_range.split('-')
    start_year = int(start_year_str)
    end_year = int(end_year_str)
    return start_year, end_year

# Example Responses
# plate lookup response
example_plate = { 
 'success': True, 
 'vin': {
     'vin': '3TMMU4FN7FM086431', 
     'year': '2015', 
     'make': 'Toyota', 
     'model': 'Tacoma', 
     'trim': 'Delux Grade', 
     'name': '2015 Toyota Tacoma', 
     'engine': '4.0L V6 DOHC', 
     'style': 'PICKUP', 
     'transmission': '', 
     'driveType': '4WD/4-Wheel Drive/4x4', 
     'fuel': 'Gasoline', 
     'color': {'name': 'Unknown', 'abbreviation': 'UNK'}
     }
 }

# car lookup response
example_car = {
   "car":{
      "make":"Lexus",
      "model":"IS",
      "generation":"III facelift (2016-2020)",
      "years":"2016-2020",
      "prob":"100.00"
   },
   "color":{
      "name":"Gray",
      "probability":0.6417
   },
   "angle":{
      "name":"Back Left",
      "probability":1.0
   },
   "bbox":{
      "br_x":0.9915,
      "br_y":0.848,
      "tl_x":0.0,
      "tl_y":0.1845
   }
}

if __name__ == '__main__':
    print(match_car(example_plate, example_car))