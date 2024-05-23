
import os

# output directory (create it and go to it)
output_dir = "/scratch/sutan101/forcing_for_beda_output/"
os.makedirs(output_dir)
os.chdir(output_dir)

# input files

# daily era5land in half degree resolution with the unit: m/day
daily_era5land = "/scratch/sutan101/forcing_for_beda/era5land/precipitation_daily_1981-2022_halfdeg.nc"

# daily w5e5 in half degree resolution with the unit: m/day
daily_w5e5     = "/scratch/sutan101/forcing_for_beda/w5e5/precipitation_daily_w5e5_1979-2019_mperday.nc"


# calculate the climatology of daily_era5land and daily_w5e5
monthly_climatology_era5land = "monthly_climatology_" + os.path.basename(daily_era5land)
cmd = "cdo -L -f nc4 -setday,1 -setyear,2000 -ymonavg " + daily_era5land + " " + monthly_climatology_era5land
os.system(cmd)
monthly_climatology_w5e5 = "monthly_climatology_" + os.path.basename(daily_w5e5)
cmd = "cdo -L -f nc4 -setday,1 -setyear,2000 -ymonavg " + daily_w5e5 + " " + monthly_climatology_w5e5 
os.system(cmd)

# identify the minimum precip above zero from W5E5
minimum_precip_above_drizzle = "minimum_precip_above_drizzle.nc"
cmd = "cdo -L -f nc4 -setday,1 -setmon,1 -setyear,1800 -timmin -setctomiss,0 " + str(daily_w5e5) + " " + minimum_precip_above_drizzle
os.system(cmd)

# defining the monthly_correction_factor: Pclim_W5E5 / Pclim_era5land
cmd = "cdo -L -f nc4 -div " + monthly_climatology_era5land + " " + monthly_climatology_w5e5 + " first_step_monthly_correction_factor.nc"
os.system(cmd)


for year in range(1981,2022):
    
    # first step: # removing the bias, implementing the monthly_correction_factor

    # convert the monthly correction file to a temporary file for this year
    tmp_first_step_monthly_correction_factor = "tmp_first_step_monthly_correction_factor_" + str(year) + ".nc"
    cmd = "cdo -setyear," + str(year) + " first_step_monthly_correction_factor.nc " + tmp_first_step_monthly_correction_factor 
    os.system(cmd)
    
    era5land_daily_yearly_file = "tmp_era5land_daily_original_" + str(year) + ".nc"
    cmd = "cdo -L -f nc4 -selyear," + str(year) + " " daily_era5land + " " era5land_daily_yearly_file
    os.system(cmd)
    
    # implementing the correction
    era5land_daily_yearly_1st_corrected = 
    cmd = "cdo -L -f nc4 -mul " + era5land_daily_yearly_file +  " " + tmp_first_step_monthly_correction_factor + era5land_daily_yearly_1st_corrected
    os.system(cmd)
    
    # second step: removing the drizzle
    era5land_daily_yearly_1st_corrected_without_drizzle = " "
    cmd = "cdo -L -f nc4 -min " + minimum_precip_above_drizzle + " " era5land_daily_yearly_1st_corrected + " " + era5land_daily_yearly_1st_corrected_without_drizzle
    os.system(cmd)


# final step: 
    
    
    
    


 


1. To remove the bias:
We use W5E5, but this covers 1979-2019 only. 
For every month, we will calculate the monthly climatology of precipitation: Pclim_W5E5 and Pclim_era5land 
Then the corrected era5land: P_corrected_era5land = (Pclim_W5E5 / Pclim_era5land) x P_era5land

2. For the drizzle correction:
We use W5E5, but this covers 1979-2019 only. 
For every pixel, we will identify the minimum precip above zero. Let’s assume this as Pmin_W5E5

Pmin_W5E5 on velocity: /scratch/sutan101/forcing_for_beda/w5e5/timmin_precipitation_without_zero_w5e5_1979-2019.nc

Then, to remove the drizzle we will assume if P_corrected_era5land <  Pmin_W5E5, P_corrected_era5land = 0.0

4. Remove the bias again. 
The above step will introduce ‘bias‘. Therefore we have to do additional bias correction. 
Then, we implement the extra bias correction.
extra_corrected era5land = (Pclim_W5E5 / Pclim_corrected_era5land) x P_corrected_era5land

5. As era5land covers only LAND, we will cover all missing values (e.g. at coastal regions) with the nearest values.  
