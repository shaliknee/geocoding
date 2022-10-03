# geocoding
Allows a user to determine a list of unhealthy air quality targets given a specified range, location, max, and AQI threshold of what qualifies as unhealthy air quality.  Can perform forward geocoding and reverse geocoding using APIs or predetermined files. Utilizes Python 3.10 and web APIs Nominatim and PurpleAir.

[[ICS 32, Project 3 Guide]](https://www.ics.uci.edu/~thornton/ics32/ProjectGuide/Project3/)

DO NOT COPY OR USE




INPUT:
The first line of input will be in one of two formats:
  CENTER NOMINATIM location, where location is any arbitrary, non-empty string describing the "center" point of our analysis. For example, if this line of input said CENTER NOMINATIM Bren Hall, Irvine, CA, the center of our analysis is Bren Hall on the campus of UC Irvine. The word NOMINATIM indicates that we'll use Nominatim's API to determine the precise location (i.e., the latitude and longitude) of our center point.
  CENTER FILE path, where path is the path to a file on your hard drive containing the result of a previous call to Nominatim. The file needs to exist. The expectation is the file will contain data in the same format that Nominatim would have given you, but will allow you to test your work without having to call the API every time — important, because Nominatim imposes limitations on how often you can call into it, and because this could allow you to make large parts of the program work without having hooked up the APIs at all.

The second line of input will be in the following format:
  RANGE miles, where miles is a positive integer number of miles. For example, if this line of input said RANGE 30, then the range of our analysis is 30 miles from the center location.

The third line of input will be in the following format:
  THRESHOLD AQI, where AQI is a positive integer specifying the AQI threshold, which means we're interested in finding places that have AQI values at least as high as that threshold. It is safe to assume that the AQI threshold is non-negative, though it could be zero.
  
The fourth line of input will be in the following format:
  MAX number, where number is the maximum number of locations we want to find in our search, which you can assume would be a positive integer. For example, if this line of input said MAX 5, then we're looking for up to five locations where the AQI value is at or above the AQI threshold.
  
The fifth line of input will be in one of two formats:
  AQI PURPLEAIR, which means that we want to obtain our air quality information from PurpleAir's API.
  AQI FILE path, where path is the path to a file on your hard drive containing the result of a previous call to PurpleAir's API with all of the sensor data in it.
The sixth line of input will be in one of two formats:
  REVERSE NOMINATIM, which means that we want to use the Nominatim API to do reverse geocoding, i.e., to determine a description of where problematic air quality sensors are located.
  REVERSE FILES path1 path2 ..., which means that we want to use files stored on our hard drive containing the results of previous calls to Nominatim's reverse geocoding API instead. Paths are separated by spaces — which means they can't contain spaces — and we expect there to be at least as many paths listed as the number we passed to MAX (e.g., if we said MAX 5 previously, then we'd specify at least five files containing reverse geocoding data).
  
OUTPUT: 
For each location, print three lines of output:
-AQI AQI_value, where AQI_value is the AQI value you calculated for this location.
-latitude longitude, which is the latitude and longitude for this location, in the same format as you printed the center location's latitude and longitude.
-description, which is the full description of the location.

EXAMPLE:
A complete example using locally-stored data:
Input:

CENTER NOMINATIM Bren Hall, Irvine, CA
RANGE 30
THRESHOLD 100
MAX 5
AQI PURPLEAIR
REVERSE NOMINATIM
CENTER 33.64324045/N 117.84185686276017/W

Output:

AQI 180
33.53814/N 117.5998/W
Garcilla Drive, Orange County, California, 92690, United States of America
AQI 157
33.690376/N 118.03055/W
Orange County, California, United States of America
AQI 154
33.68315/N 117.66642/W
Alton Parkway, Foothill Ranch, Lake Forest, Orange County, California, 92610, United States of America
AQI 152
33.816/N 118.23275/W
Arco, Tesoro Carson Refinery, Bangle, Carson, Los Angeles County, California, 90810, United States of America
AQI 151
33.86117/N 117.96228/W
1880, West Southgate Avenue, Fullerton, Orange County, California, 92833, United States of America
