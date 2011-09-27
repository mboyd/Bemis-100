avr-objdump -d main.elf

main.elf:     file format elf32-avr


Disassembly of section .text:

00000000 <__vectors>:
   0:	0c 94 3e 00 	jmp	0x7c	; 0x7c <__ctors_end>
   4:	0c 94 50 00 	jmp	0xa0	; 0xa0 <__bad_interrupt>
   8:	0c 94 50 00 	jmp	0xa0	; 0xa0 <__bad_interrupt>
   c:	0c 94 50 00 	jmp	0xa0	; 0xa0 <__bad_interrupt>
  10:	0c 94 50 00 	jmp	0xa0	; 0xa0 <__bad_interrupt>
  14:	0c 94 50 00 	jmp	0xa0	; 0xa0 <__bad_interrupt>
  18:	0c 94 50 00 	jmp	0xa0	; 0xa0 <__bad_interrupt>
  1c:	0c 94 50 00 	jmp	0xa0	; 0xa0 <__bad_interrupt>
  20:	0c 94 50 00 	jmp	0xa0	; 0xa0 <__bad_interrupt>
  24:	0c 94 50 00 	jmp	0xa0	; 0xa0 <__bad_interrupt>
  28:	0c 94 50 00 	jmp	0xa0	; 0xa0 <__bad_interrupt>
  2c:	0c 94 50 00 	jmp	0xa0	; 0xa0 <__bad_interrupt>
  30:	0c 94 50 00 	jmp	0xa0	; 0xa0 <__bad_interrupt>
  34:	0c 94 50 00 	jmp	0xa0	; 0xa0 <__bad_interrupt>
  38:	0c 94 50 00 	jmp	0xa0	; 0xa0 <__bad_interrupt>
  3c:	0c 94 50 00 	jmp	0xa0	; 0xa0 <__bad_interrupt>
  40:	0c 94 50 00 	jmp	0xa0	; 0xa0 <__bad_interrupt>
  44:	0c 94 50 00 	jmp	0xa0	; 0xa0 <__bad_interrupt>
  48:	0c 94 50 00 	jmp	0xa0	; 0xa0 <__bad_interrupt>
  4c:	0c 94 50 00 	jmp	0xa0	; 0xa0 <__bad_interrupt>
  50:	0c 94 ae 00 	jmp	0x15c	; 0x15c <__vector_20>
  54:	0c 94 50 00 	jmp	0xa0	; 0xa0 <__bad_interrupt>
  58:	0c 94 50 00 	jmp	0xa0	; 0xa0 <__bad_interrupt>
  5c:	0c 94 50 00 	jmp	0xa0	; 0xa0 <__bad_interrupt>
  60:	0c 94 50 00 	jmp	0xa0	; 0xa0 <__bad_interrupt>
  64:	0c 94 50 00 	jmp	0xa0	; 0xa0 <__bad_interrupt>
  68:	0c 94 50 00 	jmp	0xa0	; 0xa0 <__bad_interrupt>
  6c:	0c 94 50 00 	jmp	0xa0	; 0xa0 <__bad_interrupt>
  70:	0c 94 50 00 	jmp	0xa0	; 0xa0 <__bad_interrupt>
  74:	0c 94 50 00 	jmp	0xa0	; 0xa0 <__bad_interrupt>
  78:	0c 94 50 00 	jmp	0xa0	; 0xa0 <__bad_interrupt>

0000007c <__ctors_end>:
  7c:	11 24       	eor	r1, r1
  7e:	1f be       	out	0x3f, r1	; 63
  80:	cf ef       	ldi	r28, 0xFF	; 255
  82:	d4 e0       	ldi	r29, 0x04	; 4
  84:	de bf       	out	0x3e, r29	; 62
  86:	cd bf       	out	0x3d, r28	; 61

00000088 <__do_clear_bss>:
  88:	12 e0       	ldi	r17, 0x02	; 2
  8a:	a0 e0       	ldi	r26, 0x00	; 0
  8c:	b1 e0       	ldi	r27, 0x01	; 1
  8e:	01 c0       	rjmp	.+2      	; 0x92 <.do_clear_bss_start>

