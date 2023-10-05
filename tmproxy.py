from time import sleep
from requests import session
from urllib3 import disable_warnings , exceptions
disable_warnings(exceptions.InsecureRequestWarning)

# api_key : tmproxy api key
# same_ip: get new proxy or reuse current proxy
# time_change: get new proxy after
# type_proxy: http/socks5

def tmproxy(api_key,same_ip=False,time_change=10,type_proxy='https'):
    ss = session()
    ss.verify = False
    ss.trust_env = False
    def get_current_proxy():
        api = f'https://tmproxy.com/api/proxy/get-current-proxy'
        playload = {"api_key":api_key}
        response = ss.post(url=api , json=playload).json()
        if response['code'] != 0:
            print(f'{api_key} => ERROR: {response}')
            return 'error api key' , 0
        else:
            data = response['data']
            ip_allow = data['ip_allow']
            location = data['location_name']
            socks5 = data['socks5']
            https = data['https']
            time_out = data['timeout']
            next_request = data['next_request']
            expired_at = data['expired_at']
            full_information = f'IP ALLOW: {ip_allow}|LOCATION: {location}|SOCKS5: {socks5}|HTTP: {https}|TIME OUT: {time_out}|NEXT_REQUESTS: {next_request}|EXPIRED AT: {expired_at}'
            print(f'{api_key} => FULL INFOR => {full_information}')
            if type_proxy == 'https':
                return https , next_request
            elif type_proxy == 'socks5':
                return socks5 , next_request
            else:
                print('{api_key} => ERROR TYPE PROXY - ONLY ACCEPT HTTP/SOCKS => [error: {type_proxy}]')
                return 'error_type_proxy' , 0
    
    def get_new_proxy():
        api = f'https://tmproxy.com/api/proxy/get-new-proxy'
        # 0 => random
        playload = {"api_key":api_key,"sign":"string","id_location":0}
        response = ss.post(url=api , json=playload).json()
        data = response['data']
        ip_allow = data['ip_allow']
        location = data['location_name']
        socks5 = data['socks5']
        https = data['https']
        time_out = data['timeout']
        next_request = data['next_request']
        expired_at = data['expired_at']
        full_information = f'IP ALLOW: {ip_allow}|LOCATION: {location}|SOCKS5: {socks5}|HTTP: {https}|TIME OUT: {time_out}|NEXT_REQUESTS: {next_request}|EXPIRED AT: {expired_at}'
        print(f'{api_key} => FULL INFOR => {full_information}')
        if type_proxy == 'https':
            return https , next_request
        elif type_proxy == 'socks5':
            return socks5 , next_request
        else:
            print('{api_key} => ERROR TYPE PROXY - ONLY ACCEPT HTTP/SOCKS => [error: {type_proxy}]')
            return 'error_type_proxy'
        
        
    
    proxy , next_change = get_current_proxy()
    if proxy == 'error api key' or proxy == 'error_type_proxy':
        return 'error_check_api_key_again'
    else:
        # same ip: true => cho phép trùng ip => lấy proxy cũ khi chưa được đổi ip
        if same_ip == True:
            if next_change == 0:
                proxy , next_change = get_new_proxy()
                return proxy
            else:
                proxy, next_change = get_current_proxy()
                return proxy
        else:
            if next_change <= time_change:
                proxy , next_change = get_new_proxy()
                return proxy
            else:
                for x in range(next_change):
                    print(f'{api_key} => WAIT {next_change - x} FOR GET NEW PROXY',end='\r')
                    sleep(1)
                proxy , next_change = get_new_proxy()
                return proxy
    
    
    


if __name__ == '__main__':
    while True:
        api_key = '59c5ed17bee81e8ca9dfb1fe4b8931eb'
        proxy = tmproxy(api_key,same_ip=False)
        print(proxy)
        sleep(5)