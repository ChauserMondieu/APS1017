import time

# original time format
t = "2020/2/12"
print("time with original format:" + t)

# transfer into timestamps with unit second
secs = time.mktime(time.strptime(t, "%Y/%m/%d"))
print("timestamp: " + str(secs))

# output time with local time format
time_secs = time.asctime(time.localtime(secs))
print("local time:" + time_secs)

# transfer into time.time_structure
time_struct = time.strptime(t, "%Y/%m/%d")
# output time with format
time_opt = time.strftime("%Y/%m/%d", time_struct)
print("time with new format: " + time_opt)