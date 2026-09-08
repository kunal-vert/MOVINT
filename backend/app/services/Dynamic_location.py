

def Location_dynamic(location :dict):
    CurrentLocation = "International airport Kolkata"
    for realLocation in location:
        CurrentLocation = realLocation[len(location - 1)]

    return CurrentLocation    
