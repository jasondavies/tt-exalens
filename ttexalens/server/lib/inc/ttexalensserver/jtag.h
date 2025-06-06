// SPDX-FileCopyrightText: © 2024 Tenstorrent AI ULC
//
// SPDX-License-Identifier: Apache-2.0
#ifndef JTAG_H
#define JTAG_H

#include <cstdint>
#include <mutex>
#include <string>
#include <unordered_map>
#include <vector>

class Jtag {
   public:
    explicit Jtag(const char* libName);
    ~Jtag();

    int open_jlink_by_serial_wrapper(unsigned int serial_number);
    int open_jlink_wrapper();
    uint32_t read_tdr(const char* client, uint32_t reg_offset);
    uint32_t readmon_tdr(const char* client, uint32_t id, uint32_t reg_offset);
    void writemon_tdr(const char* client, uint32_t id, uint32_t reg_offset, uint32_t data);
    void write_tdr(const char* client, uint32_t reg_offset, uint32_t data);
    void dbus_memdump(const char* client_name, const char* mem, const char* thread_id_name, const char* start_addr,
                      const char* end_addr);
    void dbus_sigdump(const char* client_name, uint32_t dbg_client_id, uint32_t dbg_signal_sel_start,
                      uint32_t dbg_signal_sel_end);
    void write_axi(uint32_t reg_addr, uint32_t data);
    void write_noc_xy(uint32_t node_x_id, uint32_t node_y_id, uint64_t noc_addr, uint32_t noc_data);
    uint32_t read_axi(uint32_t reg_addr);
    uint32_t read_noc_xy(uint32_t node_x_id, uint32_t node_y_id, uint64_t noc_addr);
    std::vector<uint32_t> enumerate_jlink();
    void close_jlink();
    uint32_t read_id_raw();
    uint32_t read_id();

   private:
    void* handle;
    std::unordered_map<std::string, void*> funcMap;
    std::mutex mtx;

    void* loadFunction(const char* name);
};

#endif
