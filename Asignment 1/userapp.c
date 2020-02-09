#include <fcntl.h>
#include <unistd.h>
#include<sys/ioctl.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>

#define WR_VALUE _IOW('a','a',int32_t*)
#define WR_VALUE2 _IOW('a','b',int32_t*)

int main()
{

int file;
int32_t num;
int32_t num2;
char buffer[16];
buffer[16]='\0';
       

printf("\nHI : 'Driver being opened'\n");
file = open("/dev/adc8", O_RDWR);



if(file < 0)
 {
 printf(" Device file can't be opened\n");
 return 0;
 }


printf("Enter the channel:\n");
scanf("%d",&num);
while(num>=8)
{
printf("\nInvalid channel entered for 8 channel ADC");
printf("\nEnter valid channel(0-7):");
scanf("%d",&num);
}
ioctl(file, WR_VALUE, num);
         

printf("\nEnter 0:To store result in higher 10 bits");
printf("\nEnter 1:To store result in lower 10 bits");
printf("\nEnter the bit placement preference:\n");
scanf("%d",&num2);
ioctl(file, WR_VALUE2,num2);
 
   
read(file, buffer, sizeof(buffer));
printf("\nADC OUTPUT = %s",buffer);
     
     

printf("\nBYE :'Closing Driver'\n");
close(file);
}
