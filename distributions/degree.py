"""
Copyright [2013] [James Absalon]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# Implemented based on http://tools.ietf.org/html/rfc5053#section-5.4.4.4
# Maps a range of numbers to degrees (not temperature. actually, not sure 
# what it means

V_MIN = 0
V_MAX = 1048576
F = [0, 10241, 491582, 712794, 831695, 948446, 1032189, 1048576]
D = [None, 1, 2, 3, 4, 10, 11, 40]
between_range = lambda start, end, v: start <= v < end

def R10(v):
    """
    Returns the R10 degree for v
    This distribution comes from rfc 5053
    """

    if not between_range(V_MIN, V_MAX, v):
        raise Exception("Recieved v %s.  v must be between %s and %s" % (v, V_MIN, V_MAX))

    for i in range(1, len(F)):
        if between_range(F[i-1], F[i], v):
            return D[i]

    raise Exception("Degree not found for v %s" % v)
