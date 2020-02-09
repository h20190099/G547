#include <linux/module.h>   
#include <linux/kernel.h>   
#include <linux/init.h>      
#include <linux/moduleparam.h>
#include <linux/version.h>
#include<linux/slab.h>                
#include<linux/uaccess.h>              
#include <linux/ioctl.h>
#include <linux/random.h>
#include <linux/types.h>
#include <linux/device.h>
#include <linux/kdev_t.h>
#include <linux/fs.h>  
#include <linux/cdev.h>
 

#define WR_VALUE _IOW('a','a',int32_t*)
#define WR_VALUE2 _IOW('a','b',int32_t*)

int p;
int m=0;
int n=0;
uint16_t rand; 
uint16_t rand_temp;

int32_t member,j=0;
int32_t member_a;

char buf_er1[16];
char buf_er[10];

static dev_t first;
static struct cdev c_dev;
static struct class *cls;
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

static long etx_ioctl(struct file *file, unsigned int cmd, unsigned long arg);
 
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
 
static int etx_open(struct inode *i,struct file *f)
{
printk(KERN_INFO "mychar:open()\n");
return 0;
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

static int etx_close(struct inode *i,struct file *f)
{
printk(KERN_INFO "mychar:close()\n");
return 0;
}

//////////////////////////////////////////////////////////////////////////////////10 bit random no. generation n converting it into binary
static ssize_t etx_read(struct file *f,char __user *buf,size_t len,loff_t *off)
{

get_random_bytes(&rand,2);
rand=(rand%1024);
rand_temp=rand;



if(rand<513)
{
rand+=512;
}


while(rand!=0)
{
buf_er[m]=(rand%2)+'0';
rand=rand/2;
m=m+1;
}


buf_er[m]='\0';

//////////////////////////////////////////////////////////////////////////////////////////////////////////bit placement preference

if(member_a==0)
{
                  for(n=10;n<16;n++)
                 {
                   buf_er1[n]='x';
                
                 }


                 for(n=0;n<10;n++)
                {
                   buf_er1[n]=buf_er[n];
               
                }

}



if(member_a==1)
{
                 for(p=0;p<6;p++)
                 {
                  buf_er1[p]='x';
                
                 }

                 for(p=6;p<16;p++)

                 {
                 buf_er1[p]=buf_er[p-6];
              
                 }

}


buf_er1[16]='\0';
printk("%d",rand_temp);
printk("%s",buf_er1);
printk(KERN_INFO "mychar: read()\n");


if(copy_to_user(buf,buf_er1,sizeof(buf_er1)));
return 0;
}
 

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

static long etx_ioctl(struct file *file, unsigned int cmd, unsigned long arg)
{
       
switch(cmd) {
                case WR_VALUE:member=arg;
                          
                         
                case WR_VALUE2:member_a=arg;
                               
             }
return 0;
}
 
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
static struct file_operations fops=
                                      {

                                       .owner=THIS_MODULE,
                                       .open=etx_open,
                                       .release=etx_close,
                                       .read=etx_read,
                                       .unlocked_ioctl = etx_ioctl
                                       

                                        };
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
 
static int __init mychar_init(void)
{
printk(KERN_INFO " mychar drive registered");

 //step 1
if(alloc_chrdev_region(&first,0,1,"bits-pilani")<0)
{
return -1;
}


//step 2
if((cls=class_create(THIS_MODULE, "chardrv"))==NULL)
{
unregister_chrdev_region(first,1);
return -1;
}
if(device_create(cls,NULL,first,NULL,"adc8")==NULL)
{
class_destroy(cls);
unregister_chrdev_region(first,1);
return -1;
}


//step3
cdev_init(&c_dev,&fops);
if(cdev_add(&c_dev,first,1)==-1)
{
device_destroy(cls,first);
class_destroy(cls);
unregister_chrdev_region(first,1);
return -1;
}
return 0;
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
static void __exit mychar_exit(void)

{
cdev_del(&c_dev);
device_destroy(cls,first);
class_destroy(cls);
unregister_chrdev_region(first,1);
printk(KERN_INFO "mychar unregistered\n\n");
}


module_init(mychar_init);
module_exit(mychar_exit);

 
MODULE_LICENSE("GPL");
MODULE_AUTHOR("SANJANA LAHANE");
MODULE_DESCRIPTION("ADC8 device driver");
MODULE_VERSION("1.5");