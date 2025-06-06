// SPDX-FileCopyrightText: © 2024 Tenstorrent AI ULC
//
// SPDX-License-Identifier: Apache-2.0
#pragma once

#include <optional>

#include "ttexalens_implementation.h"
#include "umd/device/cluster.h"

namespace tt::exalens {

class umd_implementation : public ttexalens_implementation {
   public:
    typedef tt::umd::Cluster DeviceType;
    umd_implementation(tt::umd::Cluster* cluster);

   protected:
    std::optional<uint32_t> pci_read32(uint8_t noc_id, uint8_t chip_id, uint8_t noc_x, uint8_t noc_y,
                                       uint64_t address) override;
    std::optional<uint32_t> pci_write32(uint8_t noc_id, uint8_t chip_id, uint8_t noc_x, uint8_t noc_y, uint64_t address,
                                        uint32_t data) override;
    std::optional<std::vector<uint8_t>> pci_read(uint8_t noc_id, uint8_t chip_id, uint8_t noc_x, uint8_t noc_y,
                                                 uint64_t address, uint32_t size) override;
    std::optional<uint32_t> pci_write(uint8_t noc_id, uint8_t chip_id, uint8_t noc_x, uint8_t noc_y, uint64_t address,
                                      const uint8_t* data, uint32_t size) override;
    std::optional<uint32_t> pci_read32_raw(uint8_t chip_id, uint64_t address) override;
    std::optional<uint32_t> pci_write32_raw(uint8_t chip_id, uint64_t address, uint32_t data) override;
    std::optional<uint32_t> dma_buffer_read32(uint8_t chip_id, uint64_t address, uint32_t channel) override;

    std::optional<std::string> pci_read_tile(uint8_t noc_id, uint8_t chip_id, uint8_t noc_x, uint8_t noc_y,
                                             uint64_t address, uint32_t size, uint8_t data_format) override;

    std::optional<std::string> get_device_arch(uint8_t chip_id) override;

    virtual std::optional<std::tuple<int, uint32_t, uint32_t>> arc_msg(uint8_t noc_id, uint8_t chip_id,
                                                                       uint32_t msg_code, bool wait_for_done,
                                                                       uint32_t arg0, uint32_t arg1,
                                                                       int timeout) override;
    virtual std::optional<uint32_t> read_arc_telemetry_entry(uint8_t chip_id, uint8_t telemetry_tag) override;

   private:
    bool is_chip_mmio_capable(uint8_t chip_id);

    tt::umd::Cluster* cluster = nullptr;
    std::string cluster_descriptor_path;

    std::unique_ptr<tt::umd::ArcTelemetryReader> cached_arc_telemetry_reader;
    uint8_t cached_arc_telemetry_reader_chip_id = UINT8_MAX;
};

}  // namespace tt::exalens
