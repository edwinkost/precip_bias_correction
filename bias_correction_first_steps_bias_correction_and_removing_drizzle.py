
import os

# output directory (create it and go to it)
output_dir = "/scratch/sutan101/forcing_for_beda_output_v2024-05-26_correct/first_step/"
if os.path.exists(output_dir):
	cmd = "rm -r " + output_dir
	print(cmd); os.system(cmd)
os.makedirs(output_dir)
os.chdir(output_dir)

# input files

# daily era5land in half degree resolution with the unit: m/day
daily_era5land = "/scratch/sutan101/forcing_for_beda/era5land/precipitation_daily_1981-2022_halfdeg_mperday.nc"
# ~ daily_era5land = "/scratch/sutan101/forcing_for_beda/era5land/precipitation_daily_1981-1984_halfdeg_mperday.nc"

# daily w5e5 in half degree resolution with the unit: m/day
daily_w5e5     = "/scratch/sutan101/forcing_for_beda/w5e5/precipitation_daily_w5e5_1979-2019_mperday.nc"
# ~ daily_w5e5     = "/scratch/sutan101/forcing_for_beda/w5e5/precipitation_daily_w5e5_1979-1983_mperday.nc"


# calculate the climatology of daily_era5land and daily_w5e5 - based on the years 1981-2019 only 
monthly_climatology_era5land = "monthly_climatology_1981-2019_" + os.path.basename(daily_era5land)
cmd = "cdo -L -f nc4 -setday,1 -setyear,2000 -ymonavg -selyear,1981/2019 " + daily_era5land + " " + monthly_climatology_era5land
print(cmd); os.system(cmd)
monthly_climatology_w5e5 = "monthly_climatology_1981-2019_" + os.path.basename(daily_w5e5)
cmd = "cdo -L -f nc4 -setday,1 -setyear,2000 -ymonavg -selyear,1981/2019 " + daily_w5e5 + " " + monthly_climatology_w5e5 
print(cmd); os.system(cmd)

# identify the minimum precip above zero from W5E5, set the minimum to 0.1 mm/day
minimum_precip_above_drizzle = "minimum_precip_above_drizzle.nc"
cmd = "cdo -L -f nc4 -setday,1 -setmon,1 -setyear,1800 -maxc,0.0001 -timmin -setctomiss,0 " + str(daily_w5e5) + " " + minimum_precip_above_drizzle
print(cmd); os.system(cmd)

# defining the monthly_correction_factor: Pclim_W5E5 / Pclim_era5land
# ~ cmd = "cdo -L -f nc4 -setrtoc,10,inf,10 -setmisstoc,1.0 -div " + monthly_climatology_w5e5 + " " + monthly_climatology_era5land + " first_step_monthly_correction_factor.nc"
cmd = "cdo -L -f nc4 -setrtoc,100,inf,100 -setmisstoc,1.0 -div " + monthly_climatology_w5e5 + " " + monthly_climatology_era5land + " first_step_monthly_correction_factor.nc"
print(cmd); os.system(cmd)


# ~ for year in range(1981,1985):

for year in range(1981,2023):
    
    # first step: # removing the bias, implementing the monthly_correction_factor

    # convert the monthly correction file to a temporary file for this year
    tmp_first_step_monthly_correction_factor = "tmp_first_step_monthly_correction_factor_" + str(year) + ".nc"
    cmd = "cdo -setyear," + str(year) + " first_step_monthly_correction_factor.nc " + tmp_first_step_monthly_correction_factor 
    print(cmd); os.system(cmd)
    
    era5land_daily_yearly_file = "tmp_era5land_daily_original_" + str(year) + ".nc"
    cmd = "cdo -L -f nc4 -selyear," + str(year) + " " + daily_era5land + " " + era5land_daily_yearly_file
    print(cmd); os.system(cmd)
    
    # implementing the correction
    era5land_daily_yearly_1st_corrected = "tmp_era5land_daily_original_1st_corrected_" + str(year) + ".nc"
    cmd = "cdo -L -f nc4 -mul " + era5land_daily_yearly_file +  " " + tmp_first_step_monthly_correction_factor + " " + era5land_daily_yearly_1st_corrected
    print(cmd); os.system(cmd)
    
    # identify whether raindays or not
    # - raindays: if era5land_daily_yearly_1st_corrected > minimum_precip_above_drizzle
    raindays = "tmp_era5land_daily_raindays_" + str(year) + ".nc"
    cmd = "cdo -L -f nc4 -ge " + era5land_daily_yearly_1st_corrected + " " + minimum_precip_above_drizzle + " " + raindays
    print(cmd); os.system(cmd)
    
    # create a dummy zero map
    dummy_zero = "tmp_era5land_dummy_zero_" + str(year) + ".nc"
    cmd = "cdo -L -f nc4 -mulc,0.0 " + era5land_daily_yearly_1st_corrected + " " + dummy_zero
    print(cmd); os.system(cmd)
    
    # second step: removing the drizzle
    era5land_daily_yearly_1st_corrected_without_drizzle = "era5land_daily_original_1st_corrected_without_drizzle_" + str(year) + ".nc"
    cmd = "cdo -L -f nc4 -ifthenelse " + raindays + " " + era5land_daily_yearly_1st_corrected + " " + dummy_zero + " " + era5land_daily_yearly_1st_corrected_without_drizzle
    print(cmd); os.system(cmd)
    
    # remove all temporary files
    cmd = "rm tmp*"
    print(cmd); os.system(cmd)
    
