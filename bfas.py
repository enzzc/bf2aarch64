# BF -> Aarch64 compiler

from itertools import count

# Hello World
instructions = '++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.'

prolog = '''
.global _start
_start:
  ldr x1, =track
'''

data = '''
.data
  track: .FILL 1000, 1 ,0
'''

print_func = '''
print_char:
  mov x0, #1
  // x1 already set
  mov x2, #1 // len = 1 byte
  mov x8, #64  // syscall puts
  svc 0
  ret
'''

exit_func = '''
  // EXIT
  eor x0, x0, x0 // exit code 0
  mov x8, #93  // syscall exit
  svc 0
'''


get_identifier = count(start=0)
instr_count = 0


def emit_intructions(instructions, last_label=0):
    global instr_count
    counter = next(get_identifier)
    for inst in instructions:
        if inst == '>':
            print('  add x1, x1, #1')
            instr_count += 1

        elif inst == '<':
            print('  add x1, x1, #-1')  # will translate as `sub`
            instr_count += 1

        elif inst == '+':
            print('  ldrb w6, [x1]')
            print('  add w6, w6, #1')
            print('  strb w6, [x1]')
            instr_count += 3

        elif inst == '-':
            print('  ldrb w6, [x1]')
            print('  add w6, w6, #-1')  # will translate as `sub`
            print('  strb w6, [x1]')
            instr_count += 3

        elif inst == '.':
            print('  bl print_char')
            instr_count += 1

        elif inst == '[':
            print(f'loop_{counter}:')
            print('  ldrb w6, [x1]')
            print('  cmp w6, #0')
            print(f'  b.eq loopdone_{counter}')
            instr_count += 3
            yield from emit_intructions(instructions, last_label=counter)
            counter = next(get_identifier)

        elif inst == ']':
            print(f'  b loop_{last_label}')
            print(f'loopdone_{last_label}:')
            instr_count += 1
            return

        else:
            raise ValueError('Syntax Error')


print(prolog)
instructions = iter(instructions)
list(emit_intructions(instructions))
print(exit_func)
print(print_func)
print(data)
print(f'// TOTAL INSTRUCTIONS {instr_count}')
