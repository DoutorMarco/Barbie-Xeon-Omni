use std::{thread, time::Duration};

fn main() {
    println!("--- MONITOR DE VITALIDADE XEON v91.0 ---");
    println!("INICIANDO HEARTBEAT (SINAL DE VIDA 2026)...");

    for i in 1..=5 {
        // O sinal de "Estou Vivo"
        println!("[HEARTBEAT] Pulso {} - Enviando sinal 'ALIVE'...", i);
        
        // Simulação de intervalo entre batimentos
        thread::sleep(Duration::from_millis(800));
    }

    println!("STATUS: CONEXÃO MANTIDA POR VIGILÂNCIA CARDÍACA.");
    println!("VEREDITO: SISTEMA ATIVO E DETERMINÍSTICO.");
}