import pandas as pd
class MixedCroping:
    def __init__(self, input_crop: str):
        self.input_crop = input_crop 
        self.__initialize_data()
    
    def __initialize_data(self):
        self.df = pd.read_csv("features/nutrients.csv")
        self.crop = self.df["Crop"]
        self.crop_index = {value: key for key, value in enumerate(self.crop)}
    
    def mixed_crop(self):
        common = {}
        mixed_crop = []
        crop_index = self.crop_index[self.input_crop]
        for i in range(len(self.crop)):
            if i != crop_index:
                check = self.df.iloc[crop_index] == self.df.iloc[i]
                for col, value in check.items():
                    if value:
                        try:
                            common[self.crop[i]].append(col)
                        except KeyError:
                            common[self.crop[i]] = [col]
        for i in common:
            if len(common[i]) in [1, 2]:
                mixed_crop.append(i)
        return mixed_crop

    def crop_info(self,crop_nutrients):
        crop_index = self.crop_index[crop_nutrients]
        return self.df.iloc[crop_index]

    
# mixed_crop_objects = MixedCroping('rice')
# print(mixed_crop_objects.mixed_crop())
