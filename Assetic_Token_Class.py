import requests
import base64
import pandas as pd
from datetime import datetime
import sys
sys.path.append('YourPath') #change this to your path
import Admin

class AsseticAPI:
    def __init__(self):
        self.log_df = pd.DataFrame(columns=['Process', 'Status', 'Status Code', 'Error Detail', 'Time'])
    
    def get_token(self, username, password, url):
        
        """
        This function retrieves the token required for authentication, 
        pass in your username and password from registering within the Assetic Portal
        """
        try:
            credentials = (username + ':' + password)
            b64_credentials = base64.b64encode(credentials.encode('ascii'))
            headers = {'Authorization': 'Basic %s' % b64_credentials.decode('ascii')}
            resp = requests.get(url, headers=headers)
            
            if resp.status_code != 200:
                print("Status code {} on Assetic Token request - on date {}.".format(resp.status_code, (str(datetime.now().replace(microsecond=0)))))
                self.log_df = self.log_df.append({'Process': 'Get Token', 'Status': resp.status_code, 'Error Detail': 'Network Error', 'Time': (str(datetime.now().replace(microsecond=0)))}, ignore_index=True)
                
                return self.log_df
            
            response = resp.json()
            
            return response
        
        except Exception as e:
            self.log_df = self.log_df.append({'Process': 'Get Token', 'Status': 'Error', 'Error Detail': e, 'Time': (str(datetime.now().replace(microsecond=0)))}, ignore_index=True)
            print("Error on report Assetic Token on error message {}.".format(e))
            return self.log_df
    
    def get_assets(self, url, token):
        
        """
        This function demonstrates an example for retrieving the assets table with the token above, 
        """
        try:
            session = requests.Session()
            basic_auth = (Admin.Username, token)
            session.auth = basic_auth
            resp = session.get(url)
            
            if resp.status_code != 200:
                print("Status code {} on Assetic Token request - on date {}.".format(resp.status_code, (str(datetime.now().replace(microsecond=0)))))
                self.log_df = self.log_df.append({'Process': 'Get Assets', 'Status': resp.status_code, 'Error Detail': 'Network Error', 'Time': (str(datetime.now().replace(microsecond=0)))}, ignore_index=True)
                
                return self.log_df
            
            df = pd.json_normalize(resp.json())
            TotalPage = df['TotalPages'].iloc[0] #retrieve page number from response
            
            #Loop Pagination
            for i in range(1,TotalPage+1):
                URLLogic = url[:-6] + 'Page=' + str(i)  #remove 'page=1' from the passed URL and index loop it
                resp = session.get(URLLogic)
                
                if resp.status_code != 200: 
                    print("Status code {} on Assetic Token request - on date {}.".format(resp.status_code,(str(datetime.now().replace(microsecond=0)))))
                    self.log_df = self.log_df.append({'Process':'Get Assets','Status':resp.status_code,'Error Detail':'Network Error', 'Time':(str(datetime.now().replace(microsecond=0)))}, ignore_index=True)
                    
                    return self.log_df
                
                df = pd.json_normalize(resp.json())
                
                for a in df['ResourceList']:
                    df = pd.json_normalize(a) #
                    df['Page'] = i
                    df['TotalPage'] = TotalPage
                    
                    #Function to do something with data
            
            return df
        
        except Exception as e:
            self.log_df = self.log_df.append({'Process': 'Get Assets', 'Status': 'Error', 'Error Detail': e, 'Time': (str(datetime.now().replace(microsecond=0)))}, ignore_index=True)
            print("Error on report Assetic Token on error message {}.".format(e))
            
            return self.log_df

if __name__ == '__main__':
    assetic = AsseticAPI()
    token = assetic.get_token(Admin.Username,Admin.Password,Admin.URL)
    Assets = assetic.get_assets(Admin.Asset_URL,token)
