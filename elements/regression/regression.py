#!/usr/bin/env python3

import pandas as pd
import numpy as np
import math

data = pd.read_csv("./../../datasets/forestfires.csv")
# data = data.sort_values(by=['area'])

y = data[['area']].values

# Applying the logarithm model to the area
for i in range(len(y)):
    y[i] = math.log(y[i]+1)

print(y)