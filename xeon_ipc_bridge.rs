// xeon_ipc_bridge.rs
// MISSÃO: PONTE DE ALTA VELOCIDADE ENTRE RUST BARE-METAL E DASHBOARD PYTHON
// STATUS: MISSION CRITICAL

use mmap_rs::MmapOptions; // Biblioteca para mapeamento de memória física

pub struct XeonIPC {
    pub shared_buffer_addr: usize,
}

impl XeonIPC {
    /// Sinaliza o estado de Zeroização para o Dashboard
    /// 0x00: Normal | 0x01: Ataque Detectado | 0xFF: Purga Concluída (Zeroized)
    pub fn signal_purge_status(&self, status_code: u8) {
        unsafe {
            let ptr = self.shared_buffer_addr as *mut u8;
            std::ptr::write_volatile(ptr, status_code);
        }
    }
}
