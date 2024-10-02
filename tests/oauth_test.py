
#POST https://authorization-server.com/token
#client_id	    j3CziWgbG1xyvWBcfGAiGris
#client_secret	AcOWNGc7x1SPfjH-ZhLlJVSqA-xP_gGHkPfIDU5Wdo7yQhxg
#User Account
#https://oauth.com
#login	    kind-quoll@example.com
#password	Quaint-Curlew-99

from oadr30.vtn import VTNOps
from oadr30.log import oadr3_log_critical
from oadr30.price_server_client import PriceServerClient
import json


#isyp_base_url = "https://dev.isy.io"
#isyp_auth_url = "/o2/token"  
#isyp_client_id="isyportal-o2-unsubscribe"
#isyp_client_secret="testsecret" 

base_url = "http://localhost:8026/openadr3/3.0.1"
auth_url = "/auth/token"  
client_id="ven_client"
client_secret="999" 

def main():
    try:
#        vtn = VTNOps(base_url=base_url, auth_url=auth_url, client_id=client_id, client_secret=client_secret, auth_token_url_is_json=True )
#        vtn.create_ven("crap")
#        vtn.get_programs()
#        vtn.get_program('0')
#        events = vtn.get_events()

        client= PriceServerClient('https://api.olivineinc.com/i/lbnl/v1/prices/cfh/SummerHDP_MD/OpenADR3')
        events= client.get_events()
        se = json.dumps(events, indent=4)
        print (se)
#        vtn.get_events('0')
      #  vtn.__get_token__()
      #  vtn.__send_request__('POST', url='https://dev.isy.io/api/unsubscribe', body='email=crap@crap.com')

    except Exception as ex:
        oadr3_log_critical("main failed")





if __name__ == "__main__":
    main()