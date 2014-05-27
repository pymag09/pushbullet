pushbullet is python3 library to work with pushbullet service
Call of any function returns a tuple with 3 elements
    code of the HTTP request
    URL or Error of the HTTP request
    the HTTP response

The Library consist of 5 classes. Each has its own functionality
    PBPushes
    PBFileUpload
    PBUsers
    PBContacts
    PBDevices

Installation:
-------------------------------------
# git clone git@github.com:pymag09/pushbullet.git
# python3 setup.py install

Using examples:
-------------------------------------
'''import pushbullet

#Create the push instance
my_push = pushbullet.PBPushes(your_API_Key)
my_push.pushes(device_iden=(device_iden), type='note', title='my_title', body='note_body')
my_push.pushes(device_iden=(device_iden), type='link', title='my_title', body='link body', url='http://google.com')
my_push.pushes(device_iden=(device_iden), type='address', name='Bob', address='Wall street 1')
my_push.pushes(device_iden=(device_iden), type='list', title='my title', items=['one','two','three'])

#Uploading files is more complicated.
#First. create upload object
    my_upload = pushbullet.PBFileUpload(your_API_Key)
#Than. Send upload request
#Object PBFileUpload has "file_upload_param" attribute. When the request was successfully executed, file properties are stored in this variable
    my_upload.upload_request(your_file_name)

#Upload file
    print(my_upload.pb_upload(path_to_your_file))
#Send push with file URL
    print(my_push.pushes(device_iden=(device_iden),
    type='file',
    file_name=my_upload.file_upload_param['file_name'],
    file_type=my_upload.file_upload_param['file_type'],
    file_url=my_upload.file_upload_param['file_url'],
    body='look it'))
#Requesting push history
#Please remember. All functions return tuple with 3 elements.
    my_push.get_push_history()

#Deleting a push
    for p in my_push.get_push_history()[2]['pushes']:
        if p['active']:
            my_push.del_pushes(p['iden'])
            print(p)

#Getting the devices that can be pushed to:
    my_pb_dev = pushbullet.PBDevices(your_API_Key)
    my_pb_dev = my_pb_dev.get_connected_devices()

#Please remember. All functions return tuple with 3 elements. That`s why my_pb_dev[2]
    for device in my_pb_dev[2]['devices']:
        if device['active']:
            print('%s - %s' % (device['model'], device['iden']))

#Deleting a device
#use previouse example to get iden of device
    my_pb_dev.del_connected_device(device_iden):

#Getting your contacts
    my_cont = pushbullet.PBContacts(your_API_Key)

#Please remember. All functions return tuple with 3 elements.
    print(my_cont.get_contacts())

#Deleting a contact
    my_cont.del_contact(contact_iden)

#Getting this user's information
    my_pb_me = pushbullet.PBUsers(your_API_Key)
    print(my_pb_me.get_me())
'''