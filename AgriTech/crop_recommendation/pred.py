import pickle 
import pandas as pd 
from geopy.geocoders import Nominatim
import requests
import numpy as np
from sklearn.preprocessing import FunctionTransformer
geolocator = Nominatim(user_agent = "my_app")

crop = {'rice': 0,
 'maize': 1,
 'chickpea': 2,
 'kidneybeans': 3,
 'pigeonpeas': 4,
 'mothbeans': 5,
 'mungbean': 6,
 'blackgram': 7,
 'lentil': 8,
 'pomegranate': 9,
 'banana': 10,
 'mango': 11,
 'grapes': 12,
 'watermelon': 13,
 'muskmelon': 14,
 'apple': 15,
 'orange': 16,
 'papaya': 17,
 'coconut': 18,
 'cotton': 19,
 'jute': 20,
 'coffee': 21
}




def log_transform(X):
    return np.log(X)

data_conq = crop_consequences = {
  "rice": [
      "Soil depletion (nitrogen, potassium)",
      "Increased salinity (in some regions with irrigation)",
      "Water usage (moderate, but can strain resources in dry areas)",
      "May contribute to methane emissions in flooded rice paddies",
      "Potential for increased herbicide resistance in weeds with continuous use",
      "May attract pests like rice water weevil and rice stink bug",
      "Can harbor diseases like blast and sheath blight if not managed properly",
      "Monoculture practices can reduce biodiversity and soil health in the long run",
      "Excessive water usage can lead to water table depletion in some areas",
      "Improper residue management after harvest can increase disease and pest problems"
  ],
  "maize": [
      "Soil erosion (especially with monoculture and tilling)",
      "Nutrient depletion (nitrogen, phosphorus)",
      "Water usage (moderate to high depending on variety and climate)",
      "May contribute to soil compaction with heavy machinery use",
      "Potential for leaching of nitrates into groundwater with excessive fertilization",
      "Can attract pests like corn earworm and fall armyworm",
      "Susceptible to diseases like northern corn leaf blight and maize rust",
      "Monoculture practices can reduce biodiversity and soil health in the long run",
      "Heavy reliance on herbicides can lead to weed resistance",
      "Improper residue management after harvest can increase disease and pest problems"
  ],
  "chickpea": [
      "Generally considered a nitrogen-fixing crop that can improve soil fertility",
      "May increase soil salinity in some conditions with poor drainage",
      "Moderate water usage",
      "Can attract pests like pod borer and aphids",
      "Susceptible to diseases like wilt and blight",
      "Requires well-drained soils and may not perform well in heavy clay soils",
      "Fixed nitrogen benefit can be reduced with excessive phosphorus application",
      "Crop rotation is important to prevent disease buildup in the soil",
      "Early planting can help avoid heat stress and improve yields",
      "Proper weed management is crucial as chickpeas are not competitive with weeds"
  ],
  "kidneybeans": [
      "Generally considered a nitrogen-fixing crop that can improve soil fertility",
      "May increase soil acidity in some conditions, requiring lime application",
      "Moderate water usage",
      "Can attract pests like Mexican bean beetle and bean weevils",
      "Susceptible to diseases like anthracnose and rust",
      "Requires well-drained soils and may not perform well in waterlogged conditions",
      "Fixed nitrogen benefit can be reduced with excessive phosphorus application",
      "Crop rotation is important to prevent disease buildup in the soil and improve soil health",
      "Proper inoculation with specific rhizobia bacteria strains can enhance nitrogen fixation",
      "Early planting can help avoid heat stress and improve yields"
  ],
  "pigeonpeas": [
      "Generally considered a nitrogen-fixing crop that can improve soil fertility",
      "May contribute to soil erosion in sloping lands if not managed with cover crops",
      "Moderate water usage",
      "Can attract pests like pod borers and psyllids",
      "Susceptible to diseases like wilt and blight",
      "Requires well-drained soils and may not tolerate waterlogging",
      "Fixed nitrogen benefit can be reduced with excessive phosphorus application",
      "Crop rotation is important to prevent disease buildup in the soil",
      "Intercropping with other crops can improve soil health and provide additional benefits",
      "Proper pruning can promote good airflow and reduce disease pressure"
  ],
  "mothbeans": [
      "Generally considered a nitrogen-fixing crop that can improve soil fertility",
      "May require proper management to prevent excessive water usage, especially in humid climates",
      "Relatively low water usage compared to some other crops",
      "Can attract pests like pod borers and aphids",
      "Susceptible to diseases like wilt and blight",
      "Requires well-drained soils and may not tolerate waterlogging",
      "Fixed nitrogen benefit can be reduced with excessive phosphorus application",
      "Crop rotation is important to prevent disease buildup in the soil",
      "Can be a good cover crop option for suppressing weeds and improving soil health",
      "Early planting can help avoid heat stress and improve yields"
  ],
   "mungbean": [
      "Generally considered a nitrogen-fixing crop that can improve soil fertility",
      "May increase soil susceptibility to diseases if not rotated with other crops",
      "Moderate water usage",
      "Can attract pests like bean beetles and aphids",
      "Susceptible to diseases like mungbean yellow mosaic virus and bacterial wilt",
      "Requires well-drained soils and may not tolerate waterlogging",
      "Fixed nitrogen benefit can be reduced with excessive phosphorus application",
      "Crop rotation is crucial for managing diseases and improving soil health",
      "Inoculation with specific rhizobia bacteria strains can enhance nitrogen fixation",
      "Proper weed management is important, especially during early growth stages"
  ],
  "blackgram": [
      "Generally considered a nitrogen-fixing crop that can improve soil fertility",
      "May increase soil acidity in some conditions, requiring lime application",
      "Moderate water usage",
      "Can attract pests like pod borers and aphids",
      "Susceptible to diseases like blackgram wilt and cercospora leaf spot",
      "Requires well-drained soils and may not perform well in waterlogged conditions",
      "Fixed nitrogen benefit can be reduced with excessive phosphorus application",
      "Crop rotation is important to prevent disease buildup in the soil",
      "Inoculation with specific rhizobia bacteria strains can enhance nitrogen fixation",
      "Early planting can help avoid heat stress and improve yields"
  ],
  "lentil": [
      "Generally considered a nitrogen-fixing crop that can improve soil fertility",
      "May not perform well in hot and humid conditions",
      "Relatively low water usage",
      "Can attract pests like aphids and bruchid beetles",
      "Susceptible to diseases like wilt and blight",
      "Requires well-drained soils with good air circulation",
      "Fixed nitrogen benefit can be reduced with excessive phosphorus application",
      "Crop rotation is important to prevent disease buildup in the soil",
      "Early planting is recommended in warmer climates to avoid heat stress",
      "Proper weed control is crucial during early establishment"
  ],
  "pomegranate": [
      "Moderate water usage",
      "May contribute to soil salinity with excessive irrigation in arid regions",
      "Requires well-drained soils and does not tolerate waterlogging",
      "Susceptible to diseases like fungal wilt and fruit rot",
      "Can attract pests like pomegranate butterfly and mealybugs",
      "Requires proper pruning techniques to maintain fruit quality and tree health",
      "Boron deficiency can affect fruit quality and requires monitoring",
      "Pollination can be a factor, and some growers may use honeybees to improve fruit set",
      "Climate and soil conditions can significantly impact pomegranate yields and quality",
      "Susceptible to sunburn if fruit is not protected from excessive sunlight"
  ],
  "banana": [
      "High water usage",
      "May contribute to soil erosion on sloping lands if not managed with proper practices",
      "Requires well-drained, fertile soils with good organic matter content",
      "Susceptible to diseases like banana bunchy top virus and fungal diseases",
      "Can attract pests like banana weevil and aphids",
      "Requires wind protection in exposed areas",
      "Proper management of suckers is crucial for optimal yields",
      "Micronutrient deficiencies can occur, and regular soil testing is recommended",
      "Vulnerable to damage from strong winds and storms",
      "Post-harvest handling practices significantly impact fruit quality and shelf life"
  ],
  "mango": [
      "Moderate water usage",
      "May contribute to soil salinity with excessive irrigation in arid regions",
      "Requires well-drained soils and does not tolerate waterlogging",
      "Susceptible to diseases like mango malformation and anthracnose",
      "Can attract pests like fruit flies and mealybugs",
      "Requires proper pruning techniques to maintain fruit quality and tree health",
      "Nutrient deficiencies like potassium deficiency can affect fruit quality",
      "Pollination can be a factor, and some growers may use honeybees to improve fruit set",
      "Climate and soil conditions can significantly impact mango yields and quality",
      "Susceptible to sunburn if fruit is not protected from excessive sunlight"
  ],
  "watermelon": [
      "High water usage, can strain resources in dry areas, requiring efficient irrigation practices",
      "May contribute to soil erosion in sloping lands if not managed with cover crops",
      "Susceptible to diseases like fusarium wilt and anthracnose",
      "Can attract pests like aphids and cucumber beetles",
      "Requires well-drained, warm soils and may not tolerate frost",
      "Pollination can be a factor, and some growers may use honeybees to improve fruit set",
      "Proper mulching is important for weed control, moisture retention, and soil temperature regulation",
      "Staggered planting can help extend the harvest season",
      "Fruit quality and sweetness are highly dependent on weather conditions",
      "Susceptible to sunburn if fruit is not protected from excessive sunlight"
  ],
  "muskmelon": [
      "Moderate to high water usage, depending on variety and climate",
      "May contribute to soil erosion in sloping lands if not managed with cover crops",
      "Susceptible to diseases like powdery mildew and downy mildew",
      "Can attract pests like aphids and cucumber beetles",
      "Requires well-drained, warm soils and may not tolerate frost",
      "Pollination can be a factor, and some growers may use honeybees to improve fruit set",
      "Proper mulching is important for weed control, moisture retention, and soil temperature regulation",
      "Staggered planting can help extend the harvest season",
      "Fruit quality and sweetness are highly dependent on weather conditions",
      "Susceptible to sunburn if fruit is not protected from excessive sunlight"
  ],
  "apple": [
      "Moderate water usage",
      "May contribute to soil erosion on sloping lands if not managed with proper practices",
      "Requires well-drained soils with good air circulation and winter chilling hours",
      "Susceptible to diseases like apple scab and fire blight",
      "Can attract pests like codling moth and aphids",
      "Requires proper pruning techniques to maintain fruit quality and tree health",
      "Nutrient deficiencies can occur, and regular soil testing is recommended",
      "Pollination can be a factor, and some growers may use honeybees to improve fruit set",
      "Climate and soil conditions can significantly impact apple yields and quality",
      "Susceptible to sunburn if fruit is not protected from excessive sunlight"
  ],
  "orange": [
      "Moderate water usage",
      "May contribute to soil salinity with excessive irrigation in arid regions",
      "Requires well-drained soils and does not tolerate waterlogging",
      "Susceptible to diseases like citrus greening and citrus canker",
      "Can attract pests like citrus psyllid and scale insects",
      "Requires proper pruning techniques to maintain fruit quality and tree health",
      "Nutrient deficiencies like zinc deficiency can affect fruit quality",
      "Pollination can be a factor, and some growers may use honeybees to improve fruit set",
    "climate and soil conditions can significantly impact orange yields and quality",
      "Susceptible to sunburn if fruit is not protected from excessive sunlight"
  ],
  "papaya": [
      "Moderate water usage",
      "May contribute to soil erosion on sloping lands if not managed with proper practices",
      "Requires well-drained soils with good organic matter content",
      "Susceptible to diseases like papaya ringspot virus and fungal diseases",
      "Can attract pests like fruit flies and mealybugs",
      "Proper pruning and management of suckers is crucial for optimal yields",
      "Nutrient deficiencies can occur, and regular soil testing is recommended",
      "Pollination can be a factor, and wind or hand pollination techniques may be used",
      "Climate and soil conditions can significantly impact papaya yields and quality",
      "Susceptible to sunburn if fruit is not protected from excessive sunlight"
  ],
  "coconut": [
      "Relatively low water usage once established",
      "May contribute to soil potassium deficiency over time",
      "Tolerates a wide range of soil conditions but prefers well-drained soils",
      "Susceptible to diseases like bud rot and lethal yellowing",
      "Can attract pests like coconut beetle and rhinoceros beetle",
      "Requires proper management practices to maintain productivity",
      "Nutrient deficiencies like magnesium deficiency can affect nut quality",
      "Wind and storms can damage trees and reduce yields",
      "Long lifespan of trees requires long-term planning for coconut plantations",
      "Harvesting coconuts can be labor-intensive"
  ],
  "cotton": [
      "High water usage, can strain resources in dry areas, requiring efficient irrigation practices",
      "May contribute to soil erosion if not managed with cover crops and conservation tillage",
      "Requires well-drained soils and does not tolerate waterlogging",
      "Susceptible to diseases like boll rot and verticillium wilt",
      "Can attract pests like boll weevil and cotton aphid",
      "Heavy reliance on insecticides can lead to pest resistance",
      "Herbicide use can impact soil health and require careful management",
      "Genetically modified (GM) cotton varieties are widely used, raising concerns about potential environmental and health impacts",
      "Fair trade practices are important to ensure fair compensation for cotton growers",
      "Cotton production can have significant water footprint and environmental impact"
  ],
  "jute": [
      "Moderate water usage",
      "May deplete soil nutrients if not properly managed with crop rotation and nutrient amendments",
      "Requires well-drained, fertile soils with good organic matter content",
      "Susceptible to diseases like stem rot and anthracnose",
      "Can attract pests like jute semilooper and capsule borer",
      "Fiber quality can be affected by weather conditions during growth",
      "Retting process, which separates fibers from stems, can pollute water bodies if not managed properly",
      "Jute production is often labor-intensive, and fair trade practices are important",
      "Competition from synthetic fibers can impact jute market prices",
      "Sustainable jute production practices are being developed to minimize environmental impact"
  ],
  "coffee": [
      "Grown under shade trees in some regions, which can benefit soil health and biodiversity",
      "Requires specific climatic conditions and well-drained soils",
      "Susceptible to diseases like coffee rust and leaf rust",
      "Can attract pests like coffee berry borer and leaf miner",
      "Decaffeination process can use chemicals or water-intensive methods",
      "Fair trade practices are important to ensure fair compensation for coffee growers",
      "Deforestation for coffee plantations can be a major environmental concern",
      "Shade-grown coffee practices can help mitigate deforestation impacts",
      "Coffee prices can be volatile, impacting the livelihoods of coffee-growing communities",
      "Climate change can threaten coffee production in some regions"
  ]
}

