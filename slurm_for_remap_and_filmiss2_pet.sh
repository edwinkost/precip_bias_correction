#!/bin/bash

# we reserve one node of eejit, one contains 96 cores
#SBATCH -N 1

# we use all cores
#SBATCH -n 192

# wall clock time (maximum 120 hours)
#SBATCH -t 119:59:00

# the partition name 
#SBATCH -p genoa

# job name
#SBATCH -J pet_remapcon_and_fillmiss2

#~ (pcrglobwb_python3) edwin@tcn543.local.snellius.surf.nl:/scratch-shared/edwinaha/forcing_for_beda_v2024-24-05$ ls -lah /scratch-shared/edwinhs/uly_forcing_files_v2024-02-XX_em-earth_era5land
#~ total 1.2T
#~ drwxr-xr-x. 2 edwinhs edwinhs 4.0K May 22 16:19 .
#~ drwxr-xr-x. 6 edwinhs edwinhs 4.0K May 24 13:44 ..
#~ -rw-r--r--. 1 edwinhs edwinhs  724 May 22 16:19 cdo_merge.sh
#~ -rw-r--r--. 1 edwinhs edwinhs 297G May 22 16:19 pet_daily_era5land_1981-2022.nc
#~ -rw-r--r--. 1 edwinhs edwinhs 269G May 22 16:19 precipitation_daily_em-earth_1981-2019.nc
#~ -rw-r--r--. 1 edwinhs edwinhs 297G May 22 16:19 precipitation_daily_era5land_1981-2022.nc
#~ -rw-r--r--. 1 edwinhs edwinhs   85 May 22 16:19 source.txt
#~ -rw-r--r--. 1 edwinhs edwinhs 297G May 22 16:19 tavg_daily_era5land_1981-2022.nc

NC_INPUT_FILE="/scratch-shared/edwinhs/uly_forcing_files_v2024-02-XX_em-earth_era5land/pet_daily_era5land_1981-2022.nc"
GRID_DES_FILE="/projects/0/dfguu/users/edwin/data/cdo_grid_description_files/global_grid_des_05min.txt"

NC_OUTPUT_FOLDER="/scratch-shared/edwin/era5land_uly_forcing_files_for_beda/pet/"
mkdir -p ${NC_OUTPUT_FOLDER}
cd ${NC_OUTPUT_FOLDER}

NC_OUTPUT_PATTERN="pet_daily_era5land-ulysses_05min"

. /home/edwin/load_all_default.sh

# - loop through all years
for i in {1981..2022}

do
 
 YEAR=$i
 
 cdo -L -f nc4 -settime,00:00:00 -fillmiss2 -remapcon,${GRID_DES_FILE} -selyear,${YEAR} ${NC_INPUT_FILE} ${NC_OUTPUT_PATTERN}_${YEAR}.nc &
 
done

wait

