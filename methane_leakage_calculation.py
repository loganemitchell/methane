# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 16:07:50 2021

These are simple unit conversions to understand the scale of methane leakage
from the Uinta Basin natural gas infrastructure. The original data comes from
this research paper from John Lin et al (2021)
https://www.nature.com/articles/s41598-021-01721-5

Here is a press release about the study:
https://attheu.utah.edu/facultystaff/uinta-basin-methane/

@author: Logan Mitchell
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib qt


#%% Calculations to find methane leakage rates in Russian natural gas

# https://www.iea.org/countries/russia
tj = 25786288 # EIA ch4 production in 2013 in terrajoules
mmcf = tj*0.94781712 # terrajoules to million cubic feet of natural gas (mmcf)

# EIA uses: https://www.eia.gov/tools/faqs/faq.php?id=45&t=8
    # "EIA reports natural gas in volumes of cubic feet through 1964 at a pressure base of 14.65 psia (pounds per square inch absolute)
    # at 60° Fahrenheit. Beginning in 1965, the pressure base is 14.73 psia at 60° Fahrenheit."
    # 14.73 psia = 0.10156 MPa and 60 F = 15.5 C
# A gas density calculator: https://www.unitrove.com/engineering/tools/gas/natural-gas-density
# Mass Density (15.5C, 0.10156 MPa, 96.5% CH4 content) = 0.713 kg/m3 (specific vol=1.4025 m3/kg) ** This is what EIA uses
# Mass Density (21C, 96.5% CH4 content) = 0.698 kg/m3 (specific vol=1.433 m3/kg)
# A separate gas density from UCS: https://www.ucsusa.org/sites/default/files/attach/2015/03/climate-risks-of-natural-gas-fugitive-methane-emissions_methodology.pdf
    # Mass Density from UCS = 0.678 kg/m3 (specific vol=1.474 m3/kg)

# mmtch4 = mmcf*(meter^3/feet^3)*(mass density kg/m3)*(1metric ton/1000kg)
mmtch4 = mmcf*0.0283168*0.713*(1/1e3) # mmcf to million metric tons CH4

# https://www.washingtonpost.com/climate-environment/interactive/2021/russia-greenhouse-gas-emissions/
# Russian leakage in 2013 differed between reports. 
# 2015 report: ~33 million metric tons CH4 
# 2021 report: ~5 million metric tons CH4
pctleak_high = 100*33/mmtch4 # = 6.7% leakage
pctleak_low = 100*5/mmtch4   # = 1% leakage

# So, Russian gas leakage estimates are 1% on the low end & 6.7% on the high end.
# Uinta Basin gas leakage is as high as the highest estimates of Russian gas leakage.
 
#%% Time series of methane leakage from Lin et al 2021
# https://www.nature.com/articles/s41598-021-01721-5
#
# The emissions for the Uinta basin are calculated at ~25,000-45,000 kg/hr in the record.   
# A metric ton is 1000 kg, so that means 24-55 tons/hr.
# This time series is from the Model Mean in Lin et al 2021

ch4_leak = pd.DataFrame(data={'year':[2012,2015,2016,2017,2018,2019,2020,2023],
                              'ton_hr':[55,46.01307,35.17388,36.79047,31.0703,29.21299,23.80824,35]})
# CH4 leakage in tons/year
ch4_leak['ton_yr'] = ch4_leak['ton_hr']*24*365.25

#%% Methane fees in the Inflation Reduction Act (IRA) of 2022

# The Inflation Reduction Act has a $900/ton fee for methane leakage in 2023, $1200/ton in 2024, and $1500/ton in 2025.
# A small amount of leakage is allowed (<0.2%) and not every facility is covered, but a back of the envelope estimate 
# using 2019 CH4 leakage would be $230-384 million in leakage fees per year. 
# This is substantial compared to the total value of ~$1 Billion for natural gas produced in the Uinta Basin in 2017.

# Bill text: https://www.democrats.senate.gov/imo/media/doc/inflation_reduction_act_of_2022.pdf
# See Sec. 60113. Methane Emissions Reduction Program (pg 685)

ch4_leak['fee_900'] = ch4_leak['ton_yr']*900
ch4_leak['fee_1200'] = ch4_leak['ton_yr']*1200
ch4_leak['fee_1500'] = ch4_leak['ton_yr']*1500

#%% Social Cost of methane

