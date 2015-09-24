LCIficontent-Cordova
====================

Client side part of LCI demo application

### Plugins that are used in this demo application are:

- com.danielcwilson.plugins.googleanalytics 0.6.0 "Google Universal Analytics Plugin"
- com.phonegap.plugins.PushPlugin 2.2.1 "PushPlugin"
- org.apache.cordova.device 0.2.10 "Device"
- org.apache.cordova.geolocation 0.3.8 "Geolocation"
- org.apache.cordova.inappbrowser 0.5.1 "InAppBrowser"
- org.apache.cordova.splashscreen 0.3.2 "Splashscreen"
- org.apache.cordova.wifiinfo 0.1.1 "Wifi Network Information"

Application is using Leaflet open-source JavaScript library for mobile-friendly interactive maps.
When the application starts markers are placed on the map and they represent recommendation POI's for user device.

Popup, which is part of Leaflet marker, contains POI information such as:
- website,
- image,
- working hours,
- etc.

Side menu of the application is populated by categories received from cloud server.

When user selects a category, application sends user data and category id to the server by using ajax call. Server will respond with POI data for selected category in JSON format. 
If new selection is made, the application removes all POI's from map and adds new POI based on the server response. 

Application has a splash screen which describes application usage.

Application periodically collects and sends user data to cloud server. Data gathering is performed in the background process. Collectected data is used for activity recognition.

The following data is being collected:
- wifi networks which are in user's range
- location data (latitude, longitude, altitude, accuracy and speed)

User data is sent to server every 30 seconds.

