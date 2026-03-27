# import os, sys
import time
from LoRaRF import SX126x, LoRaSpi, LoRaGpio

# Cấu hình SPI và GPIO
spi = LoRaSpi(1, 1)           # SPI1, CS1
reset = LoRaGpio(0, 10)       # GPIO10
busy = LoRaGpio(0, 11)        # GPIO11
irq = LoRaGpio(0, 3)          # GPIO3

LoRa = SX126x(spi, reset, busy, irq)
print("Begin LoRa radio")
if not LoRa.begin():
    raise Exception("Can't begin LoRa")

# DIO2 làm RF switch
LoRa.setDio2RfSwitch(True)

# Bước 1: Standby mode
LoRa.setStandby(LoRa.STANDBY_RC)

# Bước 2: LoRa mode
LoRa.setModem(LoRa.LORA_MODEM)

# Bước 3: Tần số
LoRa.setFrequency(868000000)  # 868 MHz

# Bước 4: Cấu hình PA
LoRa.setTxPower(14)  # 14 dBm

# Bước 5: Set TX ramping (được gộp trong setTxPower)

# Bước 6: buffer TX/RX
LoRa.setBufferBaseAddress(0x00, 0x00)

# Bước 7: Gửi payload – thực hiện sau

# Bước 8: modulation parameters
sf = 7       # spreading factor
bw = 125000  # bandwidth
cr = 5       # coding rate (4/5)
LoRa.setLoRaModulation(sf, bw, cr)

# Bước 9: packet params
headerType = LoRa.HEADER_EXPLICIT
preambleLength = 8
payloadLength = 64
crcType = True
invertIq = False
LoRa.setLoRaPacket(headerType, preambleLength, payloadLength, crcType, invertIq)

# Bước 10: cấu hình IRQ TxDone và Timeout
irq_mask = LoRa.IRQ_TX_DONE | LoRa.IRQ_TIMEOUT
LoRa.setDioIrqParams(irq_mask, irq_mask, LoRa.IRQ_NONE, LoRa.IRQ_NONE)


# Bước 11: Sync word
LoRa.setSyncWord(0x12)  # phải giống bên receiver

# Gửi "PING" kèm theo counter mỗi 1 giây
counter = 0
print("\n-- LoRa Transmitter --\n")
while True:
    message = "PING"
    payload = bytearray(message.encode()) + bytearray([counter & 0xFF])
    print(f"[{time.time():.3f}] Bắt đầu gửi: {message}, Counter: {counter}")

    print(f"[{time.time():.3f}] → beginPacket()")
    LoRa.beginPacket()

    print(f"[{time.time():.3f}] → put()")
    LoRa.put(payload)

    
    LoRa.endPacket()  # blocking
    print(f"[{time.time():.3f}] → endPacket()")

    print(f"[{time.time():.3f}] → wait(3)")
    if LoRa.wait(3):
        status = LoRa.status()
        print(f"[{time.time():.3f}] → Trạng thái gửi: {status}")
        if status == LoRa.STATUS_TX_DONE:
            print("   → ✅ Gửi thành công!\n")
        else:
            print("   → ❌ Lỗi trạng thái sau khi gửi.\n")
    else:
        print("   → ❌ Timeout khi chờ phản hồi gửi.\n")

    counter = (counter + 1) % 256
    time.sleep(1)