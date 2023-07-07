from adguardhome import AdGuardHome

import asyncio
import json
import datetime

def load_file(file_path):
    with open(file_path) as config_file:
        config = json.load(config_file)
        return config

async def unlock_services(adguard):
    response = await adguard.request(uri='blocked_services/set',
                          method='POST',
                          json_data=[])
    if response['message'] == '':
        print("Services successfully unlocked")
    else:
        print("Issue encountered unlocking services:", response['message'])

async def unlock_websites(adguard):
    response = await adguard.request(uri='filtering/set_rules',
                                     method='POST',
                                     json_data={})
    if response['message'] == '':
        print("Websites successfully unlocked")
    else:
        print("Issue encountered unlocking websites:", response['message'])

async def lock_services(blocked_services, adguard):
    response = await adguard.request(uri='blocked_services/set',
                                     method='POST',
                                     json_data=blocked_services)
    if response['message'] == '':
        print("Services successfully locked")
    else:
        print("Issue encountered locking services:", response['message'])

 
async def lock_websites(blocked_websites, adguard):
    response = await adguard.request(uri='filtering/set_rules',
                                     method='POST',
                                     json_data=blocked_websites)
    if response['message'] == '':
        print("Websites successfully locked")
    else:
        print("Issue encountered locking websites:", response['message'])

async def main():
    '''Show example how to get status of your AdGuard Home instance.'''
    secrets = load_file('../resources/secrets/server_config.json')
    times = load_file('../resources/config/times.json')
    blocked_services = load_file('../resources/rules/blocked_services.json')
    blocked_websites = load_file('../resources/rules/blocked_websites.json')
    async with AdGuardHome(host=secrets['host'],
                           port=secrets['port'],
                           username=secrets['username'],
                           password=secrets['password']) as adguard:
        hour = datetime.datetime.now().hour
        if times['lock_hour'] == hour:
            await lock_services(blocked_services, adguard)
            await lock_websites(blocked_websites, adguard)
        elif times['unlock_hour'] == hour:
            await unlock_services(adguard)
            await unlock_websites(adguard)
        else:
            print('time to get a new watch')
        print('It is now:', hour)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
