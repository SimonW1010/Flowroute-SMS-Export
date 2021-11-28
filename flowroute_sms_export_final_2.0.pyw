import wx
import json
from flowroutenumbersandmessaging.flowroutenumbersandmessaging_client import FlowroutenumbersandmessagingClient
import os

client = FlowroutenumbersandmessagingClient('Access Key', 'Secret Key')
messages_controller = client.messages


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Flowroute export')
        panel = wx.Panel(self)

        self.SetSize(wx.Size(350, 200))

        my_btn = wx.Button(panel, label='Download', pos=(125, 80))
        my_btn.Bind(wx.EVT_BUTTON, self.on_press)

        self.Show()

        wx.StaticText(panel, label="From which date to which date would you like to download?", pos=(7, 5))

        self.from_date = wx.TextCtrl(panel, pos=(35, 45), value="yyyy-mm-dd")
        self.from_date.SetMaxLength(10)

        wx.StaticText(panel, label="To", pos=(155, 50))

        self.to_date = wx.TextCtrl(panel, pos=(180, 45), value="yyyy-mm-dd")
        self.to_date.SetMaxLength(10)

    def on_press(self, panel):
        value1 = self.from_date.GetValue()
        value2 = self.to_date.GetValue()
        username = os.getlogin()

        if not value1 or not value2:
            wx.MessageBox("ERROR (Required field empty)")
        else:

            limit = 10000000

            flowroute_dict = messages_controller.look_up_a_set_of_messages(value1, value2, limit)

            contact_list = """
            Mom
            Dad
            Sister
            Brother
            Boss
            Grandma
            """

            #contact numbers must match exactly to position of contact name. e.g. Mom pos 1 - phone number for mom pos 1
            contact_numbers = """
            18233356754
            18233356754
            18233356754
            18233356754
            18233356754
            18233356754
            """

            client_count = 0

            while client_count < limit:
                try:
                    flowroute_dict['data'][client_count]['client'] = ",Unknown"
                    client_count += 1
                except IndexError:
                    break

            mms_number = 0
            while mms_number < limit:
                try:
                    # ----------------------clean and split datetime---------------------
                    timestamp_full = flowroute_dict['data'][mms_number]['attributes']['timestamp']
                    timestamp_time_uncut = str(timestamp_full)[11:]
                    timestamp_time = timestamp_time_uncut[:8]
                    timestamp_date = str(timestamp_full)[:10]
                    del flowroute_dict['data'][mms_number]['attributes']['timestamp']
                    flowroute_dict['data'][mms_number]['attributes']['date'] = timestamp_date
                    flowroute_dict['data'][mms_number]['attributes']['time'] = timestamp_time

                    # ----------------------delete unwanted------------------------------
                    del flowroute_dict['data'][mms_number]['attributes']['amount_nanodollars']
                    del flowroute_dict['data'][mms_number]['attributes']['delivery_receipts']
                    del flowroute_dict['data'][mms_number]['attributes']['message_encoding']
                    del flowroute_dict['data'][mms_number]['id']
                    del flowroute_dict['data'][mms_number]['links']
                    del flowroute_dict['data'][mms_number]['type']

                    # ----------------------match numbers to names-----------------------
                    for run_contacts, run_number in zip(contact_list.split(), contact_numbers.split()):
                        if flowroute_dict['data'][mms_number]['attributes']['from'] == run_number or \
                                flowroute_dict['data'][mms_number]['attributes']['to'] == run_number:
                            flowroute_dict['data'][mms_number]['client'] = run_contacts

                    # --------------------------if mms-----------------------------------
                    data_is_mms = flowroute_dict['data'][mms_number]['attributes']['is_mms']
                    if str(data_is_mms) == "True":
                        del flowroute_dict['data'][mms_number]['relationships']

                    # -----------------------move body to end----------------------------
                    data = flowroute_dict['data'][mms_number]['attributes']['body']
                    flowroute_dict['data'][mms_number]['message_data'] = data
                    del flowroute_dict['data'][mms_number]['attributes']['body']

                    mms_number += 1
                except IndexError:
                    break

            flowroute_str = json.dumps(flowroute_dict)

            csv_del_quote = str(flowroute_str)

            csv_del_quote1 = csv_del_quote.replace('"', "")

            del_comma = csv_del_quote1.replace(",", "")
            del_amount = del_comma.replace("{attributes: {amount_display: $", "\n")
            del_data = del_amount.replace("{data: [", "")
            del_nanodollars = del_data.replace("amount_nanodollars:", ",")
            del_direction = del_nanodollars.replace("direction:", ",")
            del_from = del_direction.replace("from:", ",")
            del_status = del_from.replace("status:", ",")
            del_timestamp = del_status.replace("timestamp:", ",")
            del_to = del_timestamp.replace("to:", ",")
            del_links_brackets = del_to.replace("links: {}}", "")
            del_bracket = del_links_brackets.replace("}", "")
            del_message_data = del_bracket.replace("message_data:", ",")
            del_delivery_receipts = del_message_data.replace("delivery_receipts:", ",")
            del_is_mms = del_delivery_receipts.replace("is_mms:", ",")
            del_message_encoding = del_is_mms.replace("message_encoding:", ",")
            del_message_type = del_message_encoding.replace("message_type:", ",")
            del_message_data = del_message_type.replace("message_data:", ",")
            del_id = del_message_data.replace("id:", ",")
            del_links = del_id.replace("links:", ",")
            del_type = del_links.replace("type:", ",")
            del_bracket2 = del_type.replace("{", "")
            del_client = del_bracket2.replace("client:", ",")
            del_media = del_client.replace("media", ",")
            del_media_bracket = del_media.replace("media]", ",")
            del_relationships = del_media_bracket.replace("relationships:", ",,")
            del_date = del_relationships.replace("date:", ",")
            del_time = del_date.replace("time:", ",")

            mms_results = open('C:/Users/' + username + '/Desktop/'+ value2 + "sms_dataraw.csv",'w')
            mms_results.writelines("amount_display,direction,from,is_mms,"
                                   "message_type,status,to,date,time,client,message_data")
            mms_results.writelines(del_time)
            mms_results.close()
            wx.MessageBox("You can find the raw csv on your desktop")

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
