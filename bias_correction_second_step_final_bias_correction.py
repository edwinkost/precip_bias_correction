
import os

# output directory (create it and go to it)
output_dir = "/scratch/sutan101/forcing_for_beda_output_v2024-05-26_correct/second_final_step/"
if os.path.exists(output_dir):
	cmd = "rm -r " + output_dir
	print(cmd); os.system(cmd)
os.makedirs(output_dir)
os.chdir(output_dir)

# input files

# daily era5land in half degree resolution with the unit: m/day - AFTER THE FIRST STEP
daily_era5land = "/scratch/sutan101/forcing_for_beda_output_v2024-05-26_correct/first_step/merged_era5land_daily_original_1st_corrected_without_drizzle_1981-2022.nc"

# daily w5e5 in half degree resolution with the unit: m/day
daily_w5e5     = "/scratch/sutan101/forcing_for_beda/w5e5/precipitation_daily_w5e5_1979-2019_mperday.nc"

# calculate the climatology of daily_era5land and daily_w5e5
monthly_climatology_era5land = "monthly_climatology_1981-2019_" + os.path.basename(daily_era5land)
cmd = "cdo -L -f nc4 -setday,1 -setyear,2000 -ymonavg -selyear,1981/2019 " + daily_era5land + " " + monthly_climatology_era5land
print(cmd); os.system(cmd)
monthly_climatology_w5e5 = "monthly_climatology_1981-2019_" + os.path.basename(daily_w5e5)
cmd = "cdo -L -f nc4 -setday,1 -setyear,2000 -ymonavg -selyear,1981/2019 " + daily_w5e5 + " " + monthly_climatology_w5e5 
print(cmd); os.system(cmd)

# defining the monthly_correction_factor: Pclim_W5E5 / Pclim_era5land
cmd = "cdo -L -f nc4 -setrtoc,10,inf,10 -setmisstoc,1.0 -div " + monthly_climatology_w5e5 + " " + monthly_climatology_era5land + " final_step_monthly_correction_factor.nc"
print(cmd); os.system(cmd)


for year in range(1981,2023):

# ~ for year in range(1981,1985):

    
    # final step: # removing the bias, implementing the monthly_correction_factor

    # convert the monthly correction file to a temporary file for this year
    tmp_final_step_monthly_correction_factor = "tmp_final_step_monthly_correction_factor_" + str(year) + ".nc"
    cmd = "cdo -setyear," + str(year) + " final_step_monthly_correction_factor.nc " + tmp_final_step_monthly_correction_factor 
    print(cmd); os.system(cmd)
    
    era5land_daily_yearly_file = "tmp_era5land_daily_original_" + str(year) + ".nc"
    cmd = "cdo -L -f nc4 -selyear," + str(year) + " " + daily_era5land + " " + era5land_daily_yearly_file
    print(cmd); os.system(cmd)
    
    # implementing the correction
    # - set the maximum rainfall in a day to 2 meter per day
    era5land_daily_yearly_final_corrected = "era5land_daily_final_corrected_" + str(year) + ".nc"
    cmd = "cdo -L -f nc4 -setrtoc,2,inf,2 -mul " + era5land_daily_yearly_file +  " " + tmp_final_step_monthly_correction_factor + " " + era5land_daily_yearly_final_corrected
    print(cmd); os.system(cmd)
    
    # remove all temporary files
    cmd = "rm tmp*"
    print(cmd); os.system(cmd)
    
