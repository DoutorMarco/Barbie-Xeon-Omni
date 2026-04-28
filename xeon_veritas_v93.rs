use std::collections::HashSet;

fn main() {
    println!("--- FILTRO DE IDEMPOTÊNCIA XEON v93.0 ---");

    let mut comandos_processados = HashSet::new();
    
    // Lista de comandos chegando da rede (com uma duplicata proposital)
    let fluxo_entrada = vec!["CMD_001", "CMD_002", "CMD_001", "CMD_003"];

    for cmd in fluxo_entrada {
        if comandos_processados.contains(cmd) {
            println!("[BLOQUEIO] Comando {} já executado. Ignorando duplicata...", cmd);
        } else {
            println!("[EXECUÇÃO] Processando comando novo: {}", cmd);
            comandos_processados.insert(cmd);
        }
    }

    println!("STATUS: {} COMANDOS ÚNICOS ARMAZENADOS.", comandos_processados.len());
    println!("VEREDITO: SISTEMA IMUNE A REPETIÇÕES DE REDE.");
}