crop_val_list = list(crop.values())
crop_key_list = list(crop.keys())

class CropRecommendation:
    def __init__(self,N :float, Ph:float , K:float , temp:float , humidity:float , rainfall:float,ph:float):
        self.N = N
        self.Ph = Ph 
        self.K = K 
        self.temp = temp 
        self.humidity = humidity
        self.rainfall = rainfall
        self.ph = ph 
        
    def pred(self):
        # Calling Saved Machine Learning Model 
        with open('crop_recommendation\crop_prediction_updated.pkl', 'rb') as file:
                rf_classifier = pickle.load(file)

        # data entries 
        data = {'Nitrogen':[self.N], 'phosphorus':[self.Ph], 'potassium':[self.K], 'temperature':[self.temp], 'humidity':[self.humidity], 'ph':[self.ph],
       'rainfall':[self.rainfall]}
        df = pd.DataFrame(data)

        transformer = FunctionTransformer(log_transform)
        df['potassium'] = transformer.transform(df["potassium"])
        df["rainfall"] = transformer.transform(df["rainfall"])

        pred = rf_classifier.predict(df)
        val = crop_val_list.index(pred[0])
        return crop_key_list[val].capitalize() 
    
    def conseqen(self,crop):
        ans = data_conq[crop]
        return ans
        
class LocationInfo:
    def __init__(self,city):
        self.city = city 

    def info (self):
        geolocator = Nominatim(user_agent = "my_app")
        location = geolocator.geocode(f"{self.city}")
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={location.latitude:.2f}&lon={location.longitude:.2f}&appid=3ccc69be6cd2557f982e77471acff49e"
        response = requests.get(url)
        if response.status_code == 200:
            res = response.json()
            ans = res["main"]
            humidity = ans['humidity']
            lan = f'{location.latitude:.2f}'
            long = f'{location.longitude:.2f}'
            temp = ans["temp"] - 273.15
            return humidity , lan , long , temp 
        else:
            return "Error"

