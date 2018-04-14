#include "scales.h"
#include "main.h"
#include "stm32f3xx_hal.h"
#include "stm32f3xx.h"
#include "stm32f3xx_it.h"



Scale harmSubharm = {
   .grid = harmSubharmGrid,
   .t2Bitshift = 8,
   .oneVoltOct = 1};

Scale harmSubharmfullspan = {
   .grid = harmSubharmfullspanGrid,
   .t2Bitshift = 8,
   .oneVoltOct = 0};

Scale modal5primefullspan = {
   .grid = modal5primefullspanGrid,
   .t2Bitshift = 8,
   .oneVoltOct = 0};

Scale harmFolded4 = {
   .grid = harmFolded4Grid,
   .t2Bitshift = 9,
   .oneVoltOct = 1};

Scale polyResets = {
   .grid = polyResetsGrid,
   .t2Bitshift = 7,
   .oneVoltOct = 0};

Scale pentamodal5prime = {
   .grid = pentamodal5primeGrid,
   .t2Bitshift = 8,
   .oneVoltOct = 1};

void initializeScales() {
   scaleGroup[0] = harmSubharm;
   scaleGroup[1] = harmSubharmfullspan;
   scaleGroup[2] = modal5primefullspan;
   scaleGroup[3] = harmFolded4;
   scaleGroup[4] = polyResets;
   scaleGroup[5] = pentamodal5prime;
   scaleGroup[6] = harmSubharm;
   scaleGroup[7] = harmSubharmfullspan;
   scaleGroup[8] = modal5primefullspan;
   scaleGroup[9] = harmFolded4;
   scaleGroup[10] = polyResets;
   scaleGroup[11] = pentamodal5prime;
   scaleGroup[12] = harmSubharm;
   scaleGroup[13] = harmSubharmfullspan;
   scaleGroup[14] = modal5primefullspan;
   scaleGroup[15] = harmFolded4;
}
