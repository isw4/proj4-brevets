# Project 4:  Brevet time calculator with Ajax
### Author: Isaac Hong Wong (iwong@uoregon.edu)

Reimplementing the RUSA ACP controle time calculator found at:
https://rusa.org/octime_acp.html with one that works with AJAX and Flask.

## Brevets

Randonneuring (also known as Audax in the UK, Australia and Brazil) is a 
long-distance cycling sport with its origins in audax cycling. In 
randonneuring, riders attempt courses of 200 km or more, passing through 
predetermined "controls" (checkpoints) every few tens of kilometres. 
Riders aim to complete the course within specified time limits, and 
receive equal recognition regardless of their finishing order. A 
randonneuring event is called a randonnée or brevet.

In such events, riders follow a course through a series of predetermined 
checkpoints called "controls"; these are typically a few tens of kilometres 
apart. Riders are expected to keep within minimum and maximum average speed 
limits. Riders who arrive early at controls will be made to wait before they
can carry on.
(src: https://en.wikipedia.org/wiki/Randonneuring)


## ACP controle times
Controls are points where a rider must obtain proof of passage, and 
control[e] times are the minimum and maximum times by which the rider must  
arrive at the location.   

The algorithm for calculating controle times is described at
https://rusa.org/octime_alg.html. Additional background information
is in https://rusa.org/pages/rulesForRiders.  

The rules to determine the controle times are:
1)  The closing time at the starting point(first controle) is always 1h after 
    the race begins

2)  The opening and closing time for subsequent controles depends on the
    distance, the maximum speed, and minimum speed specified for that distance.
    Riders must keep within a minimum and maximum speed for a specified distance.

    | Distances(km) | Minimum(km/h) | Maximum(km/h)
    | ------------- | ------------- | --------
    | First 200     | 15            | 34
    | Next  200     | 15            | 32
    | Next  200     | 15            | 30
    | Next  600     | 11.428        | 28

    ```
    For example, a controle at 700km has an opening time of:
    200/34 + 200/32 + 200/30 + 100/28 = 22.37h (22h 22m) after the starting time
    
    And a closing time of:
    200/15 + 200/15 + 200/15 + 100/11.428 = 48.75h (48h 45m) after the starting time
    ```

3a) Brevets are organized only for 200, 300, 400, 600, and 1000km. However, the 
    last controle may not be at exactly those distances. The opening and closing
    time for the last controle is calculated using the brevet distance, not the
    actual distance.

    ```
    For example, a brevet of 1000km may have a controle at 1050km, but the opening
    and closing times for this controle is as if it were at 1000km. No extra time 
    is given to cover the extra 50km.
    ```

3b) The final controle's distance must not be more than 110% of the brevet distance. 

## ACP controle times calculator (for users)

1) Enter the starting date and time, and the brevet distance
2) Enter the controle distances in either miles or km
	- The first controle must always be 0
	- No controle can be greater than 1.1 times the brevet distance