# In 2015 the EPA calculated the social cost of CH4 as being:
# in 2015: $1000/ton
# in 2020: $1200/ton
# in 2025: $1400/ton
# in 2030: $1600/ton
# Ref: https://19january2017snapshot.epa.gov/climatechange/social-cost-carbon_.html
# Using those values, the social cost of CH4 leakage from the Uinta Basin was:
    
#45*24*365*1000 #= $394,200,000 (2015)
#25*24*365*1200 #= $262,800,000 (2020)

ch4_leak['social_cost_1000'] = ch4_leak['ton_yr']*1000
ch4_leak['social_cost_1500'] = ch4_leak['ton_yr']*1500

#%% GWP of CH4 from IPCC AR6
# GWP of fossil CH4 Table 7.15 pg 95 https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter07.pdf

# Note: fossil CH4 accounts for the CO2 after CH4 oxidation. This is slightly
# higher than biogenic CH4 which has a gwp100=27.0 and gwp20=79.7.
gwp100 = 29.8
gwp20 = 82.5

#%% Comparison of methane leakage in terms of Utah's CO2 emissions

ch4_leak['co2e_gwp100'] = ch4_leak['ton_yr']*gwp100/1e6
ch4_leak['co2e_gwp20'] = ch4_leak['ton_yr']*gwp20/1e6

# 2012
55*24*365*gwp20/1e6 # = 40.9 Million Metric Tons CO2 (2012)
55*24*365*gwp100/1e6 # = 14.5 Million Metric Tons CO2 (2012)

# 2015
45*24*365*gwp20/1e6 # = 33.5 Million Metric Tons CO2 (2015)
45*24*365*gwp100/1e6 # = 11.8 Million Metric Tons CO2 (2015)

# 2020
25*24*365*gwp20/1e6 # = 18.6 Million Metric Tons CO2 (2020)
25*24*365*gwp100/1e6 # = 6.5 Million Metric Tons CO2 (2020)

# https://www.eia.gov/environment/emissions/state/

# EIA: Table 4. 2018 State energy-related carbon dioxide emissions by sector (Million metric tons CO2)
#Commercial:     2.8
#Electric Power: 28.6 # WOW! 2020 leakage in 20yrGWP is ~2/3 all electric power emissions!
#Residential:    3.9
#Industrial:     7.0
#Transportation: 18.8 # WOW! 2020 leakage in 20yrGWP is about the same as ALL transportation CO2 emissions!
#Total:          61.1

# by fuel type:
# Coal:         26.1
# Petroleum:    21.6
# Natural gas:  13.5 # WOW! 2020 leakage in 20yrGWP is higher than CO2 emissions from natural gas usage!
# Total:        61.1

#%% Incerase in Utah's total CO2e emissions after accounting for methane leakage

# 2012 (total CO2 emissions: 61.4 MMTCO2)
100*(((45*24*365*gwp20/1e6)+61.4)/61.4-1) # = +53% (2015)
100*(((45*24*365*gwp100/1e6)+61.4)/61.4-1) # = +19% (2015)

# 2015 (total CO2 emissions: 63.5 MMTCO2)
100*(((45*24*365*gwp20/1e6)+63.5)/63.5-1) # = +51% (2015)
100*(((45*24*365*gwp100/1e6)+63.5)/63.5-1) # = +18% (2015)

# 2020 (total CO2 emissions: 61.1 MMTCO2): 
100*(((25*24*365*gwp20/1e6)+61.1)/61.1-1) # = +30% (2020)
100*(((25*24*365*gwp100/1e6)+61.1)/61.1-1) # = +11% (2020)

#%% Comparison of methane leakage with cars

# A typical passenger vehicle emits 4.6 tons of CO2/yr
# https://www.epa.gov/greenvehicles/greenhouse-gas-emissions-typical-passenger-vehicle

ch4_leak['car_gwp100'] = ch4_leak['co2e_gwp100']*1e6/4.6
ch4_leak['car_gwp20'] = ch4_leak['co2e_gwp20']*1e6/4.6


# 2012
55*24*365*gwp20/4.6 # = 8,640,978 cars! (using the 20yr GWP of CH4)
55*24*365*gwp100/4.6 # = 3,121,226 cars! (using the 100yr GWP of CH4)

# 2015
45*24*365*gwp20/4.6 # = 7,069,891 cars! (using the 20yr GWP of CH4)
45*24*365*gwp100/4.6 # = 2,553,730 cars! (using the 100yr GWP of CH4)