00000090 <.do_clear_bss_loop>:
  90:	1d 92       	st	X+, r1

00000092 <.do_clear_bss_start>:
  92:	a4 3f       	cpi	r26, 0xF4	; 244
  94:	b1 07       	cpc	r27, r17
  96:	e1 f7       	brne	.-8      	; 0x90 <.do_clear_bss_loop>
  98:	0e 94 d8 00 	call	0x1b0	; 0x1b0 <main>
  9c:	0c 94 f7 01 	jmp	0x3ee	; 0x3ee <_exit>

000000a0 <__bad_interrupt>:
  a0:	0c 94 00 00 	jmp	0	; 0x0 <__vectors>

000000a4 <USART_Init>:
  a4:	90 93 c5 00 	sts	0x00C5, r25
  a8:	80 93 c4 00 	sts	0x00C4, r24
  ac:	e0 ec       	ldi	r30, 0xC0	; 192
  ae:	f0 e0       	ldi	r31, 0x00	; 0
  b0:	80 81       	ld	r24, Z
  b2:	82 60       	ori	r24, 0x02	; 2
  b4:	80 83       	st	Z, r24
  b6:	88 e9       	ldi	r24, 0x98	; 152
  b8:	80 93 c1 00 	sts	0x00C1, r24
  bc:	86 e0       	ldi	r24, 0x06	; 6
  be:	80 93 c2 00 	sts	0x00C2, r24
  c2:	78 94       	sei
  c4:	08 95       	ret

000000c6 <USART_Transmit>:
  c6:	98 2f       	mov	r25, r24
  c8:	80 91 c0 00 	lds	r24, 0x00C0
  cc:	85 ff       	sbrs	r24, 5
  ce:	fc cf       	rjmp	.-8      	; 0xc8 <USART_Transmit+0x2>
  d0:	90 93 c6 00 	sts	0x00C6, r25
  d4:	08 95       	ret

000000d6 <USART_Receive>:
  d6:	80 91 c0 00 	lds	r24, 0x00C0
  da:	87 ff       	sbrs	r24, 7
  dc:	fc cf       	rjmp	.-8      	; 0xd6 <USART_Receive>
  de:	80 91 c6 00 	lds	r24, 0x00C6
  e2:	08 95       	ret

000000e4 <push>:
  e4:	90 e0       	ldi	r25, 0x00	; 0
  e6:	28 2f       	mov	r18, r24
  e8:	21 70       	andi	r18, 0x01	; 1
  ea:	22 b9       	out	0x02, r18	; 2
  ec:	32 e0       	ldi	r19, 0x02	; 2
  ee:	32 b9       	out	0x02, r19	; 2
  f0:	12 b8       	out	0x02, r1	; 2
  f2:	95 95       	asr	r25
  f4:	87 95       	ror	r24
  f6:	28 2f       	mov	r18, r24
  f8:	21 70       	andi	r18, 0x01	; 1
  fa:	22 b9       	out	0x02, r18	; 2
  fc:	32 b9       	out	0x02, r19	; 2
  fe:	12 b8       	out	0x02, r1	; 2
 100:	95 95       	asr	r25
 102:	87 95       	ror	r24
 104:	28 2f       	mov	r18, r24
 106:	21 70       	andi	r18, 0x01	; 1
 108:	22 b9       	out	0x02, r18	; 2
 10a:	32 b9       	out	0x02, r19	; 2
 10c:	12 b8       	out	0x02, r1	; 2
 10e:	95 95       	asr	r25
 110:	87 95       	ror	r24
 112:	28 2f       	mov	r18, r24
 114:	21 70       	andi	r18, 0x01	; 1
 116:	22 b9       	out	0x02, r18	; 2
 118:	32 b9       	out	0x02, r19	; 2
 11a:	12 b8       	out	0x02, r1	; 2
 11c:	95 95       	asr	r25
 11e:	87 95       	ror	r24
 120:	28 2f       	mov	r18, r24
 122:	21 70       	andi	r18, 0x01	; 1
 124:	22 b9       	out	0x02, r18	; 2
 126:	32 b9       	out	0x02, r19	; 2
 128:	12 b8       	out	0x02, r1	; 2
 12a:	95 95       	asr	r25
 12c:	87 95       	ror	r24
 12e:	28 2f       	mov	r18, r24
 130:	21 70       	andi	r18, 0x01	; 1
 132:	22 b9       	out	0x02, r18	; 2
 134:	32 b9       	out	0x02, r19	; 2
 136:	12 b8       	out	0x02, r1	; 2
 138:	95 95       	asr	r25
 13a:	87 95       	ror	r24
 13c:	28 2f       	mov	r18, r24
 13e:	21 70       	andi	r18, 0x01	; 1
 140:	22 b9       	out	0x02, r18	; 2
 142:	32 b9       	out	0x02, r19	; 2
 144:	12 b8       	out	0x02, r1	; 2
 146:	95 95       	asr	r25
 148:	87 95       	ror	r24
 14a:	81 70       	andi	r24, 0x01	; 1
 14c:	82 b9       	out	0x02, r24	; 2
 14e:	32 b9       	out	0x02, r19	; 2
 150:	12 b8       	out	0x02, r1	; 2
 152:	08 95       	ret

