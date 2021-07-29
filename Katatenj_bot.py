import requests
import json

url = "https://api.telegram.org/bot1905108544:AAH0RyBVX7oSyGL3iybb2MumB47JN0L8moE/"
url_silver = "https://www.mafiaonline.ru/api/api.php?action=info&param=MrSilver&i=yes"

keyboard_default = json.dumps({'remove_keyboard': True })

users = []
Silver_info = "\u0421\u043f\u0438\u0441\u043e\u043a \u0442\u0430\u0449\u0435\u0440\u043e\u0432:\n1. OverGod \n2._IMPERATOP_\n3. bertozim\n4. Goddess\n5. Katatenj\n\n\u041f\u0440\u0435\u0442\u0435\u043d\u0434\u0435\u043d\u0442\u044b \u043d\u0430 \u0442\u0430\u0449\u0435\u0440\u043e\u0432:\n- \u0422\u0435\u043c\u043d\u044b\u0439\n- Kar98k\n- 1rina0kar5";


def get_updates_json(request, offset_id='None'):  
    params = {'timeout': 30, 'offset': offset_id, 'allowed_updates': json.dumps(["message"])}
    response = requests.get(request + 'getUpdates', data=params)
    return response.json()

def get_update_results(request):
    result_data = get_updates_json(request)['result']
    if not result_data:
        return 0
    else:
        return result_data

def send_mess(chat, text, reply_markup=keyboard_default, parse_mode='None'):  
    params = {'chat_id': chat, 'text': text, 'parse_mode': parse_mode, 'reply_markup': reply_markup}
    response = requests.post(url + 'sendMessage', data=params)
    return response.json()

def send_mess_nokeyboard(chat, text, parse_mode='None'):  
    params = {'chat_id': chat, 'text': text, 'parse_mode': parse_mode}
    response = requests.post(url + 'sendMessage', data=params)
    return response.json()

def forward_mess(chat_id, from_chat_id, message_id):
    params = {'chat_id': chat_id, 'from_chat_id': from_chat_id, 'message_id': message_id}
    response = requests.post(url + 'forwardMessage', data=params)
    return response

def bot_messages(request):
    global users, Silver_info
    results = get_update_results(request)
    if results!=0:
        k = 0
        while k<len(results):
            first_result = results[k]
            person_id = first_result['message']['from']['id']
            if 'text' in first_result['message'].keys():
                if first_result['message']['text']=='/start':
                    flag = 0;
                    for i in users:
                        if i==person_id:
                            flag = 1;
                    if flag==0:
                        users.append(person_id);
                        text = 'Текущая информация MrSilver:\n\n' + Silver_info
                        send_mess_nokeyboard(person_id, text, parse_mode='None')
            k = k+1
            if 'text' in first_result['message'].keys():
                try:
                    print(str(datetime.datetime.utcfromtimestamp(first_result['message']['date'])) + ' '
                          + first_result['message']['from']['first_name']+': '+first_result['message']['text'] + ' ' + str(int(time.time())-first_result['message']['date'])) 
                except UnicodeEncodeError:
                    print(str(datetime.datetime.utcfromtimestamp(first_result['message']['date'])) + ' '
                          + first_result['message']['from']['first_name']+': '+'Unsupported text (smile)')
            else:
                print(str(datetime.datetime.utcfromtimestamp(first_result['message']['date'])) + ' '
                      + first_result['message']['from']['first_name']+': '+'No text')
        get_updates_json(request, results[k-1]['update_id']+1)
    else:
        response = requests.get(url_silver)
        result = response.json()
        if len(users)>0:
            if result['info']!=Silver_info and result['info']!='':
                for i in users:
                    text = 'Изменения в информации MrSilver:\n\n' + result['info']
                    send_mess_nokeyboard(i, text, parse_mode='None')
                    Silver_info = result['info']

def main():
    aaa = 1
    while aaa == 1:
        bot_messages(url)
        
main()
