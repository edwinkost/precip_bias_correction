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
#SBATCH -J tavg_remap_and_fillmiss2

NC_INPUT_FILE="/scratch-shared/edwin/era5land_1981-2025_for_extending_wmo_2024_run/source_1981-2022/version_20231206_merged_1981-2022/tavg_daily_1981-2022_settime.nc"
GRID_DES_FILE="/scratch-shared/edwin/era5land_1981-2025_for_extending_wmo_2024_run/source_2023-2025/cdo_griddes_global_05min.txt"

NC_OUTPUT_FOLDER="/scratch-shared/edwin/era5land_1981-2025_for_extending_wmo_2024_run/source_1981-2022/remap_fillmiss2_05min/"
mkdir -p ${NC_OUTPUT_FOLDER}
cd ${NC_OUTPUT_FOLDER}

NC_OUTPUT_PATTERN="tavg_daily_era5land-ulysses_05min_fillmiss2"

. /home/edwin/load_all_default.sh

# - loop through all years
for i in {1981..2022}

do
 
 YEAR=$i
 
 cdo -L -f nc4 -fillmiss2 -remapbil,${GRID_DES_FILE} -selyear,${YEAR} ${NC_INPUT_FILE} ${NC_OUTPUT_PATTERN}_${YEAR}.nc &
 
done

wait