00000154 <latch_out>:
 154:	84 e0       	ldi	r24, 0x04	; 4
 156:	82 b9       	out	0x02, r24	; 2
 158:	12 b8       	out	0x02, r1	; 2
 15a:	08 95       	ret

0000015c <__vector_20>:
 15c:	1f 92       	push	r1
 15e:	0f 92       	push	r0
 160:	0f b6       	in	r0, 0x3f	; 63
 162:	0f 92       	push	r0
 164:	11 24       	eor	r1, r1
 166:	2f 93       	push	r18
 168:	8f 93       	push	r24
 16a:	9f 93       	push	r25
 16c:	ef 93       	push	r30
 16e:	ff 93       	push	r31
 170:	20 91 c6 00 	lds	r18, 0x00C6
 174:	22 34       	cpi	r18, 0x42	; 66
 176:	b9 f0       	breq	.+46     	; 0x1a6 <__vector_20+0x4a>
 178:	80 91 00 01 	lds	r24, 0x0100
 17c:	90 91 01 01 	lds	r25, 0x0101
 180:	fc 01       	movw	r30, r24
 182:	ee 5f       	subi	r30, 0xFE	; 254
 184:	fe 4f       	sbci	r31, 0xFE	; 254
 186:	20 83       	st	Z, r18
 188:	01 96       	adiw	r24, 0x01	; 1
 18a:	90 93 01 01 	sts	0x0101, r25
 18e:	80 93 00 01 	sts	0x0100, r24
 192:	ff 91       	pop	r31
 194:	ef 91       	pop	r30
 196:	9f 91       	pop	r25
 198:	8f 91       	pop	r24
 19a:	2f 91       	pop	r18
 19c:	0f 90       	pop	r0
 19e:	0f be       	out	0x3f, r0	; 63
 1a0:	0f 90       	pop	r0
 1a2:	1f 90       	pop	r1
 1a4:	18 95       	reti
 1a6:	10 92 01 01 	sts	0x0101, r1
 1aa:	10 92 00 01 	sts	0x0100, r1
 1ae:	f1 cf       	rjmp	.-30     	; 0x192 <__vector_20+0x36>

