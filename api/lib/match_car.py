from enum import Enum

from lib.lookup_plate import VinInfo, VinResponse

# from lib.lookup_plate import Color as PLColor
from lib.recognize_car import Angle, Bbox, Car, CarRecognition
from pydantic import BaseModel


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


class ComparisonResult(BaseModel):
    match_result: MatchResult
    field_name: ComparisonValue
    plate_value: str
    car_value: str


class CarMatch(BaseModel):
    overall_result: MatchResult
    make_result: ComparisonResult
    model_result: ComparisonResult
    year_result: ComparisonResult
    # color_result: ComparisonResult

    class Config:
        schema_extra = {
            "example": {
                "overall_result": "MATCH",
                "make_result": {
                    "match_result": "MATCH",
                    "field_name": "MAKE",
                    "plate_value": "Toyota",
                    "car_value": "Toyota",
                },
                "model_result": {
                    "match_result": "MATCH",
                    "field_name": "MODEL",
                    "plate_value": "Corolla",
                    "car_value": "Corolla",
                },
                "year_result": {
                    "match_result": "MATCH",
                    "field_name": "YEAR",
                    "plate_value": "2015",
                    "car_value": "2015",
                },
                # "color_result": {
                #     "match_result": "MATCH",
                #     "field_name": "COLOUR",
                #     "plate_value": "Blue",
                #     "car_value": "Blue",
                # },
            }
        }


# based on the plate lookup response and the car lookup response, 
# determine if the car matches the plate
def match_car(plate: VinResponse, car: CarRecognition) -> CarMatch:
    make_result = ComparisonResult(
        match_result=compare_field(
            ComparisonValue.MAKE,
            plate.specifications.make,
            car.car.make
            ),
        field_name=ComparisonValue.MAKE,
        plate_value=plate.specifications.make,
        car_value=car.car.make,
    )
    model_result = ComparisonResult(
        match_result=compare_field(
            ComparisonValue.MODEL, plate.specifications.model, car.car.model
        ),
        field_name=ComparisonValue.MODEL,
        plate_value=plate.specifications.model,
        car_value=car.car.model,
    )
    year_result = ComparisonResult(
        match_result=compare_field(
            ComparisonValue.YEAR,
            plate.specifications.year,
            car.car.years),
        field_name=ComparisonValue.YEAR,
        plate_value=plate.specifications.year,
        car_value=car.car.years,
    )
    # # If the car color probability is low,
    # # we can't be sure so return indeterminate
    # if car.color.probability < 0.5 or plate.specifications.color.abbreviation == "UNK":
    #     color_result = ComparisonResult(
    #         match_result=MatchResult.INDETERMINATE,
    #         field_name=ComparisonValue.COLOUR,
    #         plate_value=plate.specifications.color.name,
    #         car_value=car.color.name,
    #     )
    # else:
    #     color_result = ComparisonResult(
    #         match_result=compare_field(
    #             ComparisonValue.COLOUR,
    #             plate.specifications.color.name,
    #             car.color.name,
    #         ),
    #         field_name=ComparisonValue.COLOUR,
    #         plate_value=plate.specifications.color.name,
    #         car_value=car.color.name,
    #     )

    results = [make_result, model_result, year_result]
    # If any value is a mismatch, the overall result is a mismatch
    if any(result.match_result == MatchResult.MISMATCH for result in results):
        overall_result = MatchResult.MISMATCH
    # If any value is indeterminate, the overall result is indeterminate
    elif any(
            result.match_result == MatchResult.INDETERMINATE
            for result in results
            ):
        overall_result = MatchResult.INDETERMINATE
    else:
        overall_result = MatchResult.MATCH

    return CarMatch(
        overall_result=overall_result,
        make_result=make_result,
        model_result=model_result,
        year_result=year_result,
        # color_result=color_result,
    )


def compare_field(
    field: ComparisonValue, plate_field: str, car_field: str
) -> MatchResult:
    if field == ComparisonValue.YEAR:
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
    elif field == ComparisonValue.COLOUR:
        return MatchResult.INDETERMINATE
    elif field == ComparisonValue.MAKE or field == ComparisonValue.MODEL:
        if plate_field is None or car_field is None:
            return MatchResult.INDETERMINATE
        elif plate_field != car_field:
            return MatchResult.MISMATCH
        else:
            return MatchResult.MATCH


def split_years(years_range):
    start_year_str, end_year_str = years_range.split("-")
    start_year = int(start_year_str)
    end_year = int(end_year_str)
    return start_year, end_year


# Example Responses
# plate lookup response
example_plate = VinResponse(
    vin="3TMMU4FN7FM086431",
    specifications=VinInfo(
        vin="3TMMU4FN7FM086431",
        year="2015",
        make="Toyota",
        model="Tacoma",
        trim="Delux Grade",
        name="2015 Toyota Tacoma",
        engine="4.0L V6 DOHC",
        style="PICKUP",
        transmission="",
        drive_type="4WD/4-Wheel Drive/4x4",
        fuel_type="Gasoline",
        made_in="",
        anti_brake_system="",
        city_mileage="",
        highway_mileage="",
        overall_height="",
        overall_length="",
        overall_width="",
        standard_seating="",
        steering_type="",
        type="Pickup"
        # color=PLColor(name="Unknown", abbreviation="UNK"),
    ),
)

# car recognition response
example_car_recognition = CarRecognition(
    car=Car(
        make="Lexus",
        model="IS",
        generation="III facelift (2016-2020)",
        years="2016-2020",
        prob="100.00",
    ),
    # color=RCColor(name="Gray", probability=0.6417),
    angle=Angle(name="Back Left", probability=1.0),
    bbox=Bbox(br_x=0.9915, br_y=0.848, tl_x=0.0, tl_y=0.1845),
)

if __name__ == "__main__":
    print(match_car(example_plate, example_car_recognition))
