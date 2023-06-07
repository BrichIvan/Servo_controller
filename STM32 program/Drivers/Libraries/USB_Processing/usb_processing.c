/************************************************************************
Title:	  USB receive processing

Author:   Brich Ivan
File:     usb_processing.c
Software: STM32Fxxx_HAL_Driver, CMSIS-CORE
Hardware: STM32Fxxx
Created on: June 3, 2023

*/

#include "usb_processing.h"

void USB_Restart_GPIO (void) {
	// USB reconnection in case of reset
	// Toggle USB DP (D+) to GND for USB reconnection
	GPIO_InitTypeDef GPIO_InitStruct = {0};

	// Init DP as output
	GPIO_InitStruct.Pin = GPIO_PIN_12;
	GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
	HAL_GPIO_WritePin(GPIOA, GPIO_PIN_12, GPIO_PIN_RESET); // GND
	HAL_Delay (10);

	// Reinit pin for USB
	GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
	HAL_Delay (10);
}

void USB_Frame_Receive (USBRx_TypeDef *USBRx, uint8_t* Buf, uint32_t *Len) {
	USBRx->flag = 1;		// Message received

	memset (USBRx->buffer, '\0', sizeof (USBRx->buffer));	// Clear the main data buffer
	memcpy (USBRx->buffer, Buf, (uint8_t) *Len);			// Copy data buffer
	memset (Buf, '\0', (uint8_t) *Len);						// Clear the USB Rx buffer

}

HAL_StatusTypeDef USB_Frame_Processing (USBRx_TypeDef *USBRx, CRC_HandleTypeDef *hcrc) {
	HAL_StatusTypeDef status = HAL_OK;
	USBRx->data = (int32_t) ((int16_t) (USBRx->buffer [0] << 8) | USBRx->buffer [1]);
	USBRx->crc = (USBRx->buffer [2] << 24) | (USBRx->buffer [3] << 16) | (USBRx->buffer [4] << 8) | USBRx->buffer [5];

	uint32_t CRC_calc = HAL_CRC_Calculate(hcrc, (uint32_t *) &(USBRx->data), 1);

	if (CRC_calc != USBRx->crc) {
		status = HAL_ERROR;
	}

	return status;
}
