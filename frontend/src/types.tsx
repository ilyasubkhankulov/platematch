// Translating Python Enums to TypeScript Enums
export enum MatchResult {
    MATCH = 1,
    MISMATCH = 2,
    INVALID_PLATE = 3,
    INDETERMINATE = 4,
}

export enum ComparisonValue {
    MAKE = 1,
    MODEL = 2,
    YEAR = 3,
    COLOUR = 4,
}

// Translating Pydantic Models to TypeScript Interfaces
export interface ComparisonResult {
    match_result: MatchResult;
    field_name: ComparisonValue;
    plate_value: string;
    car_value: string;
}

export interface CarMatch {
    overall_result: MatchResult;
    make_result: ComparisonResult;
    model_result: ComparisonResult;
    year_result: ComparisonResult;
    color_result: ComparisonResult;
}