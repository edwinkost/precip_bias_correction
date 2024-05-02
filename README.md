General steps: 

0. We use ERA5Land, downloaded from the Ulysses project. The following procedure will be done at 30 min resolution 
- Containing bias, usually too wet. 
- Containing drizzle. 
- But covering until the year 2023 (until now).

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
