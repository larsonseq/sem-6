def joint_probability(burglary, earthquake, alarm, john_calls, mary_calls):
    burglary_p = 0.001 
    earthquake_p = 0.002
    # Conditional Probability Tables (CPTs)
    p_alarm_given_BE = {
        (True, True): 0.95, (True, False): 0.94, (False, True): 0.29, (False, False): 0.001
    }
    p_john_calls_given_alarm = {
        True: 0.9, False: 0.05    
    }
    p_mary_calls_given_alarm = {
        True: 0.7, False: 0.01  
    }
    # Compute probabilities correctly
    p_burglary = burglary_p if burglary else (1 - burglary_p)
    p_earthquake = earthquake_p if earthquake else (1 - earthquake_p)
    p_alarm = p_alarm_given_BE[(burglary, earthquake)] if alarm else (1 - p_alarm_given_BE[(burglary, earthquake)])
    # FIX: Correctly condition John's and Mary's calls on the alarm state
    p_john_calls = p_john_calls_given_alarm[alarm] if john_calls else (1 - p_john_calls_given_alarm[alarm])
    p_mary_calls = p_mary_calls_given_alarm[alarm] if mary_calls else (1 - p_mary_calls_given_alarm[alarm])
    # Joint probability calculation
    return p_burglary * p_earthquake * p_alarm * p_john_calls * p_mary_calls
# Taking input from the user
b = input("Enter if Burglary happened: ") == "T"
e = input("Enter if Earthquake happened: ") == "T"
a = input("Enter if Alarm rang: ") == "T"
j = input("Enter if John calls: ") == "T"
m = input("Enter if Mary calls: ") == "T"
# Compute joint probability
p_query = joint_probability(b, e, a, j, m)
print(f"Probability of Burglary={b}, Earthquake={e}, Alarm={a}, John Calls={j}, Mary Calls={m}: {p_query}")


