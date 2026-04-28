use std::collections::HashMap;

fn main() {
    println!("--- DESCOBERTA DE SERVIÇOS XEON v94.0 ---");

    // Registro Central de Serviços
    let mut catalogo_rede = HashMap::new();

    // Registrando os nós da missão
    catalogo_rede.insert("SENSOR_TERMICO", "192.168.1.50");
    catalogo_rede.insert("CORTEX_IA", "192.168.1.100");
    catalogo_rede.insert("MOTOR_PROPULSAO", "192.168.1.150");

    println!("STATUS: {} NÓS DE REDE CATALOGADOS.", catalogo_rede.len());

    // Buscando um serviço específico para comunicação
    let alvo = "CORTEX_IA";
    match catalogo_rede.get(alvo) {
        Some(ip) => println!("[DESCOBERTA] Localizado {}: Conectar em {}", alvo, ip),
        None => println!("[ALERTA] Nó {} não localizado na rede!", alvo),
    }

    println!("VEREDITO: MAPEAMENTO DINÂMICO CONCLUÍDO.");
}