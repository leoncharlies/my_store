// #include "main.h"
// #include "openmv.h"
// #include "usart.h"
// #include "LED.h"
// #include "openmv.h"
// #include "stdio.h"

 
// uint8_t Number = 0;
 
// /* STM32接收端处理OpenMV传输的数据 */
// void OpenMV_Data_Receive(uint16_t OpenMV_Data)
// {
// 	/* 计数变量 */
// 	static uint8_t RxCounter=0;			//计数变量
// 	/* 数据接收数组 */
// 	static uint16_t RxBuffer[4]={0};
// 	/* 数据传输状态位 */
// 	static uint8_t RxState = 0;	
	
// 	/* 判断数据是否为有效数据，解码 */
// 	if(RxState == 0 && OpenMV_Data == 0xFE)				//0xFE帧头
// 	{
// 		RxState = 1;																//状态位改变
// 		RxBuffer[RxCounter++] = OpenMV_Data;				//将数据放入接收数组
// 	}
// 	else if(RxState == 1 && OpenMV_Data == 0xBC)	//0xBC帧头
// 	{
// 		RxState = 2;																//状态位改变
// 		RxBuffer[RxCounter++] = OpenMV_Data;				//将数据放入接收数组
// 	}
// 	else if(RxState == 2)													//读取目标数据（根据实际情况处理）
// 	{
// 		RxBuffer[RxCounter++] = OpenMV_Data;				//将数据放入接收数组
// 		if(RxCounter>=3||OpenMV_Data == 0xEF)
// 		{
// 			RxState = 3;															//状态位改变
// 			Number = RxBuffer[RxCounter-1];
			

// 		}
// 	}
// 	else if(RxState == 3)													//检测是否接收到标志位
// 	{
// 		if(RxBuffer[RxCounter-1] == 0xEF)
// 		{
// 			/* 计数和状态位归零 */
// 			RxCounter = 0;
// 			RxState = 0;
// 			for(int i = 0;i < 4; i++)
// 			{
// 				RxBuffer[i] = 0x00;
// 			}
// 		} 
// 		else 		//接收错误
// 		{
// 			/* 计数和状态位归零 */
// 			RxCounter = 0;
// 			RxState = 0;
// 			/* 清空存放数据的数组 */
// 			for(int i = 0;i < 4; i++)
// 			{
// 				RxBuffer[i] = 0x00;
// 			}
// 		}
// 	}
// 	else			//整体的接收异常
// 	{
// 		/* 计数和状态位归零 */
// 		RxCounter = 0;
// 		RxState = 0;
// 		/* 清空存放数据的数组 */
// 		for(int i = 0;i < 4; i++)
// 		{
// 			RxBuffer[i] = 0x00;
// 		}		
// 	}
// }