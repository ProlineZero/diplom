import json
import requests
import time

url = 'https://carguider.ru/'
urlAdd = 'https://carguider.ru/api/add/'
pictUrl = 'resources/pictures/'

def _vol_if_key_exist(key, dict) :
    if key in dict :
        return dict[key]
    else :
        return None

def main() :
    
    with open("baseN.json", "r", encoding="utf8") as dataFile:
        raw_data = json.load(dataFile)
        i = 0
        cnt = 0
        data = []
        for brand in raw_data :
            brand_name = brand["name"]
            country = brand["country"]

            for model in brand["models"] :
                model_name = model["name"]
                if brand_name == 'Mitsubishi':
                    cnt += 1
                
                for gen in model["generations"] :
                    gen_name = gen["name"]
                    year_begin = gen["year-start"]
                    year_end = gen["year-stop"]
                    
                    for config in gen["configurations"] :
                        pict_name = config["id"]
                        body_type = config["body-type"]
                        
                        for modification in config["modifications"] :
                            id = str(int(modification["complectation-id"]) + 1)
                            engine_type = _vol_if_key_exist("engine-type", modification["specifications"])
                            transmission_type = _vol_if_key_exist("transmission", modification["specifications"])
                            horse_power = _vol_if_key_exist("horse-power", modification["specifications"])
                            kwt_power = _vol_if_key_exist("kvt-power", modification["specifications"])
                            engine_capacity = _vol_if_key_exist("volume-litres", modification["specifications"])
                            torque = _vol_if_key_exist("moment", modification["specifications"])
                            drive = _vol_if_key_exist("drive", modification["specifications"])
                            cylinders_order = _vol_if_key_exist("cylinders-order", modification["specifications"])
                            cylinders_value = _vol_if_key_exist("cylinders-value", modification["specifications"])
                            body_length = _vol_if_key_exist("length", modification["specifications"])
                            body_width = _vol_if_key_exist("width", modification["specifications"])
                            body_height = _vol_if_key_exist("height", modification["specifications"])
                            front_brake = _vol_if_key_exist("front-brake", modification["specifications"])
                            back_brake = _vol_if_key_exist("back-brake", modification["specifications"])
                            if len(modification["specifications"]["seats"]) > 1 :
                                seats = modification["specifications"]["seats"][1]
                            else :
                                seats = modification["specifications"]["seats"][0]
                            weight = _vol_if_key_exist("weight", modification["specifications"])
                            max_speed = _vol_if_key_exist("max-speed", modification["specifications"])
                            time_to_100 = _vol_if_key_exist("time-to-100", modification["specifications"])
                            
                            # if "moment" not in modification["specifications"]:
                            #     print(brand_name, model_name, engine_type)
                            
                            car = {
                                'id': id,
                                'country': country,
                                'brand': brand_name,
                                'model': model_name,
                                'generation': gen_name,
                                'year_begin': year_begin,
                                'year_end': year_end,
                                'body_type': str(body_type).title() if body_type else body_type,
                                'body_length': body_length,
                                'body_width': body_width,
                                'body_height': body_height,
                                'weight': weight,
                                'seats': seats,
                                'pict_url': f'{url}{pictUrl}{pict_name}.jpg',
                                'engine_type': str(engine_type).title() if engine_type else engine_type,
                                'transmission_type': str(transmission_type).title() if transmission_type else transmission_type,
                                'drive_type': str(drive).title() if drive else drive,
                                'engine_capacity': engine_capacity,
                                'cylinders_order': str(cylinders_order).title() if cylinders_order else cylinders_order,
                                'cylinders_value': cylinders_value,
                                'horse_power': horse_power,
                                'kwt_power': kwt_power,
                                'torque': torque,
                                'max_speed': max_speed,
                                'time_to_100': time_to_100,
                                'front_brakes': str(front_brake).title() if front_brake else front_brake,
                                'back_brakes': str(back_brake).title() if back_brake else back_brake
                            }
                            data.append(car)
                            
                            if len(data) == 200:
                                i+=2
                                if i > 242:
                                    requests.post(urlAdd, json=data)
                                    print('posted packet number ', i)
                                    time.sleep(10)
                                data.clear()
                            
        requests.post(urlAdd, json=data)
        
main()