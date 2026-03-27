# Module Lora LR62E
- Kiểm tra nguồn cấp cho module
- Kiểm tra kết nối spi 
- Kiểm tra truyền/nhận gói tin với SX1276 mbeb shield

Module LR62E được kết nối với CM5 qua SPI bus 1, CE 1. Cần enable cổng này lên trong file `config.txt`
```
sudo nano /boot/firmware/config.txt
```
thêm dòng này vào cuối file sau đó khởi động lại CM5
>dtoverlay=spi1-2cs,cs0_pin=18,cs1_pin=17

## Cài đặt thư viện
- clone thư viện LoRaRF và chỉnh sửa lại những chỗ liên quan đến chip select trong file `SX126x.py`.
```
git clone https://github.com/chandrawi/LoRaRF-Python.git
cd LoRaRF-Python
```
- sửa hàm __init__ với  nội dung mới như sau:
```
def __init__(self, spi: LoRaSpi, reset: LoRaGpio, busy: LoRaGpio, irq: Optional[LoRaGpio]=None, txen: Optional[LoRaGpio]=None, rxen: Optional[LoRaGpio]=None):
        self._spi = spi
        self._reset = reset
        self._busy = busy
        self._irq = irq
        self._txen = txen
        self._rxen = rxen
```
- sửa hàm __wake__ với nội dung mới như sau:
```
def wake(self) :
        # wake device by initiating SPI transaction and put device in standby mode
        self.setStandby(self.STANDBY_RC)
        self._fixResistanceAntenna()
```
- sửa hàm __writeBytes__ với nội dung mới như sau:
```
def _writeBytes(self, opCode: int, data: tuple, nBytes: int) :
        if self.busyCheck() : return
        buf = [opCode]
        for i in range(nBytes) : buf.append(data[i])
        self._spi.transfer(buf)
```
- sửa hàm __readBytes__ với nội dung mới như sau:
```
def _readBytes(self, opCode: int, nBytes: int, address: tuple = (), nAddress: int = 0) -> tuple :
        if self.busyCheck() : return ()
        buf = [opCode]
        for i in range(nAddress) : buf.append(address[i])
        for i in range(nBytes) : buf.append(0x00)
        feedback = self._spi.transfer(buf)
        return tuple(feedback[nAddress+1:])
```
sau khi sửa xong, lưu lại và build package
```
cd LoRaRF-Python
python3 setup.py bdist_wheel
pip3 install dist/LoRaRF-1.4.0-py3-none-any.whl --break-system-packages
```
## Kiểm tra chức năng truyền
```
python3 ~/LR62E/transmitter.py 
```
### Đánh giá
- chương trình hay bị kẹt ở `LoRa.endPacket()`

![image](/LR62E/image/err1.png)

![image](/LR62E/image/err2.png)

![image](/LR62E/image/solu.png)

## Kiểm tra chức năng nhận
```
python3 ~/LR62E/receiver.py
```
### Đánh giá
- dễ bị mất gói tin
- gói tin nhận được bị lỗi, giải mã không như mong muốn
![image](/LR62E/image/err3.png)

![image](/LR62E/image/err4.png)

## SX1276 mbed shield
đối với chương trình cho SX1276 mbed shield, em có sửa lại để chỉ dùng tính năng đơn giản là truyền/nhận để giao tiếp với LR62E. 
Chương trình PingPong đầy đủ cho SX1276 mbed shield [ở đây](https://www.st.com/en/embedded-software/i-cube-lrwan.html)