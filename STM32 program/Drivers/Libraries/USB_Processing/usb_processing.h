/************************************************************************
Title:	  USB receive processing

Author:   Brich Ivan
File:     usb_processing.h
Software: STM32Fxxx_HAL_Driver, CMSIS-CORE
Hardware: STM32Fxxx, Motor
Created on: June 3, 2023

*/

#ifndef USB_PROCESSING_H_
#define USB_PROCESSING_H_

#include "stm32f1xx.h"
#include "string.h"

#define ERRORS_MAX		3

typedef struct {
	uint8_t flag;
	uint8_t buffer [6];
	int32_t data;
	uint32_t crc;
	uint8_t error_cnt;
	uint8_t error_flag;
} USBRx_TypeDef;

void USB_Restart_GPIO (void);
void USB_Frame_Receive (USBRx_TypeDef *USBRx, uint8_t* Buf, uint32_t *Len);
HAL_StatusTypeDef USB_Frame_Processing (USBRx_TypeDef *USBRx, CRC_HandleTypeDef *hcrc);

#endif /* USB_PROCESSING_H_ */
