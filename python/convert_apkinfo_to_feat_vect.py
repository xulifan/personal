import os, sys, shutil
from os import listdir
from os.path import isfile, join


#
# python convert_apkinfo_to_feat_vect.py ./original_data_from_jose/malware 1
#

permission=['ACCESS_4G_STATE', 'ACCESS_ALL_DOWNLOADS', 'ACCESS_ASSISTED_GPS', 'ACCESS_BACKGROUND_SERVICE', 'ACCESS_BLUETOOTH_SHARE', 'ACCESS_BSCI_DRM', 'ACCESS_CACHE_FILESYSTEM', 'ACCESS_CELL_ID', 'ACCESS_CHECKIN_PROPERTIES', 'ACCESS_COARSE', 'ACCESS_COARSE_LOCATIO', 'ACCESS_COARSE_LOCATION', 'ACCESS_COARSE_UPDATES', 'ACCESS_CORSE_LOCATION', 'ACCESS_COURSE_LOCATION', 'ACCESS_DATA', 'ACCESS_DOWNLOAD_MANAGER', 'ACCESS_DOWNLOAD_MANAGER_ADVANCED', 'ACCESS_DRM', 'ACCESS_FINE_LOCATION', 'ACCESS_FINE_LOCATON', 'ACCESS_GPS', 'ACCESS_HIGH_LOCATION', 'ACCESS_KUGOU_SERVICE', 'ACCESS_LGDRM', 'ACCESS_LOCATION', 'ACCESS_LOCATION_EXTRA_COMMANDS', 'ACCESS_LOCATTON_MOCK_LOCATION', 'ACCESS_MATCH_CONTENT', 'ACCESS_MOCK_LOCATION', 'ACCESS_NETWORK_CHANGE', 'ACCESS_NETWORK_STATE', 'ACCESS_NETWORK_watson', 'ACCESS_PROVIDER', 'ACCESS_PUSHAGENT', 'ACCESS_SUPERUSER', 'ACCESS_SURFACE_FLINGER', 'ACCESS_WIFI_STATE', 'ACCESS_WIMAX_STATE', 'ACCES_MOCK_LOCATION', 'ACCOUNT_MANAGER', 'ACTION_CALL', 'ACTION_CALL_PRIVILEGED', 'ACTION_PHONE_STATE_CHANGED', 'ADD_ACCOUNTS', 'ADD_SYSTEM_SERVICE', 'ANSWER_PHONE', 'AOM_MESSAGE', 'APPWIDGET_LIST', 'AUDIO_SERVICE', 'AUTHENTICATE_ACCOUNTS', 'AUTH_APP', 'BACKUP', 'BAIDU_LOCATION_SERVICE', 'BATTERY_STATS', 'BILLING', 'BIND_ACCESSIBILITY_SERVICE', 'BIND_APPWIDGET', 'BIND_DEVICE_ADMIN', 'BIND_INPUT_METHOD', 'BIND_WALLPAPER', 'BLUETOOTH', 'BLUETOOTH_ADMIN', 'BOOT_COMPLETED', 'BRICK', 'BROADCAST', 'BROADCAST_PACKAGE_ADDED', 'BROADCAST_PACKAGE_REMOVED', 'BROADCAST_SMS', 'BROADCAST_STICKY', 'BROADCAST_WAP_PUSH', 'C2D_MESSAGE', 'CALL', 'CALL_PHONE', 'CALL_PRIVILEGED', 'CAMER', 'CAMERA', 'CAMERA_EXTENDED', 'CAN_REQUEST_ENHANCED_WEB_ACCESSIBILITY', 'CAN_REQUEST_TOUCH_EXPLORATION_MODE', 'CHANGE_4G_STATE', 'CHANGE_CHANGE_STATE', 'CHANGE_COMPONENT_ENABLED_STATE', 'CHANGE_CONFIGURATION', 'CHANGE_NETWORK_STATE', 'CHANGE_WIFI_AP_STATE', 'CHANGE_WIFI_MULTICAST_STATE', 'CHANGE_WIFI_STATE', 'CHANGE_WIMAX_STATE', 'CHECK_LICENSE', 'CLEAR_APP_CACHE', 'CLEAR_APP_USER_DATA', 'CONFIGURE_SIP', 'CONNECTIVITY_INTERNAL', 'CONTACT', 'CONTROL_LOCATION_UPDATES', 'DELETE_CACHE_FILES', 'DELETE_EXTERNAL_STORAGE', 'DELETE_PACKAGES', 'DEVICE_POWER', 'DIAGNOSTIC', 'DIAL', 'DISABLE_HDMI', 'DISABLE_KEYGUARD', 'DOWNLOAD_WITHOUT_NOTIFICATION', 'DUMP', 'EXPAND_STATUS_BAR', 'FACTORY_TEST', 'FINE_LOCATION', 'FLAG_ACTIVITY_NEW_TASK', 'FLAG_KEEP_SCREEN_ON', 'FLASHLIGHT', 'FORCE_BACK', 'FORCE_STOP_PACKAGES', 'FULLSCREEN', 'GET_ACCOUNTS', 'GET_LIMIT_STATUS', 'GET_PACKAGE_SIZE', 'GET_TASKS', 'GLOBAL_SEARCH', 'GLOBAL_SEARCH_CONTROL', 'HARDWARE_TEST', 'INJECT_EVENT', 'INJECT_EVENTS', 'INSTALL_DRM', 'INSTALL_LOCATION_PROVIDER', 'INSTALL_PACKAGES', 'INTERACT_ACROSS_USERS', 'INTERACT_ACROSS_USERS_FULL', 'INTERNAL_SYSTEM_WINDOW', 'INTERNET', 'KILL_BACKGROUND_PROCESSES', 'LINE_ACCESS', 'LISTEN_CELL_LOCATION', 'LISTEN_SIGNAL_STRENGTH', 'LISTEN_SIGNAL_STRENGTHS', 'LOCATION', 'MANAGE_ACCOUNTS', 'MANAGE_APP_TOKENS', 'MANAGE_USB', 'MANAGE_USERS', 'MAPS_RECEIVE', 'MASTER_CLEAR', 'MODE_WORLD_READABLE', 'MODE_WORLD_WRITEABLE', 'MODIFY_AUDIO_SETTINGS', 'MODIFY_PHONE_STATE', 'MOUNT_FORMAT_FILESYSTEMS', 'MOUNT_UNMOUNT_FILESYSTEMS', 'MOVE_PACKAGE', 'NETWORK', 'NFC', 'NO_SOFT_KEYS', 'PACKAGE_USAGE_STATS', 'PERMISSION_NAME', 'PERSISTENT_ACTIVITY', 'PERSONAL_MEDIA', 'PICK_CONTACT', 'PREVENT_POWER_KEY', 'PROCESS_CALL', 'PROCESS_INCOMING_CALLS', 'PROCESS_OUTGOING_CALLS', 'RAISED_THREAD_PRIORITY', 'READ_ATTACHMENT', 'READ_CALENDAR', 'READ_CALL_LOG', 'READ_CONTACTS', 'READ_DATA', 'READ_EXTERENAL_STORAGE', 'READ_EXTERNAL_STORAGE', 'READ_FRAME_BUFFER', 'READ_INPUT_STATE', 'READ_INTERNAL_STORAGE', 'READ_LOGS', 'READ_MMS', 'READ_OWNER_DATA', 'READ_PERMISSION', 'READ_PHONE_DATA', 'READ_PHONE_STAT', 'READ_PHONE_STATE', 'READ_PROFILE', 'READ_SECURE_SETTINGS', 'READ_SETTINGS', 'READ_SMS', 'READ_SOCIAL_STREAM', 'READ_SYNC_SETTINGS', 'READ_SYNC_STATS', 'READ_TASKS', 'READ_USER_DICTIONARY', 'REBOOT', 'RECEIVE', 'RECEIVE_ADM_MESSAGE', 'RECEIVE_BOOT_COMPLETED', 'RECEIVE_BOOT_PERMISSION', 'RECEIVE_DATA_MESSAGE', 'RECEIVE_MMS', 'RECEIVE_SMS', 'RECEIVE_USER_PRESENT', 'RECEIVE_WAP_PUSH', 'RECORDE_AUDIO', 'RECORD_AUDIO', 'RECORD_VIDEO', 'REENABLE_KEYGUARD', 'REORDER_TASKS', 'RESTART_PACKAGES', 'RESTRICTED', 'RUN_INSTRUMENTATION', 'SDCARD_WRITE', 'SEND', 'SEND_DATA_MESSAGE', 'SEND_DOWNLOAD_COMPLETED_INTENTS', 'SEND_SMS', 'SET_ACTIVITY_WATCHER', 'SET_ALARM', 'SET_ALWAYS_FINISH', 'SET_ANIMATION_SCALE', 'SET_DEBUG_APP', 'SET_ORIENTATION', 'SET_PREFERRED_APPLICATIONS', 'SET_PROCESS_FOREGROUND', 'SET_PROCESS_LIMIT', 'SET_TIME_ZONE', 'SET_WALLPAPER', 'SET_WALLPAPER_COMPONENT', 'SET_WALLPAPER_HINT', 'SET_WALLPAPER_HINTS', 'SIGNAL_PERSISTENT_PROCESSES', 'SIM_STATE_READY', 'SMARTCARD', 'SMS_RECEIVED', 'START_BACKGROUND_SERVICE', 'STATUS_BAR', 'STOP_APP_SWITCHES', 'STORAGE', 'SUBSCRIBED_FEEDS_READ', 'SUBSCRIBED_FEEDS_WRITE', 'SYSTEM_ALERT_WINDOW', 'SYSTEM_DIALOG_WINDOW', 'SYSTEM_ERROR_WINDOW', 'SYSTEM_OVERLAY_WINDOW', 'UPDATE_DEVICE_STATS', 'USES_POLICY_FORCE_LOCK', 'USE_CREDENTIALS', 'USE_SIP', 'VIBRATE', 'VIBRATION', 'WAKE_LOCK', 'WIFI_LOCK', 'WRITE', 'WRITE_APN_SETTINGS', 'WRITE_CALENDAR', 'WRITE_CALL_LOG', 'WRITE_CONTACTS', 'WRITE_EXTERNAL_STORAGE', 'WRITE_EXTERNAL_STOREAGE', 'WRITE_GSERVICES', 'WRITE_INTERNAL_STORAGE', 'WRITE_MEDIA_STORAGE', 'WRITE_MMS', 'WRITE_OWNER_DATA', 'WRITE_PROFILE', 'WRITE_SECURE', 'WRITE_SECURE_SETTINGS', 'WRITE_SETTINGS', 'WRITE_SMS', 'WRITE_SOCIAL_STREAM', 'WRITE_SYNC_SETTINGS', 'WRITE_SYNC_STATS', 'WRITE_TASKS', 'WRITE_USER_DICTIONARY', 'WRTIE_OWNER_DATA', 'YAHOO_INTER_APP', 'YNP_MESSAGE', 'accelerometer']


