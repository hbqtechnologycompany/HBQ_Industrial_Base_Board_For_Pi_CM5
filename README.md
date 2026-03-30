# CM5 Gateway
Powerful Raspberry Pi CM5-based IoT gateway with 4G (Quectel EC25-E), LoRa (LR62E), and Zigbee (Silicon Labs MGM12/21) options. This repo contains hardware references and software examples to control cellular, LoRa, and Zigbee modules on the CM5 gateway.

<img width="1340" height="827" alt="CM5 Base Board V2" src="https://github.com/user-attachments/assets/004c41dd-b800-45b3-9cf7-db68eaf7eb6c" />
<img width="1024" height="994" alt="CM5 Base Board V2" src="https://github.com/user-attachments/assets/a4fee5ae-d5a8-421f-a334-58e36e0e691e" />

<img width="447" height="500" alt="CM5 Base Board V2" src="https://github.com/user-attachments/assets/c09b169a-82b6-477b-bffa-3d320f86ab8d" />
<img width="447" height="500" alt="CM5 Base Board V2" src="https://github.com/user-attachments/assets/3c0f746d-53c6-4f91-bf9e-5a5010d36583" />

## Buy the CM5 Gateway
- Store: [HBQ Technology Store](https://store.hbqsolution.com/)
- Contact: `contact@hbqsolution.com` | `hbqsolution@gmail.com` | (+84) 035 719 1643 | (+84) 094 850 7979

See `SUPPORT.md` for detailed purchase, warranty, and support information.

## Hardware
- Public schematic: `Schematic/Gateway_CM5_Schematic_public.pdf`
- Photos: `HW/HW.jpg`, `HW/HW_TOP.jpg`, `HW/HW_TOP2.jpg`, `HW/HW_BOT.jpg`

## Modules and Examples
- `EC25-E/`: LTE 4G module utilities and AT command notes
- `LR62E/`: LoRa module setup and Python examples
- `MGM12P22F1024GA-V4R/`: Zigbee NCP CPC notes and build logs
- `MGM210PA22JIA2R/`: Zigbee MG21 docs and images

Each module folder includes its own `README.md` with setup steps and troubleshooting.

## Quick Start (Raspberry Pi CM5)
1. Update OS and enable required interfaces
   - Enable SPI1 and required GPIOs per module README
2. EC25-E power/reset control
   - Use `EC25-E/turn_on_EC25.py` and `EC25-E/reset_EC25.py`
3. Establish 4G data session
   - Bring up `wwan0`, run AT `$QCRMCALL=1,1`, then DHCP on `wwan0`
4. LoRa LR62E
   - Enable `spi1` overlay and use instructions in `LR62E/README.md`
5. Zigbee (CPC)
   - Build and run `cpcd` and host app as documented in `MGM12P22F1024GA-V4R/README.md`

## Development
- Contribution guide: see `CONTRIBUTING.md`
- Code of conduct: see `CODE_OF_CONDUCT.md`
- Security policy: see `SECURITY.md`

## License
This project is licensed under the MIT License. See `LICENSE`.

## Acknowledgements
- Quectel EC25-E docs in `EC25-E/doc`
- Silicon Labs Gecko SDK references in `MGM12P22F1024GA-V4R/zigbeeNCP_CPC/gecko_sdk_4.4.6`

---
If you use CM5 Gateway in a product or research, please star the repo and consider contributing improvements.

## Donate / Sponsor
If this project is useful to you, consider supporting development:
- GitHub Sponsor button (top of repo)
- Custom links: store `https://store.hbqsolution.com/`
- Add your preferred method (PayPal, BuyMeACoffee) to `.github/FUNDING.yml`
