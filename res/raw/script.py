import android
import exceptions
import os
import time
import codecs

droid=android.Android()

def eventloop():
	try:
	    while True:
			event=droid.eventWait().result
			print event
			if event["name"]=="click":
				id=event["data"]["id"]
				if id=="btn_exit":
					droid.fullDismiss()
					return
				if id=="btn_crawl":
					
					path=droid.fullQueryDetail("tv_path").result['text']      #path from user
					search=droid.fullQueryDetail("tv_keyword").result['text']   #keyword from user
					results=[]
					
					#FILE EXTENSIONS
					title = 'Select File extensions'
					droid.dialogCreateAlert(title)
					ext_options=['.java', '.txt', '.py','.sh','.html','.php']
					droid.dialogSetMultiChoiceItems(ext_options, [])
					droid.dialogSetPositiveButtonText('Ok')
					droid.dialogShow()
					response=droid.dialogGetResponse().result
					ext=[]
					indexes = droid.dialogGetSelectedItems()[1] # 1 is for getting indices
					if indexes==ext:			#empty
						
						break
					for index in indexes:
						ext.append(ext_options[index])
			
					ext=tuple(ext) 
					
					droid.fullSetProperty("btn_crawl","text","Crawling...")
					for j in os.walk(path): #recursive traversal in given path
						for k in j[2]:
							if k.lower().endswith(ext):
								try:         
									f = open(j[0]+'/'+k,"r")
									droid.fullSetProperty("btn_crawl","text",j[0]+k)
									if search in f.read().decode('UTF-8','ignore') or search in k:
										results.append(j[0]+k)
										droid.fullSetList("listView1",results)
								except Exception as e:
									droid.fullSetProperty("btn_crawl","text",str(e))
									eventloop()
								finally:
									f.close()							
					droid.fullSetProperty("btn_crawl","text","Done.")
					time.sleep(2)
					droid.fullSetProperty("btn_crawl","text","Crawl!")
			elif event["name"]=="screen":
			  if event["data"]=="destroy":
			  	droid.fullDismiss()
				return
	except Exception:
		droid.makeToast(Exception)

print "Started"
layout="""<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="fill_parent"
    android:layout_height="fill_parent"
    android:orientation="vertical" 
	android:background="#aa000000">

    <Button
        android:id="@+id/btn_exit"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:background="@android:drawable/ic_menu_close_clear_cancel" 
        android:layout_gravity="right"/>

    <EditText
        android:id="@+id/tv_path"
        android:layout_width="fill_parent"
        android:layout_height="wrap_content"         
		android:text="/mnt/sdcard/">
		
        <requestFocus />
    </EditText>

    <EditText
        android:id="@+id/tv_keyword"
        android:layout_width="fill_parent"
        android:layout_height="wrap_content" 
        android:hint="keyword"/>


			<Button
	        android:id="@+id/btn_crawl"
	        android:layout_width="fill_parent"
	        android:layout_height="wrap_content"
	        android:text="Crawl!"
	        android:textColor="#ffffffff"
	        android:background="#ff880077"
	         />

    


    <ListView
        android:id="@+id/listView1"
        android:layout_width="fill_parent"
        android:layout_height="wrap_content" >
    </ListView>

</LinearLayout>
"""


print layout
print droid.fullShow(layout)
eventloop()
