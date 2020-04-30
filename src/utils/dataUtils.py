import pandas as pd
import numpy as np
import os
import datetime
 

def store_as_csv(data, target_img_path, image_prefix):
    try:
        df = pd.DataFrame(np.array(data), columns=['image_name', 'time', 'weather'])
        os.makedirs(target_img_path + '/csvs',exist_ok=True)
        df.to_csv(path_or_buf=target_img_path + "/csvs/{}.csv" .format(image_prefix))
    except Exception as e:
        print('---store as csv failed---')
        print(e)

def image_prefix_generator(city):
    try:
        d = datetime.datetime.today()
        date = d.strftime('%Y-%m-%d')
        return '{}_{}'.format(city, date)
    except Exception as e:
        print('---image prefix generate failed---')
        print(e)