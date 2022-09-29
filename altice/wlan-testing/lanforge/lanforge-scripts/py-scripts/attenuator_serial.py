import sys
import os
import importlib
import time

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))

lfcli_base = importlib.import_module("py-json.LANforge.lfcli_base")
LFCliBase = lfcli_base.LFCliBase
LFRequest = importlib.import_module("py-json.LANforge.LFRequest")
LFUtils = importlib.import_module("py-json.LANforge.LFUtils")

class AttenuatorSerial(LFCliBase):
    def __init__(self, lfclient_host, lfclient_port,  debug_=False):
        super().__init__(lfclient_host, lfclient_port, debug_)
        self.lfclient_host = lfclient_host
        self.COMMANDS = ["show_attenuators", "set_attenuator"]
        self.atten_serno = ""
        self.atten_idx = ""
        self.atten_val = ""
        self.atten_data = {
            "shelf": 1,
            "resource": 1,
            "serno": None,
            "atten_idx": None,
            "val": None,
            "mode": None,
            "pulse_width_us5": None,
            "pulse_interval_ms": None,
            "pulse_count": None,
            "pulse_time_ms": None
        }

    def show(self, debug=False):
        ser_no_list = []
        print("Show Attenuators.........")
        response = self.json_get("/attenuators/")
        print(f"atten : {response}")
        time.sleep(0.01)
        if response is None:
            print(response)
            raise ValueError("Cannot find any endpoints")
        else:
            attenuator_resp = response["attenuator"]
            if "entity id" in attenuator_resp.keys():
                key = attenuator_resp["entity id"]
                print(f"key : {key}")
                ser_no_list.append(key)
            # for i in attenuator_resp:
            #     for key in i:
            #         if key == "entity id":
            #             print("entity id")
            #         # print("%s " % (key))
            #         ser_no_list.append(key)

        return ser_no_list
def main():
    obj = AttenuatorSerial(lfclient_host="localhost", lfclient_port=8802)
    x = obj.show()
    print("out",x)


if __name__ == '__main__':
    main()