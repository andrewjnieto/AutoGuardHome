from adguardhome import AdGuardHome

import asyncio
import json

def load_secrets():
    with open("../resources/secrets/server_config.json") as config_file:
        secrets = json.load(config_file)
        return secrets
    
async def main():
    """Show example how to get status of your AdGuard Home instance."""
    secrets = load_secrets()
    async with AdGuardHome(host=secrets['host'],
                           port=secrets['port'],
                           username=secrets['username'],
                           password=secrets['password']) as adguard:
        version = await adguard.version()
        print("AdGuard version:", version)

        active = await adguard.protection_enabled()
        active = "Yes" if active else "No"
        print("Protection enabled?", active)

        if not active:
            print("AdGuard Home protection disabled. Enabling...")
            await adguard.enable_protection()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
