/************************************************************************
Title:	  MG90S Servo controller implementation

Author:   Brich Ivan
File:     servo_control.h
Software: STM32Fxxx_HAL_Driver, CMSIS-CORE
Hardware: STM32Fxxx, Servo MG90S (Tower Pro)
Created on: June 3, 2023

*/

#ifndef SERVO_CONTROLLER_H_
#define SERVO_CONTROLLER_H_

#include "stm32f1xx_hal.h"

#define SERVO_ANGLE_MAX		90.0
#define INT16_MAX_VALUE		32767.0

#define SERVO_PWM_MAX			6000	// PWM counts for 90 deg
#define SERVO_PWM_MID 		4500	// PWM counts for 0 deg
#define SERVO_PWM_MIN			3000	// PWM counts for -90 deg

enum State_Enum {
	STANDBY					= 0,
	CONTROL_LOOP		= 2,
	ERROR_HOLD			= 3
};


void Angle_Decode (int32_t* angle_PWM, int32_t* data);

#endif /* SERVO_CONTROLLER_H_ */
