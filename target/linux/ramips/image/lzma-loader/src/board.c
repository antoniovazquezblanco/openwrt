/*
 * Arch specific code for ramips based boards
 *
 * Copyright (C) 2013 John Crispin <blogic@openwrt.org>
 * Copyright (C) 2018 Tobias Schramm <tobleminer@gmail.com>
 * Copyright (C) 2023 Antonio Vázquez <antoniovazquezblanco@gmail.com>
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License version 2 as published
 * by the Free Software Foundation.
 */

#include <stdint.h>
#include <stddef.h>

#define KSEG0			0x80000000
#define KSEG1			0xa0000000

#define _ATYPE_ 		__PTRDIFF_TYPE__
#define _ATYPE32_		int

#define _ACAST32_		(_ATYPE_)(_ATYPE32_)

#define CPHYSADDR(a)		((_ACAST32_(a)) & 0x1fffffff)

#define KSEG0ADDR(a)		(CPHYSADDR(a) | KSEG0)
#define KSEG1ADDR(a)		(CPHYSADDR(a) | KSEG1)

#define UART_LSR_THRE		0x20
#define UART_LSR_TEMT		0x40

#if defined(SOC_MT7620) || defined(SOC_RT3883)
#define UART_BASE			KSEG1ADDR(0x10000c00)
#define UART_THR			(UART_BASE + 0x04)
#define UART_LSR			(UART_BASE + 0x1c)
#define UART_LSR_MASK			UART_LSR_TEMT
#elif defined(SOC_MT7621)
#define UART_BASE			KSEG1ADDR(0x1e000c00)
#define UART_THR			(UART_BASE + 0x00)
#define UART_LSR			(UART_BASE + 0x14)
#define UART_LSR_MASK			UART_LSR_THRE
#elif defined(SOC_RT305X)
#define UART_BASE			KSEG1ADDR(0x10000c00)
#define UART_THR			(UART_BASE + 0x04)
#define UART_LSR			(UART_BASE + 0x1c)
#define UART_LSR_MASK			UART_LSR_THRE
#elif defined(SOC_RT63365E)
#define UART_BASE			KSEG1ADDR(0xbfbf0000)
#define UART_THR			(UART_BASE + 0x03)
#define UART_LSR			(UART_BASE + 0x17)
#define UART_LSR_MASK			UART_LSR_THRE
#else
#error "Unsupported SOC..."
#endif

// Helper functions
#define READREG_U8(r)		(*(volatile uint8_t *)(r))
#define WRITEREG_U8(r,v)	(*(volatile uint8_t *)(r)) = v

void board_init(void)
{
	#define	CR_UART_FCR (0x08+UART_BASE+3)
	WRITEREG_U8(CR_UART_FCR, 0xf);
	#define	CR_UART_MCR (0x10+UART_BASE+3)
	WRITEREG_U8(CR_UART_MCR, 0);
	#define	CR_UART_MISCC		(0x24+UART_BASE+3)
	WRITEREG_U8(CR_UART_MISCC, 0);
	#define CR_UART_IER (UART_BASE + 3 + 4)
	WRITEREG_U8(CR_UART_IER, 0);
}

void board_putc(int ch)
{
	while ((READREG_U8(UART_LSR) & UART_LSR_MASK) == 0);
	WRITEREG_U8(UART_THR, (uint8_t) ch);
	while ((READREG_U8(UART_LSR) & UART_LSR_MASK) == 0);
}
