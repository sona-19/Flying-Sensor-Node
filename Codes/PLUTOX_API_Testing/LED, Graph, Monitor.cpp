#include "PlutoPilot.h"
#include "led.h"
#include "control.h"
#include "althold.h"
#include "Sensor.h"
#include "print.h"



//The setup function is called once at Pluto's hardware startup
void plutoInit()
{
// Add your hardware initialization code here
}



//The function is called once before plutoFly when you activate UserCode
void onPilotStart()
{
  // do your one time stuffs here

	Control.disableFlightStatus(true);
	ledOp(L_MID, OFF);

}



// The loop function is called in an endless loop
void plutoPilot()
{

//Add your repeated code here

	if(Althold.getVelocityZ() > 0){

			ledOp(L_LEFT, ON);//green led
			ledOp(L_RIGHT, OFF);//red led
			//Print.monitor("Velocity Z:", Althold.getVelocityZ());

	}else{
			ledOp(L_LEFT, OFF);
			ledOp(L_RIGHT, ON);
		}



		Print.monitor("Temperature", Barometer.getTemperature());
		Print.redGraph(Althold.getEstimatedAltitude());


}



//The function is called once after plutoFly when you deactivate UserCode
void onPilotFinish()
{

	 // do your cleanup stuffs here

	 Control.disableFlightStatus(false);

}
