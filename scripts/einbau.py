   
class ConvertTrack(BaseCommand):

    def convert_tracks(self, cfg, tub_paths, limit):
        '''
        Convert AI driven track data from tubs to training data.
        usage
        donkey convtrack --tub data/tub_48_20-04-16 --config ./myconfig.py
        
        '''
        import matplotlib.pyplot as plt
        import pandas as pd

        records = gather_records(cfg, tub_paths)

        records = records[:limit]
        num_records = len(records)
        print('processing %d records:' % num_records)
        print('tub_paths: ', tub_paths)

        ix = 0
        for record_path in records:
            # increment json file number counter
            ix +=1

            #print(record_path) # name of json file
            # read AI record
            with open(record_path, 'r') as fp:
                record = json.load(fp)
            #user_angle = float(record["user/angle"])
            #user_throttle = float(record["user/throttle"])
            pilot_angle = float(record["pilot/angle"])
            pilot_throttle = float(record["pilot/throttle"])
                        
            # store pilot/angle into user/angle 
            record["user/angle"]      = pilot_angle
            record["user/throttle"]   = pilot_throttle
            record["pilot/angle"]     = 0.0
            record["pilot/throttle"]  = 0.0

            # write modified record
            myoutput_path = "./data/AI_tub_48_20-04-16/record_"+str(ix)+".json"          
            try:
                with open(myoutput_path, 'w') as fp:
                    json.dump(record, fp)
                    #print('wrote record:', record)
            except TypeError:
                print('troubles with record:', json_data)
            except FileNotFoundError:
                raise
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
            

# t = create_sample_tub(tub_path, records=initial_records)
