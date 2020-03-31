#include<linux/kernel.h>
#include<linux/module.h>
#include<linux/usb.h>
#include<linux/slab.h>

#define SANDISK_VID   0x0781
#define SANDISK_PID   0x5567

#define JETFLASH_VID  0x8564
#define JETFLASH_PID  0x1000

#define USB_ENDPOINT_IN               0x80
#define BOMS_RESET                    0xFF
#define BOMS_RESET_REQ_TYPE           0x21
#define BOMS_GET_MAX_LUN              0xFE
#define BOMS_GET_MAX_LUN_REQ_TYPE     0xA1
#define READ_CAPACITY_LENGTH	      0x08
#define REQUEST_DATA_LENGTH           0x12
#define be_to_int32(buf) (((buf)[0]<<24)|((buf)[1]<<16)|((buf)[2]<<8)|(buf)[3])


// Command Block Wrapper (CBW)
struct command_block_wrapper {
uint8_t dCBWSignature[4];
uint32_t dCBWTag;
uint32_t dCBWDataTransferLength;
uint8_t bmCBWFlags;
uint8_t bCBWLUN;
uint8_t bCBWCBLength;
uint8_t CBWCB[16];
};



// Command Status Wrapper (CSW)
struct command_status_wrapper {
uint8_t dCSWSignature[4];
uint32_t dCSWTag;
uint32_t dCSWDataResidue;
uint8_t bCSWStatus;
};



static uint8_t cdb_length[256] = {
// 0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F
06,06,06,06,06,06,06,06,06,06,06,06,06,06,06,06,  //  0
06,06,06,06,06,06,06,06,06,06,06,06,06,06,06,06,  //  1
10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,  //  2
10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,  //  3
10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,  //  4
10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,  //  5
00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,  //  6
00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,  //  7
16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,  //  8
16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,  //  9
12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,  //  A
12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,  //  B
00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,  //  C
00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,  //  D
00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,  //  E
00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,  //  F
};

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

struct usbdev_private
{
struct usb_device *udev;
unsigned char class;
unsigned char subclass;
unsigned char protocol;
unsigned char ep_in;
unsigned char ep_out;
};

struct usbdev_private *p_usbdev_info;




//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


//disconnect
static void pen_disconnect(struct usb_interface *interface)
{
printk(KERN_INFO "USB device has been removed\n");
return ;
}


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//usb_device_id
static struct usb_device_id pen_table[] = {
    { USB_DEVICE(SANDISK_VID,SANDISK_PID) },
    { USB_DEVICE(JETFLASH_VID,JETFLASH_PID) },
    {} /*Terminating entry*/
};

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
static int get_mass_storage_status(struct usb_device *udev, uint8_t endpoint, uint32_t expected_tag)
{ 
struct command_status_wrapper *csw=kmalloc(sizeof(struct command_status_wrapper),GFP_KERNEL);
int r,size;
r=usb_bulk_msg(udev,usb_rcvbulkpipe(udev,endpoint),(void *)csw,13, &size, 1000);

if(r<0)
printk("Error occured in status");


if (size != 13) 
{
printk("   get_mass_storage_status: received %d bytes (expected 13)\n", size);
return -1;
}
	
}


