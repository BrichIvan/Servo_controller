/************************************************************************
Title:	  MG90S Servo controller implementation

Author:   Brich Ivan
File:     servo_control.c
Software: STM32Fxxx_HAL_Driver, CMSIS-CORE
Hardware: STM32Fxxx, Servo MG90S (Tower Pro)
Created on: June 3, 2023

*/
#include "servo_control.h"
#include "math.h"

void Angle_Decode (int32_t* angle_PWM, int32_t* data) {
	// For testing
	// float angle = (float) *data * (SERVO_ANGLE_MAX/INT16_MAX_VALUE); // [deg]

	// angle to PWM transform
	float angle_tmp = (float) *data * (SERVO_PWM_MIN / (2*INT16_MAX_VALUE));
	*angle_PWM = (int32_t) roundf(angle_tmp) + SERVO_PWM_MID;

	// Servo protection
	if (*angle_PWM > SERVO_PWM_MAX) {
		*angle_PWM = SERVO_PWM_MAX;
	} else if (*angle_PWM < SERVO_PWM_MIN) {
		*angle_PWM = SERVO_PWM_MIN;
	}

}
