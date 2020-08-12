# coding: utf-8

import numpy as np
import pandas as pd

from metpy.units import units
from metpy.calc import dewpoint_from_relative_humidity

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    
    length = 10.4 * units.inches
    width = 20 * units.meters
    print(length, width)
    
    array = [length.magnitude, width.magnitude]
    print(array)
    
    temp = [273, 274, 275, 276, 277]
    rh = [100, 90, 90, 90, 90]
    
    df = pd.DataFrame({'Temp.': temp, 'Humidity': rh})
    print(df)
    
    print(df['Temp.'].values * units('K'))
    print(df['Humidity'].values / 100.)
    
    # 露点温度の算出
    dewpoint = dewpoint_from_relative_humidity(
                    (df['Temp.'].values * units('K')),
                    df['Humidity'].values / 100.
    )
    print(dewpoint.to(units('K')))
    
    #        'dewpoint': dewpoint_rh( (np.array(temp) * units('degC') ).to(units('K') ),
    #                            np.array(rh) / 100.).to(units('degF')),