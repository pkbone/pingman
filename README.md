PingMan
=======


---------

######DESCRIPTION


Network managers tried to seek a perfect network tool to understand the performance and the status of the nodes/routers/switches/firewalls, however, many tools on the market are not perfect. Some tiny ping tools can provide packet loss rate and response, but they can not applied to be deployed to multiple locations and running long term; Some SAAS vendors offer great application to monitor nodes but there is no simple solution to deal with internal routers and servers.  Many heavy node manager software are being packaged too many features and difficult to deploy. Some smart users adopt splunk with scripts and searches, but it is difficult to build a fully functional application to monitor the real infrastructure.

The PingMan is not a "Cool" idea to revolution something, it is just to manage to solve the actual issue. It takes the advantage of newly released Splunk AppFramework and Modular Inputs technique. This App is easily to be extended for more active test such as Web/HTTP, Email/SMTP and etc. 

PingMan includes

1. Ping Modular inputs

   Forget about scripts, now the ping target can be easily added through Splunk inputs UI.
   
2. Monitor Dashboard 

   Built with App Framework, the Host Monitor provide whole picture of everything you need to know about the availability status of the monitored targets.
   There is an expandable table inspired by splunk sample to quickly display recent history of any node without leave the main dashboard.
   
3. Host Detail 

   Detail Reports shows responsiveness and performance for any length of time period.
   
4. Alerts

   Not only alerts triggered by ping loss, but the recovery will be triggered either, so it could be easy to integrate to email/Network Management software/Ticket system to trigger the alert start and the end. The alert detail can be checked through host detail report too.

Pingman uses no third party db or any local persistent file beside Splunk API/App Framework facility, so it is a very light and easy to deploy app.



How to install?

Please download and start splunk-appframework first. (http://github.com/splunk/splunk-appframework) 

clone the repository file into etc/apps/

restart the splunk appframework (splunkdj) and splunk and rock it with web browser.

License: Open Source with BSD 3 clause. 


######Limitation:

The App only works on Linux/MacOS, it currently will not work with Splunk on Windows.    


##### Special Thanks

Splunk AppFramework is great.   Just hope more icons in the customized bootstrap css.





