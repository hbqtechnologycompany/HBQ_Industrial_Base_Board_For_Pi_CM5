import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(currentdir)))
from LoRaRF import SX126x, LoRaSpi, LoRaGpio
import time

# Begin LoRa radio with connected SPI bus and IO pins (cs and reset) on GPIO
# SPI is defined by bus ID and cs ID and IO pins defined by chip and offset number
spi = LoRaSpi(1, 1)           # SPI1, CSn[1] (CE1)
reset = LoRaGpio(0, 10)       # GPIO10 (LORA_RESET)
busy = LoRaGpio(0, 11)        # GPIO11 (LORA_BUSY)
irq = LoRaGpio(0, 3)          # GPIO3  (LORA_DIO1)

LoRa = SX126x(spi, reset, busy, irq)
print("Begin LoRa radio")
result = LoRa.begin()
print("LoRa.begin() trả về:", result)
if not result:
    raise Exception("Something wrong, can't begin LoRa radio")

# dùng DIO2 làm RF switch:
LoRa.setDio2RfSwitch(True)
# Set frequency to 868 MHz
print("Set frequency to 868 MHz")
LoRa.setFrequency(868000000)

# Set RX gain. RX gain option are power saving gain or boosted gain
print("Set RX gain to power saving gain")
LoRa.setRxGain(LoRa.RX_GAIN_POWER_SAVING)                       # Power saving gain

# Set TX power (nếu cần, thường chỉ dùng cho module phát)
print("Set TX power to 14 dBm")
LoRa.setTxPower(14)

# Configure modulation parameter: SF=7, BW=125kHz, CR=4/5
print("Set modulation parameters:\n\tSpreading factor = 7\n\tBandwidth = 125 kHz\n\tCoding rate = 4/5")
sf = 7                                                          # LoRa spreading factor: 7
bw = 125000                                                     # Bandwidth: 125 kHz
cr = 5                                                          # Coding rate: 4/5
LoRa.setLoRaModulation(sf, bw, cr)

# Configure packet parameter including header type, preamble length, payload length, and CRC type
# The explicit packet includes header contain CR, number of byte, and CRC type
# Receiver can receive packet with different CR and packet parameters in explicit header mode
print("Set packet parameters:\n\tExplicit header type\n\tPreamble length = 12\n\tPayload Length = 15\n\tCRC on")
print("Set packet parameters:\n\tExplicit header type\n\tPreamble length = 8\n\tPayload Length = 64\n\tCRC on\n\tIQ Inversion off")
headerType = LoRa.HEADER_EXPLICIT                               # Explicit header mode
preambleLength = 8                                              # Preamble length = 8
payloadLength = 64                                              # Payload length = 64
crcType = True                                                  # CRC enable
invertIq = False                                                # IQ Inversion off
LoRa.setLoRaPacket(headerType, preambleLength, payloadLength, crcType, invertIq)

# Set syncronize word for public network (0x3444)
print("Set syncronize word to 0x12")
LoRa.setSyncWord(0x12)

print("\n-- LoRa Receiver --\n")

# Cấu hình ngắt (IRQ) cho các sự kiện mong muốn
irq_mask = LoRa.IRQ_RX_DONE | LoRa.IRQ_TIMEOUT | LoRa.IRQ_HEADER_ERR | LoRa.IRQ_CRC_ERR
LoRa.setDioIrqParams(irq_mask, irq_mask, LoRa.IRQ_NONE, LoRa.IRQ_NONE)

LoRa.request(LoRa.RX_CONTINUOUS)
counter = 0

# Receive message continuously
while True:
    # Lấy trạng thái các cờ ngắt hiện tại từ chip LoRa
    irq_status = LoRa.getIrqStatus()
    # print("IRQ status (trước clear):", irq_status) # Debug: In ra trạng thái trước khi xóa

    # Nếu có bất kỳ ngắt nào được kích hoạt
    if irq_status != 0:
        # Xóa TẤT CẢ các cờ ngắt đã được kích hoạt. ĐÂY LÀ BƯỚC QUAN TRỌNG ĐỂ TIẾP TỤC NHẬN.
        LoRa.clearIrqStatus(irq_status)
        # print("IRQ status (sau clear):", LoRa.getIrqStatus()) # Debug: Kiểm tra lại sau khi xóa

        # Kiểm tra loại sự kiện ngắt đã xảy ra
        if irq_status & LoRa.IRQ_RX_DONE:
            print("\n-> Gói tin đã được nhận thành công!")

            # Lấy thông tin về độ dài payload nhận được và địa chỉ buffer
            payload_length_rx, rx_start_buffer_pointer = LoRa.getRxBufferStatus()
            print(f"   Payload Length nhận được: {payload_length_rx} bytes")

            if payload_length_rx > 0:
                try:
                    # Đọc TẤT CẢ các byte payload nhận được từ buffer
                    # Chỉ đọc khi có gói tin đã được xác nhận qua IRQ
                    received_bytes = LoRa.read(payload_length_rx)

                    message = ""
                    # counter = 0

                    # Phân tích payload dựa trên giả định "PING" (4 bytes) + counter (1 byte)
                    if payload_length_rx >= 4:
                        message = "".join(chr(b) for b in received_bytes[0:4])
                        
                    elif payload_length_rx > 0:
                        # Nếu payload ít hơn 4 bytes, đọc toàn bộ là message
                        message = "".join(chr(b) for b in received_bytes)
                        print(f"   Cảnh báo: Payload nhỏ hơn 4 bytes, nội dung có thể không phải 'PING': '{message}'")

                    # In nội dung và counter
                    print(f"   Nội dung: '{message}', Counter: {counter}")
                    counter += 1

                    # Lấy và hiển thị trạng thái gói tin (RSSI, SNR, Signal RSSI)
                    rssi_pkt, snr_pkt, signal_rssi_pkt = LoRa.getPacketStatus()
                    rssi = rssi_pkt / -2
                    snr = snr_pkt / 4
                    signal_rssi = signal_rssi_pkt / -2
                    print(f"   Trạng thái tín hiệu: RSSI = {rssi:.2f} dBm | SNR = {snr:.2f} dB | Signal RSSI = {signal_rssi:.2f} dBm")

                except IndexError:
                    print("   Lỗi: Không thể đọc đủ byte từ bộ đệm. Có thể do gói tin rỗng hoặc lỗi đọc.")
                except Exception as e:
                    print(f"   Lỗi khi xử lý gói tin: {e}")
            else:
                print("   Không có payload hợp lệ trong gói tin đã nhận (gói tin rỗng).")

        elif irq_status & LoRa.IRQ_TIMEOUT:
            print("\nLỗi: Thời gian chờ nhận gói tin đã hết (Timeout).")
        elif irq_status & LoRa.IRQ_HEADER_ERR:
            print("\nLỗi: Gói tin nhận được có lỗi Header (kiểm tra tham số LoRa).")
        elif irq_status & LoRa.IRQ_CRC_ERR:
            print("\nLỗi: Gói tin nhận được có lỗi CRC (dữ liệu bị hỏng).")
        else:
            print(f"\nSự kiện không xác định hoặc lỗi IRQ: 0x{irq_status:X}")
        
        print("-" * 50) # Dòng phân cách

    time.sleep(0.01) # Dừng một chút để tránh vòng lặp quá nóng