000001b0 <main>:
 1b0:	4f 92       	push	r4
 1b2:	5f 92       	push	r5
 1b4:	6f 92       	push	r6
 1b6:	7f 92       	push	r7
 1b8:	8f 92       	push	r8
 1ba:	9f 92       	push	r9
 1bc:	af 92       	push	r10
 1be:	bf 92       	push	r11
 1c0:	cf 92       	push	r12
 1c2:	df 92       	push	r13
 1c4:	ef 92       	push	r14
 1c6:	ff 92       	push	r15
 1c8:	0f 93       	push	r16
 1ca:	df 93       	push	r29
 1cc:	cf 93       	push	r28
 1ce:	00 d0       	rcall	.+0      	; 0x1d0 <main+0x20>
 1d0:	00 d0       	rcall	.+0      	; 0x1d2 <main+0x22>
 1d2:	cd b7       	in	r28, 0x3d	; 61
 1d4:	de b7       	in	r29, 0x3e	; 62
 1d6:	12 b8       	out	0x02, r1	; 2
 1d8:	87 e0       	ldi	r24, 0x07	; 7
 1da:	81 b9       	out	0x01, r24	; 1
 1dc:	10 92 c5 00 	sts	0x00C5, r1
 1e0:	85 e0       	ldi	r24, 0x05	; 5
 1e2:	80 93 c4 00 	sts	0x00C4, r24
 1e6:	80 91 c0 00 	lds	r24, 0x00C0
 1ea:	82 60       	ori	r24, 0x02	; 2
 1ec:	80 93 c0 00 	sts	0x00C0, r24
 1f0:	88 e9       	ldi	r24, 0x98	; 152
 1f2:	80 93 c1 00 	sts	0x00C1, r24
 1f6:	86 e0       	ldi	r24, 0x06	; 6
 1f8:	80 93 c2 00 	sts	0x00C2, r24
 1fc:	78 94       	sei
 1fe:	8c ec       	ldi	r24, 0xCC	; 204
 200:	89 83       	std	Y+1, r24	; 0x01
 202:	82 e2       	ldi	r24, 0x22	; 34
 204:	8a 83       	std	Y+2, r24	; 0x02
 206:	81 e1       	ldi	r24, 0x11	; 17
 208:	8b 83       	std	Y+3, r24	; 0x03
 20a:	1c 82       	std	Y+4, r1	; 0x04
 20c:	5e 01       	movw	r10, r28
 20e:	08 94       	sec
 210:	a1 1c       	adc	r10, r1
 212:	b1 1c       	adc	r11, r1
 214:	95 e0       	ldi	r25, 0x05	; 5
 216:	69 2e       	mov	r6, r25
 218:	71 2c       	mov	r7, r1
 21a:	6c 0e       	add	r6, r28
 21c:	7d 1e       	adc	r7, r29
 21e:	02 e0       	ldi	r16, 0x02	; 2
 220:	84 e0       	ldi	r24, 0x04	; 4
 222:	88 2e       	mov	r8, r24
 224:	b4 e1       	ldi	r27, 0x14	; 20
 226:	4b 2e       	mov	r4, r27
 228:	b1 e0       	ldi	r27, 0x01	; 1
 22a:	5b 2e       	mov	r5, r27
 22c:	f5 01       	movw	r30, r10
 22e:	80 81       	ld	r24, Z
 230:	90 e0       	ldi	r25, 0x00	; 0
 232:	ee 24       	eor	r14, r14
 234:	ff 24       	eor	r15, r15
 236:	99 24       	eor	r9, r9
 238:	93 94       	inc	r9
 23a:	98 22       	and	r9, r24
 23c:	9c 01       	movw	r18, r24
 23e:	35 95       	asr	r19
 240:	27 95       	ror	r18
 242:	35 95       	asr	r19
 244:	27 95       	ror	r18
 246:	ac 01       	movw	r20, r24
 248:	55 95       	asr	r21
 24a:	47 95       	ror	r20
 24c:	55 95       	asr	r21
 24e:	47 95       	ror	r20
 250:	55 95       	asr	r21
 252:	47 95       	ror	r20
 254:	bc 01       	movw	r22, r24
 256:	75 95       	asr	r23
 258:	67 95       	ror	r22
 25a:	75 95       	asr	r23
 25c:	67 95       	ror	r22
 25e:	75 95       	asr	r23
 260:	67 95       	ror	r22
 262:	75 95       	asr	r23
 264:	67 95       	ror	r22
 266:	fc 01       	movw	r30, r24
 268:	f5 95       	asr	r31
 26a:	e7 95       	ror	r30
 26c:	f5 95       	asr	r31
 26e:	e7 95       	ror	r30
 270:	f5 95       	asr	r31
 272:	e7 95       	ror	r30
 274:	f5 95       	asr	r31
 276:	e7 95       	ror	r30
 278:	f5 95       	asr	r31
 27a:	e7 95       	ror	r30
 27c:	dc 01       	movw	r26, r24
 27e:	0a 2e       	mov	r0, r26
 280:	ab 2f       	mov	r26, r27
 282:	00 0c       	add	r0, r0
 284:	aa 1f       	adc	r26, r26
 286:	bb 0b       	sbc	r27, r27
 288:	00 0c       	add	r0, r0
 28a:	aa 1f       	adc	r26, r26
 28c:	bb 1f       	adc	r27, r27
 28e:	6c 01       	movw	r12, r24
 290:	cc 0c       	add	r12, r12
 292:	cd 2c       	mov	r12, r13
 294:	cc 1c       	adc	r12, r12
 296:	dd 08       	sbc	r13, r13
 298:	95 95       	asr	r25
 29a:	87 95       	ror	r24
 29c:	81 70       	andi	r24, 0x01	; 1
 29e:	21 70       	andi	r18, 0x01	; 1
 2a0:	41 70       	andi	r20, 0x01	; 1
 2a2:	61 70       	andi	r22, 0x01	; 1
 2a4:	e1 70       	andi	r30, 0x01	; 1
 2a6:	a1 70       	andi	r26, 0x01	; 1
 2a8:	9c 2d       	mov	r25, r12
 2aa:	91 70       	andi	r25, 0x01	; 1
 2ac:	92 b8       	out	0x02, r9	; 2
 2ae:	02 b9       	out	0x02, r16	; 2
 2b0:	12 b8       	out	0x02, r1	; 2
 2b2:	82 b9       	out	0x02, r24	; 2
 2b4:	02 b9       	out	0x02, r16	; 2
 2b6:	12 b8       	out	0x02, r1	; 2
 2b8:	22 b9       	out	0x02, r18	; 2
 2ba:	02 b9       	out	0x02, r16	; 2
 2bc:	12 b8       	out	0x02, r1	; 2
 2be:	42 b9       	out	0x02, r20	; 2
 2c0:	02 b9       	out	0x02, r16	; 2
 2c2:	12 b8       	out	0x02, r1	; 2
 2c4:	62 b9       	out	0x02, r22	; 2
 2c6:	02 b9       	out	0x02, r16	; 2
 2c8:	12 b8       	out	0x02, r1	; 2
 2ca:	e2 b9       	out	0x02, r30	; 2
 2cc:	02 b9       	out	0x02, r16	; 2
 2ce:	12 b8       	out	0x02, r1	; 2
 2d0:	a2 b9       	out	0x02, r26	; 2
 2d2:	02 b9       	out	0x02, r16	; 2
 2d4:	12 b8       	out	0x02, r1	; 2
 2d6:	92 b9       	out	0x02, r25	; 2
 2d8:	02 b9       	out	0x02, r16	; 2
 2da:	12 b8       	out	0x02, r1	; 2
 2dc:	08 94       	sec
 2de:	e1 1c       	adc	r14, r1
 2e0:	f1 1c       	adc	r15, r1
 2e2:	33 e5       	ldi	r19, 0x53	; 83
 2e4:	e3 16       	cp	r14, r19
 2e6:	f1 04       	cpc	r15, r1
 2e8:	09 f7       	brne	.-62     	; 0x2ac <main+0xfc>
 2ea:	82 b8       	out	0x02, r8	; 2
 2ec:	12 b8       	out	0x02, r1	; 2
 2ee:	20 e0       	ldi	r18, 0x00	; 0
 2f0:	30 e0       	ldi	r19, 0x00	; 0
 2f2:	c2 01       	movw	r24, r4
 2f4:	01 97       	sbiw	r24, 0x01	; 1
 2f6:	f1 f7       	brne	.-4      	; 0x2f4 <main+0x144>
 2f8:	2f 5f       	subi	r18, 0xFF	; 255
 2fa:	3f 4f       	sbci	r19, 0xFF	; 255
 2fc:	8b e1       	ldi	r24, 0x1B	; 27
 2fe:	28 35       	cpi	r18, 0x58	; 88
 300:	38 07       	cpc	r19, r24
 302:	b9 f7       	brne	.-18     	; 0x2f2 <main+0x142>
 304:	08 94       	sec
 306:	a1 1c       	adc	r10, r1
 308:	b1 1c       	adc	r11, r1
 30a:	a6 14       	cp	r10, r6
 30c:	b7 04       	cpc	r11, r7
 30e:	09 f0       	breq	.+2      	; 0x312 <main+0x162>
 310:	8d cf       	rjmp	.-230    	; 0x22c <main+0x7c>
 312:	ee ee       	ldi	r30, 0xEE	; 238
 314:	f2 e0       	ldi	r31, 0x02	; 2
 316:	32 e0       	ldi	r19, 0x02	; 2
 318:	53 c0       	rjmp	.+166    	; 0x3c0 <main+0x210>
 31a:	6c e0       	ldi	r22, 0x0C	; 12
 31c:	99 38       	cpi	r25, 0x89	; 137
 31e:	08 f4       	brcc	.+2      	; 0x322 <main+0x172>
 320:	5c c0       	rjmp	.+184    	; 0x3da <main+0x22a>
 322:	52 e0       	ldi	r21, 0x02	; 2
 324:	29 38       	cpi	r18, 0x89	; 137
 326:	08 f4       	brcc	.+2      	; 0x32a <main+0x17a>
 328:	5c c0       	rjmp	.+184    	; 0x3e2 <main+0x232>
 32a:	8c e0       	ldi	r24, 0x0C	; 12
 32c:	49 38       	cpi	r20, 0x89	; 137
 32e:	08 f4       	brcc	.+2      	; 0x332 <main+0x182>
 330:	5c c0       	rjmp	.+184    	; 0x3ea <main+0x23a>
 332:	42 e0       	ldi	r20, 0x02	; 2
 334:	90 e0       	ldi	r25, 0x00	; 0
 336:	79 38       	cpi	r23, 0x89	; 137
 338:	08 f0       	brcs	.+2      	; 0x33c <main+0x18c>
 33a:	91 e0       	ldi	r25, 0x01	; 1
 33c:	96 2b       	or	r25, r22
 33e:	95 2b       	or	r25, r21
 340:	20 e0       	ldi	r18, 0x00	; 0
 342:	a9 38       	cpi	r26, 0x89	; 137
 344:	08 f0       	brcs	.+2      	; 0x348 <main+0x198>
 346:	21 e0       	ldi	r18, 0x01	; 1
 348:	82 2b       	or	r24, r18
 34a:	84 2b       	or	r24, r20
 34c:	82 95       	swap	r24
 34e:	80 7f       	andi	r24, 0xF0	; 240
 350:	89 2b       	or	r24, r25
 352:	90 e0       	ldi	r25, 0x00	; 0
 354:	28 2f       	mov	r18, r24
 356:	21 70       	andi	r18, 0x01	; 1
 358:	22 b9       	out	0x02, r18	; 2
 35a:	32 b9       	out	0x02, r19	; 2
 35c:	12 b8       	out	0x02, r1	; 2
 35e:	95 95       	asr	r25
 360:	87 95       	ror	r24
 362:	28 2f       	mov	r18, r24
 364:	21 70       	andi	r18, 0x01	; 1
 366:	22 b9       	out	0x02, r18	; 2
 368:	32 b9       	out	0x02, r19	; 2
 36a:	12 b8       	out	0x02, r1	; 2
 36c:	95 95       	asr	r25
 36e:	87 95       	ror	r24
 370:	28 2f       	mov	r18, r24
 372:	21 70       	andi	r18, 0x01	; 1
 374:	22 b9       	out	0x02, r18	; 2
 376:	32 b9       	out	0x02, r19	; 2
 378:	12 b8       	out	0x02, r1	; 2
 37a:	95 95       	asr	r25
 37c:	87 95       	ror	r24
 37e:	28 2f       	mov	r18, r24
 380:	21 70       	andi	r18, 0x01	; 1
 382:	22 b9       	out	0x02, r18	; 2
 384:	32 b9       	out	0x02, r19	; 2
 386:	12 b8       	out	0x02, r1	; 2
 388:	95 95       	asr	r25
 38a:	87 95       	ror	r24
 38c:	28 2f       	mov	r18, r24
 38e:	21 70       	andi	r18, 0x01	; 1
 390:	22 b9       	out	0x02, r18	; 2
 392:	32 b9       	out	0x02, r19	; 2
 394:	12 b8       	out	0x02, r1	; 2
 396:	95 95       	asr	r25
 398:	87 95       	ror	r24
 39a:	28 2f       	mov	r18, r24
 39c:	21 70       	andi	r18, 0x01	; 1
 39e:	22 b9       	out	0x02, r18	; 2
 3a0:	32 b9       	out	0x02, r19	; 2
 3a2:	12 b8       	out	0x02, r1	; 2
 3a4:	95 95       	asr	r25
 3a6:	87 95       	ror	r24
 3a8:	28 2f       	mov	r18, r24
 3aa:	21 70       	andi	r18, 0x01	; 1
 3ac:	22 b9       	out	0x02, r18	; 2
 3ae:	32 b9       	out	0x02, r19	; 2
 3b0:	12 b8       	out	0x02, r1	; 2
 3b2:	95 95       	asr	r25
 3b4:	87 95       	ror	r24
 3b6:	81 70       	andi	r24, 0x01	; 1
 3b8:	82 b9       	out	0x02, r24	; 2
 3ba:	32 b9       	out	0x02, r19	; 2
 3bc:	12 b8       	out	0x02, r1	; 2
 3be:	36 97       	sbiw	r30, 0x06	; 6
 3c0:	20 81       	ld	r18, Z
 3c2:	41 81       	ldd	r20, Z+1	; 0x01
 3c4:	a2 81       	ldd	r26, Z+2	; 0x02
 3c6:	94 81       	ldd	r25, Z+4	; 0x04
 3c8:	75 81       	ldd	r23, Z+5	; 0x05
 3ca:	83 81       	ldd	r24, Z+3	; 0x03
 3cc:	89 38       	cpi	r24, 0x89	; 137
 3ce:	08 f0       	brcs	.+2      	; 0x3d2 <main+0x222>
 3d0:	a4 cf       	rjmp	.-184    	; 0x31a <main+0x16a>
 3d2:	60 e0       	ldi	r22, 0x00	; 0
 3d4:	99 38       	cpi	r25, 0x89	; 137
 3d6:	08 f0       	brcs	.+2      	; 0x3da <main+0x22a>
 3d8:	a4 cf       	rjmp	.-184    	; 0x322 <main+0x172>
 3da:	50 e0       	ldi	r21, 0x00	; 0
 3dc:	29 38       	cpi	r18, 0x89	; 137
 3de:	08 f0       	brcs	.+2      	; 0x3e2 <main+0x232>
 3e0:	a4 cf       	rjmp	.-184    	; 0x32a <main+0x17a>
 3e2:	80 e0       	ldi	r24, 0x00	; 0
 3e4:	49 38       	cpi	r20, 0x89	; 137
 3e6:	08 f0       	brcs	.+2      	; 0x3ea <main+0x23a>
 3e8:	a4 cf       	rjmp	.-184    	; 0x332 <main+0x182>
 3ea:	40 e0       	ldi	r20, 0x00	; 0
 3ec:	a3 cf       	rjmp	.-186    	; 0x334 <main+0x184>

000003ee <_exit>:
 3ee:	f8 94       	cli

000003f0 <__stop_program>:
 3f0:	ff cf       	rjmp	.-2      	; 0x3f0 <__stop_program>
