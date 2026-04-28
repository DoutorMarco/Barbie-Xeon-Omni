use std::collections::BinaryHeap;

fn main() {
    println!("--- PRIORIZAÇÃO DE FLUXO XEON v92.0 ---");

    // O BinaryHeap sempre coloca o maior valor no topo
    let mut fila_urgencia = BinaryHeap::new();

    // Injetando dados com diferentes prioridades (Nível, Descrição)
    fila_urgencia.push((1, "Log de Rotina"));
    fila_urgencia.push((10, "ALERTA TÉRMICO CRÍTICO"));
    fila_urgencia.push((5, "Atualização de Telemetria"));

    println!("STATUS: {} MENSAGENS EM TRIAGEM.", fila_urgencia.len());

    // Processando por ordem de importância
    while let Some((nivel, msg)) = fila_urgencia.pop() {
        println!("[QoS NÍVEL {}] Processando: {}", nivel, msg);
    }

    println!("VEREDITO: DADOS CRÍTICOS PROCESSADOS COM PRIORIDADE.");
}