# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 16:07:50 2021

@author: Logan Mitchell
"""

#%%

# https://www.iea.org/countries/russia
tj = 25786288 # EIA ch4 production in 2013 in terrajoules
mmcf = tj*0.94781712 # terrajoules to million cubic feet of natural gas

# https://www.ucsusa.org/sites/default/files/attach/2015/03/climate-risks-of-natural-gas-fugitive-methane-emissions_methodology.pdf
# Mass Density from UCS = 0.678 kg/m3 (specific vol=1.474 m3/kg)
# Another gas density calculator: https://www.unitrove.com/engineering/tools/gas/natural-gas-density
# Mass Density (15C, 96.5% CH4 content) = 0.712 kg/m3 (specific vol=1.405 m3/kg)
# Mass Density (21C, 96.5% CH4 content) = 0.698 kg/m3 (specific vol=1.433 m3/kg)
# mmtch4 = mmcf*(meter^3/feet^3)*(mass density kg/m3)*(1metric ton/1000kg)
mmtch4 = mmcf*0.0283168*0.712*(1/1e3) # mmcf to million metric tons CH4

# https://www.washingtonpost.com/climate-environment/interactive/2021/russia-greenhouse-gas-emissions/
# Russian leakage in 2013 differed between reports. 
# 2015 report: ~33 million metric tons CH4 
# 2021 report: ~5 million metric tons CH4
pctleak_high = 100*33/mmtch4 # = 6.7% leakage
pctleak_low = 100*5/mmtch4   # = 1% leakage

100*34/mmtch4
# So, Russian gas leakage estimates are 1% on the low end & 6.7% on the high end.
# Uinta Basin gas leakage is as high as the highest estimates of Russian gas leakage.
 
#%%

# The emissions for the Uinta basin are calculated at ~25,000-45,000 kg/hr in the record.   
# A metric ton is 1000 kg, so that means 25-45 tons/hr.  
# Multiply by 8760 h/yr = 219000 to 394200 tons/yr.
55*24*365 #= 481800 (2012)
45*24*365 #= 394200 (2015)
25*24*365 #= 219000 (2020)

# I just saw that the reconciliation bill is proposing a $900/ton fee for methane leakage.  
# That would mean that the Uinta basin operators could be paying $197-354 million in leakage fees per year.
45*24*365*900 #= $354780000 (2015)
25*24*365*900 #= $197100000 (2020)

#%% GWP of CH4 from IPCC
# GWP of CH4 pg 73 https://www.ipcc.ch/site/assets/uploads/2018/02/WG1AR5_Chapter08_FINAL.pdf
gwp100 = 28
gwp20 = 84

#%% Comparison of methane leakage in terms of Utah's CO2 emissions

# 2012
55*24*365*gwp20/1e6 # = 40.5 Million Metric Tons CO2 (2012)
55*24*365*gwp100/1e6 # = 13.5 Million Metric Tons CO2 (2012)

# 2015
45*24*365*gwp20/1e6 # = 33.1 Million Metric Tons CO2 (2015)
45*24*365*gwp100/1e6 # = 11.0 Million Metric Tons CO2 (2015)

# 2020
25*24*365*gwp20/1e6 # = 18.4 Million Metric Tons CO2 (2020)
25*24*365*gwp100/1e6 # = 6.1 Million Metric Tons CO2 (2020)

18*24*365*gwp20/1e6 # = 18.4 Million Metric Tons CO2 (2020)


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
100*(((45*24*365*gwp20/1e6)+61.4)/61.4-1) # = +53.9% (2015)
100*(((45*24*365*gwp100/1e6)+61.4)/61.4-1) # = +18.0% (2015)

# 2015 (total CO2 emissions: 63.5 MMTCO2)
100*(((45*24*365*gwp20/1e6)+63.5)/63.5-1) # = +52.1% (2015)
100*(((45*24*365*gwp100/1e6)+63.5)/63.5-1) # = +17.4% (2015)

# 2020 (total CO2 emissions: 61.1 MMTCO2): 
100*(((25*24*365*gwp20/1e6)+61.1)/61.1-1) # = +30.1% (2020)
100*(((25*24*365*gwp100/1e6)+61.1)/61.1-1) # = +10.0% (2020)

#%% Comparison of methane leakage with cars

# A typical passenger vehicle emits 4.6 tons of CO2/yr
# https://www.epa.gov/greenvehicles/greenhouse-gas-emissions-typical-passenger-vehicle

# 2012
55*24*365*gwp20/4.6 # = 8,798,086 cars! (using the 20yr GWP of CH4)
55*24*365*gwp100/4.6 # = 2,932,695 cars! (using the 100yr GWP of CH4)

# 2015
45*24*365*gwp20/4.6 # = 7,198,434 cars! (using the 20yr GWP of CH4)
45*24*365*gwp100/4.6 # = 2,399,478 cars! (using the 100yr GWP of CH4)

# 2020
25*24*365*gwp20/4.6 # = 3,999,130 cars! (using the 20yr GWP of CH4)
25*24*365*gwp100/4.6 # = 1,333,043 cars! (using the 100yr GWP of CH4)

# https://tax.utah.gov/econstats/mv/registrations
# in 2021 Utah had a total of 2.7 million cars and trucks registered in the state


