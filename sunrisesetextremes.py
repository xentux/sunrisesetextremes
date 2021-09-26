from skyfield import api, almanac

from pytz import timezone
from math import modf

DATA_PATH = "./data"
YEAR = 2021
TIMEZONE = "Europe/Berlin"  # MEZ
LATITUDE = "51.43"  # Duisburg, North rhine-Westphalia, Germany
LONGITUDE = "6.76"  # 51.43° N, 6.76° E

ts = api.load.timescale()
load = api.Loader(DATA_PATH)  # shared BSP file directory
planets = load(
    "de421.bsp"
)  # load JPL Ephemeris, DE421 is most accurate for AD 1900 to 2050
earth = planets["earth"]
sun = planets["sun"]


def risesetextremes(lat, lon, tzstr, startYear=YEAR, years=1, verbose=False):
    lat2 = round(float(lat), 2)  # rouding to 2 decimal places
    lon2 = round(float(lon), 2)
    lon3 = round(float(lon), 2)
    if lat2 < 0:
        lat3 = str(abs(lat2)) + " S"  # Skyfield expects strings with cardinal directions
    else:
        lat3 = str(abs(lat2)) + " N"
    if lon2 < 0:
        lon3 = str(abs(lon2)) + " W"
    else:
        lon3 = str(abs(lon3)) + " E"
    if verbose:
        print("calculating sunrise, sunset")
    data = _risesetextremes(lat3, lon3, tzstr, startYear, years, verbose)
    if verbose:
        print("done")

    result = dict()
    for y in range(startYear, startYear + years):
        result[str(y)] = dict()
        for x in ["rise", "set"]:
            result[str(y)][f"{x}_earliest"] = data[str(y)][f"{x}s"][
                data[str(y)][f"{x}_hr"].index(min(data[str(y)][f"{x}_hr"]))
            ]
            result[str(y)][f"{x}_latest"] = data[str(y)][f"{x}s"][
                data[str(y)][f"{x}_hr"].index(max(data[str(y)][f"{x}_hr"]))
            ]
        for x in ["short", "long"]:
            if x == "short":
                f = min
            else:
                f = max
            idx = data[str(y)]["sunlight"].index(f(data[str(y)]["sunlight"]))
            hrs_fract, hrs = modf(data[str(y)]["sunlight"][idx])
            mins_fract, mins = modf(hrs_fract * 60.0)
            result[str(y)][
                f"{x}est_hrs"
            ] = f"{int(hrs)} hours {int(mins)} minutes {round(mins_fract*60.0)} seconds"
            result[str(y)][f"{x}est_date"] = data[str(y)]["rises"][idx]
    return result, data


def _risesetextremes(lat, lon, tzstr, startYear, years, verbose=False):
    ts = api.load.timescale()
    load = api.Loader(DATA_PATH)
    e = load("de430t.bsp")
    # earth = planets['earth']

    tz = timezone(tzstr)

    bluffton = api.Topos(lat, lon)
    t0 = ts.utc(startYear, 1, 1)
    t1 = ts.utc(startYear + years, 1, 1)
    t, y = almanac.find_discrete(t0, t1, almanac.sunrise_sunset(e, bluffton))

    if verbose:
        print("done")

    result = dict()

    prevrise = None
    for ti, yi in zip(t, y):
        dt, _ = ti.astimezone_and_leap_second(tz)
        if yi:
            x = "rise"
        else:
            x = "set"

        year = str(dt.year)

        if year not in result.keys():
            result[year] = {
                "rises": [],
                "rise_hr": [],
                "sets": [],
                "set_hr": [],
                "sunlight": [],
            }
        hrs = dt.hour + dt.minute / 60.0 + dt.second / 3600.0
        result[year][f"{x}s"].append(dt)
        result[year][f"{x}_hr"].append(hrs)
        if yi:
            prevrise = ti
        else:
            if prevrise is not None:
                result[year]["sunlight"].append((ti - prevrise) * 24.0)

    return result


def sun_alt(t):
    observer = api.Topos("35.78 N", "78.64 E")
    place = observer + earth
    astrometric = place.at(t).observe(sun)
    alt, az, distance = astrometric.apparent().altaz()
    return alt.degrees


if __name__ == "__main__":

    jkl, data = risesetextremes(LATITUDE, LONGITUDE, TIMEZONE)

    for x in ["rise", "set"]:
        print(x)
        for y in ["earliest", "latest"]:
            print("%20s: %s" % (y, jkl[str(YEAR)][f"{x}_{y}"]))

    for x in ["shortest", "longest"]:
        print(x)
        for y in ["date", "hrs"]:
            print("%20s: %s" % (y, jkl[str(YEAR)][f"{x}_{y}"]))
