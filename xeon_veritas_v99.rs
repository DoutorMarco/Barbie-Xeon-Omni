fn main() {
    println!("--- PROTOCOLO 2FA XEON v99.0 ---");

    // Fatores de Autenticação
    let chave_operador = "ACESSO_AUTORIZADO_2026";
    let status_sensor = "ESTAVEL"; // A máquina também precisa concordar

    println!("VALIDANDO FATORES DE SEGURANÇA...");

    // O sistema só libera se ambos os fatores forem verdadeiros (Lógica AND)
    if chave_operador == "ACESSO_AUTORIZADO_2026" && status_sensor == "ESTAVEL" {
        println!("SUCESSO: [2FA VALIDADO]. ACIONANDO NÚCLEO.");
    } else {
        println!("ALERTA: [FALHA DE AUTENTICAÇÃO]. ACESSO NEGADO.");
    }

    println!("VEREDITO: SOBERANIA DE COMANDO CONFIRMADA.");
}