permission_all=[]

n_feat=len(permission)

input=sys.argv[1]
input=input.rstrip('/')
label=sys.argv[2]
if label.isdigit() == False:
    print 'The label has to be digit\n'
    sys.exit()
f_output=open('output.permission','w')

for dirs in listdir(input):
    #print dirs
    apk_dir=input+'/'+dirs
    if os.path.isdir(apk_dir):
        files=listdir(apk_dir)
        strace_filename=''
        apkinfo_filename=''
        app_name=''
        app_id=-1
        root_num=-1
        highest_strace=-1
        
        if 'strace.txt' in files:
            strace_filename=apk_dir+'/strace.txt'
            apk_activities=''
            
            if os.path.isfile(apk_dir+'/apk-info.txt') != True:
                #print 'Cannot open apk info file in ',apk_dir
                continue
            apkinfo_filename=apk_dir+'/apk-info.txt'
        else:
        
            #
            # get highest strace number if there is multiple strace files
            #
            for item in files:
                if item[0:7]=='strace.':
                    strace_num=int(item[7])
                    if strace_num>highest_strace:
                        highest_strace=strace_num
                        strace_filename=apk_dir+'/'+item
            if highest_strace==-1:
                #print 'Cannot get strace file in ',apk_dir
                continue
                #sys.exit(0)
                
            if os.path.isfile(apk_dir+'/apk-info.'+str(highest_strace)+'.txt') != True:
                print 'Cannot open apk-info file in ',apk_dir
                continue
            apkinfo_filename=apk_dir+'/apk-info.'+str(highest_strace)+'.txt'
            
        apk_info=open(apkinfo_filename,'r')
        feat_vect=[0 for i in range(n_feat)]
        lines=apk_info.readlines()
        
        for line in lines:
            line=line.rstrip()
            line=line.strip()
            if 'android.permission' in line:
                line=line[line.rfind('.')+1:]
                if len(line) == 0:
                    continue
                if line not in permission_all:
                    #print line,apk_dir
                    permission_all.append(line)
                if line not in permission:
                    print line, ' not in permission list'
                    continue
                feat_vect[permission.index(line)]=1
        f_output.write(label)
        for i in range(n_feat):
            f_output.write(' '+str(i)+':'+str(feat_vect[i]))
        f_output.write('\n');
                #print line

#permission_all.sort()
#print permission_all

#print len(permission_all)


#
# get unique permissions from both benign and malware
#
#permission_uni=[]
#for item in permission:
#    if item not in permission_uni:
#        permission_uni.append(item)
#permission_uni.sort()
#print permission_uni
              
            
    
    


