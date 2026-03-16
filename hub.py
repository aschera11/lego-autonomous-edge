from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Color
from pybricks.tools import wait
from usys import stdin, stdout
from uselect import poll

hub = TechnicHub()

# ══════════════════════════════════════════════════
#  LED COLOR CODES
#
#  BOOT:
#  YELLOW              -> Initializing
#  CYAN                -> Scanning motor ports
#  WHITE flash x1      -> Motor found on port
#  RED flash x6        -> No motors found at all
#
#  SELF TEST:
#  ORANGE solid        -> Battery reading in progress
#  GREEN flash x3      -> Battery OK  (above 7400 mV)
#  YELLOW flash x3     -> Battery LOW (6600-7400 mV)
#  RED flash x3        -> Battery CRITICAL (below 6600 mV)
#  WHITE pulse x2      -> Motor spin test starting
#  GREEN flash x1      -> Motor passed (rotated OK)
#  RED flash x2        -> Motor failed (blocked or missing)
#
#  RUNTIME:
#  GREEN solid         -> Idle, ready, rdy sent to browser
#  WHITE flash         -> Byte received in stdin
#  ORANGE flash        -> Valid command recognized
#  MAGENTA flash       -> Unknown/unexpected byte
#  RED flash           -> Motor threw an exception
#
#  PROTOCOL:
#  Char UUID: c5f50002-8280-46da-89f4-6d8051e4aeef (ONLY this one)
#  Hub sends b"rdy" via stdout.buffer before each command slot
#  Browser must wait for "rdy" notification THEN send 0x06 + byte
#  using writeValue with response:true (NOT writeWithoutResponse)
#  Firmware strips 0x06, puts remaining bytes into stdin.buffer
# ══════════════════════════════════════════════════


def flash(color, times, on_ms, off_ms):
    i = 0
    while i < times:
        hub.light.on(color)
        wait(on_ms)
        hub.light.off()
        wait(off_ms)
        i = i + 1


def alternate(color_a, color_b, times, ms):
    i = 0
    while i < times:
        hub.light.on(color_a)
        wait(ms)
        hub.light.on(color_b)
        wait(ms)
        i = i + 1


# ── PHASE 1: INIT ──────────────────────────────────────────────
hub.light.on(Color.YELLOW)
wait(500)


# ── PHASE 2: MOTOR DISCOVERY ───────────────────────────────────
hub.light.on(Color.CYAN)
wait(300)

motor_a = None
motor_b = None
motor_c = None
motor_d = None
found_count = 0

try:
    motor_a = Motor(Port.A)
    found_count = found_count + 1
    flash(Color.WHITE, 1, 200, 150)
    hub.light.on(Color.CYAN)
    wait(150)
except Exception:
    pass

try:
    motor_b = Motor(Port.B)
    found_count = found_count + 1
    flash(Color.WHITE, 1, 200, 150)
    hub.light.on(Color.CYAN)
    wait(150)
except Exception:
    pass

try:
    motor_c = Motor(Port.C)
    found_count = found_count + 1
    flash(Color.WHITE, 1, 200, 150)
    hub.light.on(Color.CYAN)
    wait(150)
except Exception:
    pass

try:
    motor_d = Motor(Port.D)
    found_count = found_count + 1
    flash(Color.WHITE, 1, 200, 150)
    hub.light.on(Color.CYAN)
    wait(150)
except Exception:
    pass

if found_count == 0:
    flash(Color.RED, 6, 200, 200)

# First found = drive, second found = steer
# To hardcode: drive_motor = motor_a  steer_motor = motor_b
drive_motor = None
steer_motor = None

if motor_a is not None:
    if drive_motor is None:
        drive_motor = motor_a
    elif steer_motor is None:
        steer_motor = motor_a

if motor_b is not None:
    if drive_motor is None:
        drive_motor = motor_b
    elif steer_motor is None:
        steer_motor = motor_b

if motor_c is not None:
    if drive_motor is None:
        drive_motor = motor_c
    elif steer_motor is None:
        steer_motor = motor_c

if motor_d is not None:
    if drive_motor is None:
        drive_motor = motor_d
    elif steer_motor is None:
        steer_motor = motor_d

DRIVE_SPEED = 800
STEER_ANGLE = 60
STEER_SPEED = 300


# ── PHASE 3: BATTERY CHECK ─────────────────────────────────────
hub.light.on(Color.ORANGE)
wait(400)

try:
    voltage_mv = hub.battery.voltage()
    if voltage_mv >= 7400:
        flash(Color.GREEN, 3, 250, 150)
    elif voltage_mv >= 6600:
        flash(Color.YELLOW, 3, 300, 150)
    else:
        flash(Color.RED, 3, 400, 200)
except Exception:
    flash(Color.MAGENTA, 2, 300, 200)

wait(300)


# ── PHASE 4: MOTOR SELF-TEST ───────────────────────────────────
hub.light.on(Color.WHITE)
wait(300)
hub.light.off()
wait(200)
hub.light.on(Color.WHITE)
wait(300)
hub.light.off()
wait(400)


