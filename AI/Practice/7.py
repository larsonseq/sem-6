def joint_probabilty(bg, eq, al, jc, mc):
    bgp = 0.001
    eqp = 0.002
    albe = {
        (True, True): 0.95, (True, False): 0.94, (False, True): 0.29, (False, False): 0.001
    }

    jcal = {
        True: 0.9, False:0.05
    }

    mcal = {
        True: 0.7, False: 0.01
    }

    pb = bgp if bg else (1 - bgp)
    pe = eqp if eq else (1-eq)
    pal = albe[(bg, eq)] if al else (1 - albe[(bg, eq)])
    pjc = jcal[al] if jc else (1 - jcal[al])
    pmc = mcal[al] if mc else (1 - mcal[al])

    return pb * pe * pal * pjc * pmc

# Taking input from the user
b = input("Enter if Burglary happened: ") == "T"
e = input("Enter if Earthquake happened: ") == "T"
a = input("Enter if Alarm rang: ") == "T"
j = input("Enter if John calls: ") == "T"
m = input("Enter if Mary calls: ") == "T"
# Compute joint probability
p_query = joint_probabilty(b, e, a, j, m)
print(f"Probability of Burglary={b}, Earthquake={e}, Alarm={a}, John Calls={j}, Mary Calls={m}: {p_query}")


