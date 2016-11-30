import pandas as pd
import numpy as np
import random
import pymongo
import time
import re
import datetime
client = pymongo.MongoClient('143.248.156.197')

db = client.research

sillokManIndex=db.sillokManIndex
sillokManInfo = db.sillokManInfo
aksManIndex = db.aksManIndex

df= pd.DataFrame(list(aksManIndex.find()))
