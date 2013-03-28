files = np.sort(glob.glob(loc + 'ocean_his_*.nc')) # sorted list of file names
filesfull = np.sort(glob.glob(loc + 'ocean_his_*.nc')) #full path of files
# Find the list of files that cover the desired time period
for i,name in enumerate(files): # Loop through files
	nctemp = netCDF.Dataset(name)
	ttemp = nctemp.variables['ocean_time'][:]
	nctemp.close()
	# If datenum_in is larger than the first time in the file but smaller
	# than the last time, then this is the correct file to use to start
	if date > ttemp[0] and date <= ttemp[-1]:
		ifile = i # this is the starting file identifier then
		break
# Since the number of indices per file can change, make the process
# of finding the necessary files a little more general
# Start by opening two files
i = 1
fname = [files[ifile]]


# pdb.set_trace()

# if ff: #forward - add 2nd file on end
# 	fname.append(files[ifile+i])
# else: #backward - add previous time file to beginning
# 	fname.insert(0,files[ifile-i])
nc = netCDF.MFDataset(fname) # files in fname are in chronological order
# number of indices included in opened files so far
ninds = nc.variables['ocean_time'][:].size 
# Find which output in ifile is closest to the user-input start time (choose lower index)
# Dates for drifters from this start date
dates = nc.variables['ocean_time'][:]	
ilow = date >= dates
# time index with time value just below date (relative to file ifile)
istart = dates[ilow].size - 1
nc.close()
# Select indices 
if ff:
	tinds = range(istart,istart+tout) # indices of model outputs desired
else: # backward in time
	# have to shift istart since there are now new indices behind since going backward
	tinds = range(istart,istart-tout,-1)
# If we need more indices than available in these files, add another

if ff:
	# if the final index we want is beyond the length of these files,
	# keep adding files on
	while tinds[-1] >= len(dates): 
		# if tdir: #forward - add 2nd file on end
		fname.append(files[ifile+i])
		nc = netCDF.MFDataset(fname) # files in fname are in chronological order
		dates = nc.variables['ocean_time'][:]	
		ilow = date >= dates
		# time index with time value just below datenum_in (relative to file ifile)
		istart = dates[ilow].size - 1
		tinds = range(istart,istart+tout)
		nc.close()
		i = i + 1
else: #backwards in time
	while tinds[-1] < 0:
		fname.insert(0,files[ifile-i])
		nc = netCDF.MFDataset(fname)
		dates = nc.variables['ocean_time'][:]	
		ilow = date >= dates
		# time index with time value just below datenum_in (relative to file ifile)
		istart = dates[ilow].size - 1
		tinds = range(istart,istart-tout,-1)
		nc.close()
		i = i + 1
