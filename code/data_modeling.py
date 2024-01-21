
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import math
import geopy.distance
import requests
from data_wrangling import *

df = pd.read_csv("datasets/updated_mlb.csv")