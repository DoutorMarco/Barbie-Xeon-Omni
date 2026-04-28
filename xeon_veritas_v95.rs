fn main() {
    println!("--- BARRAMENTO DE EVENTOS XEON v95.0 ---");

    // Lista de assinantes (Simulação de módulos ouvindo o sistema)
    let assinantes = vec!["MODULO_MOTOR", "MODULO_BATERIA", "MODULO_RESFRIAMENTO"];

    // O Evento Crítico (O "Grito")
    let evento_urgente = "ALERTA_TERMICO_325K";

    println!("[PUBLISH] Evento detectado: {}", evento_urgente);

    // Propagando para todos os interessados simultaneamente
    for modulo in assinantes {
        println!("[SUBSCRIBE] {} recebeu o alerta e iniciou resposta.", modulo);
    }

    println!("STATUS: PROPAGAÇÃO DE EVENTOS CONCLUÍDA EM MILISSEGUNDOS.");
    println!("VEREDITO: SINCRONIA TOTAL DE REAÇÃO.");
}