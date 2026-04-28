use std::collections::HashMap;

fn main() {
    println!("--- ALGORITMO DE CONSENSO XEON v96.0 ---");

    // Simulando três leituras de sensores independentes
    // Sensor 3 está "alucinando" (ruído térmico)
    let leituras = vec![323.0, 323.0, 328.5]; 

    println!("LEITURAS RECEBIDAS: {:?}", leituras);

    let mut contagem = HashMap::new();

    // Contabilizando os votos de cada valor
    for &valor in &leituras {
        *contagem.entry(valor.to_string()).or_insert(0) += 1;
    }

    // Decidindo pela maioria (Consenso)
    let mut vencedor = String::new();
    let mut max_votos = 0;

    for (valor, &votos) in &contagem {
        if votos > max_votos {
            max_votos = votos;
            vencedor = valor.clone();
        }
    }

    if max_votos >= 2 {
        println!("STATUS: CONSENSO ALCANÇADO VIA MAIORIA ({} votos).", max_votos);
        println!("VEREDITO: VALOR DETERMINÍSTICO DEFINIDO EM {}K.", vencedor);
        println!("NOTA: LEITURA DISCREPANTE DESCARTADA COM SUCESSO.");
    } else {
        println!("ALERTA: IMPOSSOBILIDADE DE CONSENSO. REINICIAR SENSORES.");
    }
}