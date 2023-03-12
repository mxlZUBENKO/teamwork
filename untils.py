def calorie_сalculation(gender, age, height, weight, level_of_physical_activity):
    if gender == "Женский":
        calorie_count = 655.1 + (9.563*weight) + (1.85*height) - (4.676*age)
        return calorie_count
    calorie_count = 66.5 + (13.75*weight) + (5.003*height) - (6.775*age)
    return calorie_count
