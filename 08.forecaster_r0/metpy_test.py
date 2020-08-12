# coding: utf-8

import numpy as np
import pandas as pd

from metpy.units import units
from metpy.calc import dewpoint_from_relative_humidity, equivalent_potential_temperature

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    temp = [0, 5, 10, 15, 20, 25]
    rh = [100, 100, 100, 100, 100, 100]
    pres = [850, 850, 850, 850, 850, 850]
    
    df = pd.DataFrame({'Temp.': temp, 'Humidity': rh, 'Pressure': pres})
    print(df)
    
    print(df['Temp.'].values * units('deg'))
    print(df['Humidity'].values / 100.)
    print(df['Pressure'].values * 100.)
    
    # 露点温度の算出
    dewpoint = dewpoint_from_relative_humidity(
                    (df['Temp.'].values * units('degC')).to(units('K')),
                    df['Humidity'].values / 100.
    )
    print('##### 露点温度 #####')
    print(dewpoint)
    print(dewpoint.to(units('K')))
    
    # 相当温位の算出
    potensial_temp = equivalent_potential_temperature(
                        df['Pressure'].values * units('hPa'),
                        (df['Temp.'].values * units('degC')).to(units('K')),
                        dewpoint.to(units('K'))
        )
    print('##### 相当温位 #####')
    print(potensial_temp)
    
    #        'dewpoint': dewpoint_rh( (np.array(temp) * units('degC') ).to(units('K') ),
    #                            np.array(rh) / 100.).to(units('degF')),