# 2020
25*24*365*gwp20/4.6 # = 3,927,717 cars! (using the 20yr GWP of CH4)
25*24*365*gwp100/4.6 # = 1,418,739 cars! (using the 100yr GWP of CH4)

# https://tax.utah.gov/econstats/mv/registrations
# in 2021 Utah had a total of 2.7 million cars and trucks registered in the state

#%% Production and consumption data in Utah

# Overall EIA state energy profile:
# https://www.eia.gov/state/analysis.php?sid=UT#47

# Natural gas production in Utah is about equal to consumption. 
# Between the mid-1990s & 2005 production was around 250,000 MCF. It increased
# after the fracking boom up to a peak of 490,000 MCF in 2012, then fell back to 
# 240,000 MCF in 2020 due to low natural gas prices.
# EIA Production data: https://www.eia.gov/dnav/ng/ng_prod_sum_dc_sut_mmcf_a.htm
# EIA Production chart: https://www.eia.gov/dnav/ng/hist/n9050ut2a.htm
# 
# Consumption was around 140,000MCF in the 1990s through 2005, then it increased
# to 200,000 MCF until 2018 when it increased again to 220,000 MCF
# EIA Consumption data: https://www.eia.gov/dnav/ng/ng_cons_sum_dcu_SUT_a.htm 
# EIA Consumption chart: https://www.eia.gov/dnav/ng/hist/n3060ut2a.htm

# In 2012:
100*178941/490393 # = Natural gas consumption was 36.5% of the volume produced in Utah
# In 2015:
100*188297/417020 # = Natural gas consumption was 45.1% of the volume produced in Utah
# In 2020:
100*225523/241989 # = Natural gas consumption was 93.2% of the volume produced in Utah
# in 2021:
100*223020/238884 # = Natural gas consumption was 93.4% of the volume produced in Utah


#%% Market value of natural gas leakage (kg CH4/hour to $/hour)

# $/mmbtu can be found on EIA
# https://www.eia.gov/naturalgas/weekly/#tabs-prices-2

# Historically natural gas was around $3.00/mmbtu, but it got up to around $8.50/mmbtu in 2013, but dropped back below $2.00/mmbtu in 2024
# EIA on natural gas prices 2024/7/22: https://www.eia.gov/todayinenergy/detail.php?id=62544
ch4_cost = pd.DataFrame(data={
    'emission_kg':[35000],
    'kg_ng/kg_ch4':[1/0.96],
    'specific_vol_m3_ng/kg_ng':[1.4025/1],
    'ft3/m3':[3.28048**3/1**3],
    'mcf/ft3':[1/1000],
    'mmbtu/mcf':[1.045/1], # EIA data for Utah https://www.eia.gov/dnav/ng/ng_cons_heat_a_EPG0_VGTH_btucf_a.htm
    'usd/mmbtu_past':[3.00/1],
    'usd/mmbtu_now':[3.00/1]})

# Also 1 mmbtu = 10 therms

cost = (ch4_cost['emission_kg']*ch4_cost['kg_ng/kg_ch4']*ch4_cost['specific_vol_m3_ng/kg_ng']*
            ch4_cost['ft3/m3']*ch4_cost['mcf/ft3']*ch4_cost['mmbtu/mcf']*ch4_cost['usd/mmbtu_now'])
print('Leakage of '+str(ch4_cost['emission_kg'][0])+' kg CH4/hr are worth $'+str(int(cost[0]))+'/hr ($'+str(int(cost[0]*365.25*24))+'/yr) at $'+str(ch4_cost['usd/mmbtu_now'][0])+'/mmbtu')

# Paste in excel:
# ch4kg_to_usd = (1/0.96)*(1.4025/1)*(3.28048**3/1**3)*(1/1000)*(1/1)*(8.50/1)
ch4kg_to_usd_now = (ch4_cost['kg_ng/kg_ch4']*ch4_cost['specific_vol_m3_ng/kg_ng']*
            ch4_cost['ft3/m3']*ch4_cost['mcf/ft3']*ch4_cost['mmbtu/mcf']*ch4_cost['usd/mmbtu_now'])[0]
1000*ch4kg_to_usd_now

# A metric ton is 1000 kg
ch4ton_to_usd_now = ch4kg_to_usd_now*1000

ch4_leak['usd_yr_now'] = ch4_leak['ton_yr']*ch4ton_to_usd_now

ch4kg_to_usd_past = (ch4_cost['kg_ng/kg_ch4']*ch4_cost['specific_vol_m3_ng/kg_ng']*
            ch4_cost['ft3/m3']*ch4_cost['mcf/ft3']*ch4_cost['mmbtu/mcf']*ch4_cost['usd/mmbtu_past'])[0]
