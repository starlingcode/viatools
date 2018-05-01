#include "stm32f3xx_hal.h"
#include "stm32f3xx.h"
#include "stm32f3xx_it.h"



typedef struct {
	const uint32_t *aPattern;
	const uint32_t *bPattern;
	const uint32_t aLength;
	const uint32_t bLength;
} pattern;



static const uint32_t eucludean5_16[16] = {1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0}; 

static const uint32_t eucludean2_16[16] = {1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0}; 

static const uint32_t eucludean2_8[8] = {1, 0, 0, 0, 1, 0, 0, 0}; 

static const uint32_t eucludean3_16[16] = {1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0}; 

static const uint32_t eucludean5_8[8] = {1, 0, 1, 1, 0, 1, 1, 0}; 

static const uint32_t eucludean8_16[16] = {1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0}; 

static const uint32_t eucludean7_8[8] = {1, 1, 1, 1, 1, 1, 1, 0}; 

static const uint32_t eucludean7_16[16] = {1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0}; 

static const uint32_t eucludean4_8[8] = {1, 0, 1, 0, 1, 0, 1, 0}; 

static const uint32_t eucludean4_16[16] = {1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0}; 

static const uint32_t eucludean8_8[8] = {1, 1, 1, 1, 1, 1, 1, 1}; 

static const uint32_t eucludean3_8[8] = {1, 0, 0, 1, 0, 0, 1, 0}; 

static const uint32_t eucludean6_16[16] = {1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0}; 

static const uint32_t eucludean6_8[8] = {1, 1, 1, 0, 1, 1, 1, 0}; 

static const uint32_t eucludean1_8[8] = {1, 0, 0, 0, 0, 0, 0, 0}; 

static const uint32_t eucludean1_16[16] = {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}; 

