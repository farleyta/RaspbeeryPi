# RaspbeeryPi
Raspberry Pi-powered brains behind my home kegerator and bar.

This repo runs on a $10 Raspberry Pi Zero W, with [2 flow meters](https://www.adafruit.com/product/828) installed within the keg lines to measure how much beer flows for each pour. Each click is measured, and after 10 seconds of inactivity, a calculation is made, and details of the pour are logged to a PostgreSQL database and emitted to a [custom Apache Kafka stream](https://github.com/farleyta/BeerKafka) for future downstream processing.

Heavily influenced by https://github.com/adafruit/Kegomatic.

### Some fun ideas for future improvements:

- full writeup of hardware and software development process!
- a UI for registering new kegs, measuring how much is left in current keg, and viewing historic pour data
- a realtime alert system when a certain amount has been poured (eg, "You've used 90% of Keg #1, time to brew again!")
- a user service for allowing friends to register their own pours (fingerprint scanner? face detection?)
- a safety shutoff valve (requires installation of in-line solenoid)