////////////////////////////////////////////////////////////////////////////////////////////////////////
static int send_mass_storage_command(struct usb_device *udev, uint8_t endpoint, uint8_t lun,uint8_t *cdb, uint8_t direction, int data_length, uint32_t *ret_tag)
{
struct command_block_wrapper *cbw=kmalloc(sizeof(struct command_block_wrapper),GFP_KERNEL);

static uint32_t tag = 1;
int i=0, r,size;
uint8_t cdb_len;


cdb_len = cdb_length[cdb[0]];
memset(cbw, 0, sizeof(*cbw));
cbw->dCBWSignature[0] = 'U';
cbw->dCBWSignature[1] = 'S';
cbw->dCBWSignature[2] = 'B';
cbw->dCBWSignature[3] = 'C';
*ret_tag = tag;
cbw->dCBWTag = tag++;
cbw->dCBWDataTransferLength = data_length;
cbw->bmCBWFlags = direction;
cbw->bCBWLUN = lun;
cbw->bCBWCBLength = cdb_len;
memcpy(cbw->CBWCB, cdb, cdb_len);


//transfer length must be 31 bytes
r = usb_bulk_msg(udev,usb_sndbulkpipe(udev,endpoint),(void*)cbw,31, &size,1000);
if (r <0) 
		{
			printk(KERN_INFO "ERROR");
			return -1;
		}
		

printk("sent %d CDB bytes\n", cdb_len);

return 0;
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

static int test_mass_storage(struct usb_device *udev, uint8_t endpoint_in, uint8_t endpoint_out)
{
int r,size;
uint8_t lun=0;
uint32_t i, max_lba, block_size;
long device_size;
uint8_t cdb[16]; // SCSI Command Descriptor Block
uint8_t *buffer=kmalloc(sizeof(uint8_t),GFP_KERNEL);
uint32_t expected_tag;



memset(buffer, 0, sizeof(buffer));
memset(cdb, 0, sizeof(cdb));
cdb[0] = 0x25; // Read Capacity


printk(KERN_INFO "Resetting USB device");
r= usb_control_msg(udev,usb_sndctrlpipe(udev,0),BOMS_RESET,BOMS_RESET_REQ_TYPE,0,0,NULL,0,1000);
if(r<0)
printk("Reset failed with error :%d",r);
else
printk("Reset done successfully");

//Reading Capacity
send_mass_storage_command(udev,endpoint_out,lun,cdb,USB_ENDPOINT_IN,READ_CAPACITY_LENGTH,&expected_tag);

        usb_bulk_msg(udev,usb_rcvbulkpipe(udev,endpoint_in),(void*)buffer,READ_CAPACITY_LENGTH ,&size, 1000);
        printk("received %d bytes\n", size);
        printk("&buffer[0]: %d",buffer[0]);
	printk("&buffer[4]: %x",&buffer[4]);
        max_lba = be_to_int32(&buffer[0]);
        block_size = be_to_int32(&buffer[4]);
        device_size = ((long)(max_lba+1))*block_size/(1024*1024*1024);
        printk("max_lba: %x",max_lba);
        printk("Attached USB size is %ld GB\n", device_size);
        get_mass_storage_status(udev, endpoint_in, expected_tag);
       return 0;
}



//////////////////////////////////////////////////////////////////////////////////////////////////////////



//probe function
static int pen_probe(struct usb_interface *interface, const struct usb_device_id *id)
{
int i;
unsigned char epAddr,epAttr;
uint8_t endpoint_in = 0, endpoint_out = 0;	// default IN and OUT endpoints
struct usb_device *udev=interface_to_usbdev(interface);
struct usb_endpoint_descriptor *endpoint;



   
if(id->idProduct == SANDISK_PID  && id->idVendor == SANDISK_VID)
{
printk(KERN_INFO "Known USB Drive detected\n");
}

if(id->idProduct == JETFLASH_PID  && id->idVendor == JETFLASH_VID)
{
printk(KERN_INFO "Known USB Drive detected\n");
}

  
printk(KERN_INFO "No. of Altsettings =%d\n",interface->num_altsetting);
printk(KERN_INFO "No. of Endpoints =%d\n",interface->cur_altsetting->desc.bNumEndpoints);

for(i=0;i<interface->cur_altsetting->desc.bNumEndpoints;i++)
{
endpoint=&interface->cur_altsetting->endpoint[i].desc;
epAddr=endpoint->bEndpointAddress;
epAttr=endpoint->bmAttributes;
printk(KERN_INFO "ED[%d]->bmAttributes:0x%02X\n",i,epAttr);
printk(KERN_INFO "ED[%d]->bEndpointAddress:0x%02X\n",i,epAddr);


if((epAttr & USB_ENDPOINT_XFERTYPE_MASK)==USB_ENDPOINT_XFER_BULK)
{
if(epAddr & 0x80)
{
printk(KERN_INFO "EP %d is BULK IN\n",i);
endpoint_in = endpoint->bEndpointAddress;
printk(KERN_INFO "EP %d is BULK IN with address: 0x%02X\n",i,endpoint_in);
}
else
{
printk(KERN_INFO "EP %d is BULK OUT\n",i);
endpoint_out = endpoint->bEndpointAddress;
printk(KERN_INFO "EP %d is BULK OUT with address: 0x%02X\n",i,endpoint_out);
}
}
}


printk(KERN_INFO "VID=%04X:PID=%04X\n",id->idVendor, id->idProduct);
printk(KERN_INFO "USB DEVICE CLASS: %X\n",interface->cur_altsetting->desc.bInterfaceClass);
printk(KERN_INFO "USB DEVICE SUBCLASS: %X\n",interface->cur_altsetting->desc.bInterfaceSubClass);
printk(KERN_INFO "USB DEVICE PROTOCOL: %X\n",interface->cur_altsetting->desc.bInterfaceProtocol);
test_mass_storage(udev,endpoint_in, endpoint_out);
        return 0;
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

//usb driver
static struct usb_driver pen_driver =
{
    .name = "usbdev",
    .id_table = pen_table,
    .probe = pen_probe,
    .disconnect = pen_disconnect,
};


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

static int __init pen_init(void)
{

usb_register(&pen_driver);
printk(KERN_INFO "UAS READ Capacity Driver Inserted\n");
return 0;
  
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
static void __exit pen_exit(void)
{

usb_deregister(&pen_driver);
printk(KERN_INFO "\t BYE");
return ;

}

module_init(pen_init);
module_exit(pen_exit);

MODULE_LICENSE("GPL");
