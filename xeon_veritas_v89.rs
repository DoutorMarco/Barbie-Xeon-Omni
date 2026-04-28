use std::thread;
use std::time::Duration;

fn main() {
    println!("--- MONITOR DE TIMEOUT XEON v89.0 ---");
    
    let limite_espera = 3; // Segundos
    let mut tempo_decorrido = 0;
    let conexao_sucesso = false; // Simulação de rede fora do ar

    println!("TENTANDO CONEXÃO (LIMITE: {}s)...", limite_espera);

    while tempo_decorrido < limite_espera {
        if conexao_sucesso {
            println!("SUCESSO: CONEXÃO ESTABELECIDA.");
            return;
        }
        
        thread::sleep(Duration::from_secs(1));
        tempo_decorrido += 1;
        println!("Aguardando... {}s", tempo_decorrido);
    }

    println!("--- ALERTA: TIMEOUT ALCANÇADO ---");
    println!("STATUS: ABORTANDO PARA EVITAR TRAVAMENTO DO CÓRTEX.");
    println!("VEREDITO: SISTEMA PROTEGIDO CONTRA LATÊNCIA INFINITA.");
}