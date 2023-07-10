# AutoGuardHome
Personal Setup for periodically rotating AdGuardHome rules for blocking and unblocking websites and services (i.e. Twitter)

Especially useful for restricting access to services during the work/school day

Setup:

1. Clone the respository onto yuour machine
2. Alter the following configuration files:
    1.  times.json: Set the hours between which domains will be blocked
    2.  blocked_services.json: Set the specific services to be blocked (leave as empty list if no services are to be blocked)
    3.  blocked_websites.json: Set the specific websites to be blocked (leave as empty dictionary if no websites are to be blocked)
    4.  logger_config.json: Customize the behavior of the main logger
3. Use crontab or another job scheduler to trigger the program in sync with the specified times in times.json
4. Be productive!