ch4ton_to_usd_past = ch4kg_to_usd_past*1000
ch4_leak['usd_yr_past'] = ch4_leak['ton_yr']*ch4ton_to_usd_past

# A typical passenger vehicle emits 4.6 tons of CO2/yr
# https://www.epa.gov/greenvehicles/greenhouse-gas-emissions-typical-passenger-vehicle
# so a typical passenger vehicle emits 1000*4.6/(365.25*24) = 0.52 kg CO2/hour 
typical_car_kg_co2_hr = 1000*4.6/(365.25*24)

equivalent_to_gwp20 = int(ch4_cost['emission_kg']*gwp20/typical_car_kg_co2_hr)
equivalent_to_gwp100 = int(ch4_cost['emission_kg']*gwp100/typical_car_kg_co2_hr)

print('Leakage of '+str(ch4_cost['emission_kg'][0])+' kg CH4/hr have GWP20 CO2-equivalent emissions of '+str(equivalent_to_gwp20)+' typical cars')
print('Leakage of '+str(ch4_cost['emission_kg'][0])+' kg CH4/hr have GWP100 CO2-equivalent emissions of '+str(equivalent_to_gwp100)+' typical cars')

#% Leakage equivalent to annual residential consumption

# Estimate of annual residential natural gas consumption comes from the EIA 2020 RECS data, see excel spreadsheet.
# In the Mountain North region we have the following data:
# Population: 4.62 Million
# Annual natural gas residential consumption:
    # Total: 288 billion cubic feet
    # Space Heating: 203 billion cubic feet
    # Water Heating: 73 billion cubic feet
    # Other: 11 billion cubic feet

#*** Make sure ch4_cost['emission_kg'][0] is units of kg/hr
total_household_kg_ch4 = 288*1000*1000*(1/ch4_cost['mcf/ft3'])*(1/ch4_cost['ft3/m3'])*(1/ch4_cost['specific_vol_m3_ng/kg_ng'])*(1/ch4_cost['kg_ng/kg_ch4'])
typical_household_kg_ch4 = total_household_kg_ch4/4.62e6
typical_household_kg_ch4_hr = typical_household_kg_ch4/(365.25*24)
typical_number_households = int(ch4_cost['emission_kg'][0]/typical_household_kg_ch4_hr)
print('Leakage of '+str(ch4_cost['emission_kg'][0])+' kg CH4/hr is equivalent to the gas usage of '+str(typical_number_households)+' typical households in Utah')

#%% Methane leakage fee per 1 mmbtu

# prices are in mmbtu. How much does a x% leakage rate increase those prices?

ton_ch4_per_mmbtu = ((1/ch4_cost['mmbtu/mcf'])*(1/ch4_cost['mcf/ft3'])*(1/ch4_cost['ft3/m3'])*
        (1/ch4_cost['specific_vol_m3_ng/kg_ng'])*(1/ch4_cost['kg_ng/kg_ch4'])*(1/1000))
print(ton_ch4_per_mmbtu[0])


print(ton_ch4_per_mmbtu[0]*1500*0.02)

leak_rates = pd.DataFrame(data={'leak_rate': np.linspace(0,10,11)})
leak_rates['usd_per_mmbtu_900'] = 900*(leak_rates['leak_rate']/100)*ton_ch4_per_mmbtu[0]
leak_rates['usd_per_mmbtu_1200'] = 1200*(leak_rates['leak_rate']/100)*ton_ch4_per_mmbtu[0]
leak_rates['usd_per_mmbtu_1500'] = 1500*(leak_rates['leak_rate']/100)*ton_ch4_per_mmbtu[0]

fig, ax = plt.subplots(num=1)
ax.plot(leak_rates['leak_rate'],leak_rates['usd_per_mmbtu_900'], 'k--', label='$900/ton in 2024')
ax.plot(leak_rates['leak_rate'],leak_rates['usd_per_mmbtu_1200'], 'k:', label='$1200/ton in 2025')
ax.plot(leak_rates['leak_rate'],leak_rates['usd_per_mmbtu_1500'], 'k', label='$1500/ton in 2026')
ax.set_ylabel('Methane leakage fee (USD/mmbtu)')
ax.set_xlabel('Natural gas leakage rate')

legend = ax.legend(loc='upper left', shadow=True, fontsize='large')
plt.grid(visible=True,axis='both')