def test_motor(m):
    if m is None:
        return
    hub.light.on(Color.ORANGE)
    wait(200)
    try:
        angle_before = m.angle()
        m.run_time(400, 400, wait=True)
        wait(100)
        angle_after = m.angle()
        if angle_before > angle_after:
            delta = angle_before - angle_after
        else:
            delta = angle_after - angle_before
        m.run_target(300, angle_before, wait=True)
        wait(100)
        if delta >= 15:
            flash(Color.GREEN, 1, 300, 150)
        else:
            flash(Color.RED, 2, 300, 150)
    except Exception:
        flash(Color.RED, 2, 300, 150)
    wait(200)


test_motor(motor_a)
test_motor(motor_b)
test_motor(motor_c)
test_motor(motor_d)


# ── PHASE 5: STDIN SETUP ───────────────────────────────────────
hub.light.on(Color.YELLOW)
wait(200)

stdin_ok = False
try:
    tmp = stdin.buffer
    stdin_ok = True
except AttributeError:
    alternate(Color.RED, Color.YELLOW, 10, 250)
    stdin_ok = False

keyboard = poll()
try:
    keyboard.register(stdin)
except Exception:
    alternate(Color.CYAN, Color.RED, 10, 250)


# ── PHASE 6: READY ─────────────────────────────────────────────
hub.light.on(Color.GREEN)
wait(600)
hub.light.off()
wait(200)
hub.light.on(Color.GREEN)


# ══════════════════════════════════════════════════
#  MAIN LOOP
# ══════════════════════════════════════════════════

while True:

    # Signal browser: ready for next command
    stdout.buffer.write(b"rdy")

    # Wait for a byte to arrive (yields CPU while waiting)
    while not keyboard.poll(10):
        wait(10)

    # Read 1 raw byte
    raw = None
    if stdin_ok:
        try:
            raw = stdin.buffer.read(1)
        except Exception:
            raw = None

    if raw is None:
        try:
            ch = stdin.read(1)
            if isinstance(ch, str):
                raw = ch.encode()
            else:
                raw = ch
        except Exception:
            raw = None

    if raw is None:
        continue

    if len(raw) == 0:
        continue

    byte_val = raw[0]
    cmd = chr(byte_val)

    hub.light.on(Color.WHITE)
    wait(60)

    is_valid = (
        cmd == 'w' or
        cmd == 's' or
        cmd == 'a' or
        cmd == 'd' or
        cmd == 'x' or
        cmd == 'q' or
        cmd == 'e' or
        cmd == 'z' or
        cmd == 'c'
    )

    if not is_valid:
        hub.light.on(Color.MAGENTA)
        stdout.buffer.write(b"unk")
        wait(200)
        hub.light.on(Color.GREEN)
        continue

    hub.light.on(Color.ORANGE)

    try:

        if cmd == 'w':
            if drive_motor is not None:
                drive_motor.run(DRIVE_SPEED)
            if steer_motor is not None:
                steer_motor.run_target(STEER_SPEED, 0)

        elif cmd == 's':
            if drive_motor is not None:
                drive_motor.run(-DRIVE_SPEED)
            if steer_motor is not None:
                steer_motor.run_target(STEER_SPEED, 0)

        elif cmd == 'a':
            if steer_motor is not None:
                steer_motor.run_target(STEER_SPEED, -STEER_ANGLE)

        elif cmd == 'd':
            if steer_motor is not None:
                steer_motor.run_target(STEER_SPEED, STEER_ANGLE)

        elif cmd == 'x':
            if drive_motor is not None:
                drive_motor.stop()
            if steer_motor is not None:
                steer_motor.run_target(STEER_SPEED, 0)

        elif cmd == 'q':
            if drive_motor is not None:
                drive_motor.run(DRIVE_SPEED)
            if steer_motor is not None:
                steer_motor.run_target(STEER_SPEED, -STEER_ANGLE)

        elif cmd == 'e':
            if drive_motor is not None:
                drive_motor.run(DRIVE_SPEED)
            if steer_motor is not None:
                steer_motor.run_target(STEER_SPEED, STEER_ANGLE)

        elif cmd == 'z':
            if drive_motor is not None:
                drive_motor.run(-DRIVE_SPEED)
            if steer_motor is not None:
                steer_motor.run_target(STEER_SPEED, -STEER_ANGLE)

        elif cmd == 'c':
            if drive_motor is not None:
                drive_motor.run(-DRIVE_SPEED)
            if steer_motor is not None:
                steer_motor.run_target(STEER_SPEED, STEER_ANGLE)

        stdout.buffer.write(b"ok!")
        wait(60)
        hub.light.on(Color.GREEN)

    except Exception:
        hub.light.on(Color.RED)
        stdout.buffer.write(b"err")
        wait(400)
        hub.light.on(Color.GREEN)