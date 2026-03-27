# Module LTE EC25-E
- Kiểm tra nguồn cấp module
- Kiểm tra kết nối sim
- Kiểm tra sóng
- Kiểm tra khả năng truy cập internet

## Cài đặt Driver
Module EC25-E sử dụng USB QMI_WWAN Driver trên hệ điều hành linux. Driver này có sẵn trên raspberry OS nên chúng ta không cần cài đặt thêm.

## Điều khiển module EC25
>PWRKEY Pin của module EC25-E được nối với GPIO27 của CM5.

>RESET_N của module EC25-E được nối với GPIO26 của CM5.

Chúng ta sẽ điều khiển module EC25-E thông qua 2 chân này.

```
// turn on 
python3 ~/EC25E/turn_on_EC25.py
// reset
python3 ~/EC25E/reset_EC25.py
```
sau khi turn on module EC25, đèn Led Mode sẽ sáng, đèn Led Status sẽ nhấp nháy. 

## AT Command
- Kiểm tra kết nối sim
```
at+cpin?
+CPIN: READY
```
- Kiểm tra nhà mạng 
```
at+cops?
+COPS: 0,0,"Viettel Viettel",7
```
- Kiểm tra tín hiệu sóng
```
at+csq
+CSQ: 18,99
```
- Kiểm tra trạng thái đăng ký mạng
```
at+cereg?
+CEREG: 0,1
```

## Kết nối 4g
Bật giao diện mạng 
```
sudo ifconfig wwan0 up
```
Mở minicom `sudo minicom -D /dev/ttyUSB2` rồi chạy at command 
```
AT$QCRMCALL=1,1                         
$QCRMCALL:V4
OK
```
Gán địa chỉ IP cho giao diện mạng wwan0
```
sudo udhcpc -i wwan0
```
![image](/EC25-E/image/ganIP.png)

