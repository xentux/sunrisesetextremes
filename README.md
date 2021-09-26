# Sun rise and set extremes

Uses [skyfield python module](https://pypi.org/project/skyfield/) to calculate sun rise and set extrema at a given observation point for a given year.  

**Note:** These results are overly precise and the actual time the Sun may be first or last seen depends heavily on atmospheric conditions and may vary by a minute or more.

Forked from [rtphokie/sunrisesetextremes](https://github.com/rtphokie/sunrisesetextremes).

## Improvements
- *Fixed*: Bug in *risesetextremes* occuring with eastern (positive) longitudes.
- *Fixed*: Removed a few dots (".") at the end of a code line.
- *Improved*: Removed unnecessary libraries
- *Improved*: Moved a few configurations to 'static' variables at the beginning of the code.
- Moved requirement and environment management to poetry.

## Examples
**For Raleigh, NC (35.78° N, 78.64° W) in 2020**

```
rise
            earliest: 2020-06-12 05:57:53.541141-04:00
              latest: 2020-10-31 07:36:19.900938-04:00
set
            earliest: 2020-12-04 17:00:40.772783-05:00
              latest: 2020-06-28 20:34:47.071092-04:00
shortest
                date: 2020-12-21 
                 hrs: 9 hours 43 minutes 56 seconds
longest
                date: 2020-06-20 
                 hrs: 14 hours 35 minutes 12 seconds
```


**Duisburg, North rhine-Westphalia, Germany (51.43° N, 6.76° E) in 2021**
```
rise
            earliest: 2021-12-13 04:10:23.572331+01:00
              latest: 2021-06-25 09:40:05.241672+02:00
set
            earliest: 2021-06-16 17:29:22.529098+02:00
              latest: 2021-12-29 20:52:02.830779+01:00
shortest
                date: 2021-06-21 09:39:38.803151+02:00
                 hrs: 7 hours 50 minutes 20 seconds
longest
                date: 2021-12-21 04:12:13.506637+01:00
                 hrs: 16 hours 37 minutes 46 seconds
```
