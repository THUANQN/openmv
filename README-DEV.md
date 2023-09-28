### Hướng dẫn sơ bộ
- Xem hướng dẫn thiết lập môi trường phát triển [link](src/README.md)
- Các bước thực hiện như sau :
  - Fork từ trang github về kho của tài khoản mình [openmv/openmv](https://github.com/openmv/openmv.git)
  - Clone recursive từ kho đã fork [THUANQN/openmv](https://github.com/THUANQN/openmv.git)
    - `$ git clone --recurse-submodules -j8 https://github.com/THUANQN/openmv.git`
    - Update: Giảm thời gian kéo xuống, ta làm như sau:
        - `$ git clone --depth=1 https://github.com/THUANQN/openmv.git`
        - `$ cd openmv`
        - `$ git submodule update --init --depth=1 --no-single-branch`
        - `$ git -C src/micropython/ submodule update --init --depth=1`
  - Tạo môi trường phát triển từ Linux theo các dòng lệnh như sau: 
    ```
    $ sudo apt-get update
    $ sudo apt-get install git build-essential
    $ TOOLCHAIN_PATH=/usr/local/arm-none-eabi
    $ TOOLCHAIN_URL="https://armkeil.blob.core.windows.net/developer/Files/downloads/gnu-rm/10-2020q4/gcc-arm-none-eabi-10-2020-q4-major-x86_64-linux.tar.bz2"
    $ sudo mkdir ${TOOLCHAIN_PATH}
    $ wget --no-check-certificate -O - ${TOOLCHAIN_URL} | sudo tar --strip-components=1 -jx -C ${TOOLCHAIN_PATH}
    $ export PATH=${TOOLCHAIN_PATH}/bin:${PATH}
    ```
    - Sau này mỗi lần gọi môi trường phát triển có thể thực hiện dòng lệnh qua mỗi terminal
    ```
    $ TOOLCHAIN_PATH=/usr/local/arm-none-eabi
    $ export PATH=${TOOLCHAIN_PATH}/bin:${PATH}
    ```
    - Hoặc thực hiện thêm đường dẫn `usr/local/arm-none-eabi` vào biến `PATH` tại file config `~/.bashrc` nếu sử dụng thường xuyên.
  - Build firmware
    ```
    cd openmv
    make -j$(nproc) -C src/micropython/mpy-cross   # Builds Micropython mpy cross-compiler
    make -j$(nproc) TARGET=<TRAGET_NAME> -C src    # Builds the OpenMV firmware
    ```
    - Có 2 quá trình build là `micropython` (tạo ra file biên dịch chéo `mpy-cross` trong thư mục `src/micropython/mpy-cross/build`) và `target board` (tạo ra các file cơ bản như `bootloader.bin` `firmware.bin` `openmv.bin` nằm trong thư mục `src/build/bin`)
    - <TARGET_NAME> tham khảo trong [supported boards](https://github.com/openmv/openmv/tree/master/src/omv/boards). VD `OPENMV4` `OPENMV4P`
    - Vì chúng ta đang tập trung phát triển phía `openmv` còn `micropython` chỉ là submodule trợ giúp nên sau khi chỉnh sửa chỉ cần build `target board` là được.
    - Khi rẽ sang nhánh develop cần thực hiện lệnh `$git submodule update --recursive` để cập nhật submodule trước khi build
  - Ý nghĩa các file sau khi build
    ```
    * bootloader.bin  # Bootloader Binary Image (not directly used)
    * bootloader.dfu  # Bootloader DFU Image (not directly used)
    * bootloader.elf  # Bootloader ELF Image (used to generate the BIN/DFU Files)
    * firmware.bin    # Firmware Binary Image (Used by `Tools->Run Bootloader` in OpenMV IDE)
    * firmware.dfu    # Firmware DFU Image (not directly used)
    * firmware.elf    # Firmware ELF Image (used to generate the BIN/DFU Files)
    * openmv.bin      # Combined Bootloader+Firmware Binary Image (not directly used)
    * openmv.dfu      # Combined Bootloader+Firmware DFU Image (Used by `Tools->Run Bootloader` in OpenMV IDE)
    * uvc.bin         # Alternative UVC Binary Image (not directly used)
    * uvc.dfu         # Alternative UVC DFU Image (not directly used)
    * uvc.elf         # Alternative UVC ELF Image (used to generate the BIN/DFU Files)
    ```
  - Flash firmware (tìm hiểu sau)
### Cách thức tiếp cận để develop
- Hướng dẫn chung
    - Tạo branch mới hoặc checkout/switch branch
        - `$ git checkout -b dev-thuanqn`
        - `$ git switch dev-thuanqn`
    - Develop source code   
    - Commit and push
        - `$ git add . && git commit "<commit-message>"`
        - `$ git push` or `$ git push <remote-name> <branch-name>` (vd `$ git push orgin dev-thuanqn`)
        

