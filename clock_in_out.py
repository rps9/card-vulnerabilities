'''
In this scenario, the running example will be a workplace that uses the mifare classic and is trying to be secure. 

Steps for protection:
    - the reader only expects certain unique cards that belong to each employee
    - scanning in is equivalent to clocking in, and scanning out is equivalent to clocking out
    - if someone has scanned in, that card cannot be used to scan in again unless it has been scanned out
    - if the card is used to scan in outside of regular work hours, it will not work
    - if the employee puts in for PTO or sick time, the card will not work
    - if a hypothetical attacker gets to the workplace before the worker and scans in, the system will alert that a non-employee
        scanned in
    - if the employee forgot to scan out the previous day, and can't get back in, the system will detect that they have been clocked
        in for a while and that it must have been an error on the employees part, not an attacker 
    - finally, when the employee scans out, it writes unique data to the card that it is expecting next time
    
Vulnerabilities/issues: 
    - If the employee leaves early, and an attacker clones their card after they leave work, the attacker then has a small window
        to enter the building undetected
        - this could be mitigated if we add a system for employees to say they are leaving work early, but this could become
            cumbersome
    - adding all of this custom logic could be expensive in the real world, so at that point it might not even be worth using the
        mifare classic 
'''