/* =========================
   XEON v1.7: LINKER SCRIPT
   TARGET: ARM CORTEX-M4
   ========================= */

MEMORY
{
  /* Configuração padrão para chips de alta performance (STM32/Cortex-M4) */
  FLASH (rx) : ORIGIN = 0x08000000, LENGTH = 512K
  RAM (rwx)  : ORIGIN = 0x20000000, LENGTH = 128K
}

/* O ponto de entrada definido no xeon_core.rs */
ENTRY(_start)

SECTIONS
{
  /* Vetor de interrupção e código do XEON */
  .text :
  {
    KEEP(*(.vector_table))
    *(.text .text.*)
    . = ALIGN(4);
  } > FLASH

  /* Dados constantes (Matemática do XEON) */
  .rodata :
  {
    *(.rodata .rodata.*)
    . = ALIGN(4);
  } > FLASH

  /* Variáveis de estado de Homeostase */
  .data :
  {
    _sdata = .;
    *(.data .data.*)
    . = ALIGN(4);
    _edata = .;
  } > RAM AT > FLASH

  /* Memória volátil (BSS) */
  .bss :
  {
    _sbss = .;
    *(.bss .bss.*)
    . = ALIGN(4);
    _ebss = .;
  } > RAM

  /* Definição do Stack (Pilha) no topo da RAM para evitar transbordo */
  _stack_top = ORIGIN(RAM) + LENGTH(RAM);
}
