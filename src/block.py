from adguardhome import AdGuardHome

import asyncio
import json
import datetime
import logging

def config_logs(log_config):
    FORMAT='%(levelname)s|%(funcName)s: %(message)s [%(created)f]'
    logging.basicConfig(filename='example.log',
                        encoding='utf-8')
    print('completed')

def load_file(file_path):
    with open(file_path) as config_file:
        config = json.load(config_file)
        return config

config_logs(load_file('../resources/config/logs.json'))
logger = logging.getLogger();
async def set_blocked_services(services, adguard):
    response = await adguard.request(uri='blocked_services/set',
                          method='POST',
                          json_data=services)
    return response

async def set_blocked_websites(websites, adguard):
    response = await adguard.request(uri='filtering/set_rules',
                                     method='POST',
                                     json_data=websites)
    return response

async def main():
    '''Show example how to get status of your AdGuard Home instance.'''
    secrets = load_file('../resources/secrets/server_config.json')
    times = load_file('../resources/config/times.json')
    blocked_services = load_file('../resources/rules/blocked_services.json')
    blocked_websites = load_file('../resources/rules/blocked_websites.json')
    log_config = load_file('../resources/config/logs.json')
    config_logs(log_config)
    logger.debug("debug")
    async with AdGuardHome(host=secrets['host'],
                           port=secrets['port'],
                           username=secrets['username'],
                           password=secrets['password']) as adguard:
        hour = datetime.datetime.now().hour
        if times['lock_hour'] == hour:
            print('Blocking services and websites')
            await set_blocked_services(blocked_services, adguard)
            await set_blocked_websites(blocked_websites, adguard)
        elif times['unlock_hour'] == hour:
            print('Unblocking services and websites')
            await set_blocked_services([], adguard)
            await set_blocked_websites({}, adguard)
        else:
            print('Time to get a new watch')

if __name__ == "__main__":
    asyncio.run(main())
