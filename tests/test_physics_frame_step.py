"""Execute the retail task-step producer/writer and patched hkpWorld dt block.

BB_TEST_EBOOT_ELF points at a read-only prepared 1.09 ELF. The harness maps
fixture memory, never a running game, and copies instructions from that ELF.
"""
from paths import ROOT
import ctypes
import io
import os
import struct
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from patches import (FPS_PRESETS, SCALED_BASE, SCALED_FPS, PHYSICS_FRAME_STEP_SITE,
                     PHYSICS_FRAME_STEP_GUARDS, NATIVE_TASK_STEP, eboot_segments,
                     eboot_bytes, preset_writes, physics_frame_step)

ELF = Path(os.environ.get('BB_TEST_EBOOT_ELF') or ROOT/'out/eboot.elf')


class PhysicsStepGuards(unittest.TestCase):
    def test_unconverted_and_missing_image_are_untouched(self):
        writes = [(12, b'example')]
        self.assertIs(physics_frame_step(writes, '30', b'elf'), writes)
        self.assertIs(physics_frame_step(writes, '60', None), writes)

    def test_each_missing_guard_refuses_the_entire_correction(self):
        writes = [(PHYSICS_FRAME_STEP_SITE+11, struct.pack('<f', 1/60))]
        for rejected in PHYSICS_FRAME_STEP_GUARDS:
            with self.subTest(guard=rejected), patch('patches.site_matches',
                    side_effect=lambda elf, guard: guard != rejected), redirect_stdout(io.StringIO()):
                self.assertIs(physics_frame_step(writes, '60', b'elf'), writes)


@unittest.skipUnless(sys.platform == 'win32' and ELF.is_file(), 'needs Windows and BB_TEST_EBOOT_ELF')
class NativePhysicsStep(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.elf = ELF.read_bytes()
        ph = struct.unpack_from('<Q', cls.elf, 32)[0]
        size, count = struct.unpack_from('<HH', cls.elf, 54)
        cls.segments = [struct.unpack_from('<II6Q', cls.elf, ph+i*size) for i in range(count)]
        cls.kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        cls.kernel.VirtualAlloc.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_ulong, ctypes.c_ulong]
        cls.kernel.VirtualAlloc.restype = ctypes.c_void_p
        cls.kernel.VirtualFree.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_ulong]
        cls.kernel.GetCurrentProcess.restype = ctypes.c_void_p
        cls.kernel.FlushInstructionCache.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t]
        cls.length = max(s[3]+s[6] for s in cls.segments if s[0] == 1)
        cls.base = cls.kernel.VirtualAlloc(None, cls.length, 0x3000, 0x40)
        if not cls.base:
            raise OSError(ctypes.get_last_error())
        for typ, _, off, va, _, fs, _, _ in cls.segments:
            if typ == 1:
                ctypes.memmove(cls.base+va, cls.elf[off:off+fs], fs)
        # Last instruction in each copied block returns to the harness.
        ctypes.memmove(cls.base+0x2018e6b, b'\xc3', 1)
        ctypes.memmove(cls.base+0x17f9b78, b'\xc3', 1)

    @classmethod
    def tearDownClass(cls):
        cls.kernel.VirtualFree(cls.base, 0, 0x8000)

    def apply(self, writes):
        for offset, data in writes:
            ctypes.memmove(self.base+offset, data, len(data))
        self.kernel.FlushInstructionCache(self.kernel.GetCurrentProcess(), self.base, self.length)

    def runner(self, native_task=True):
        # Win64 pointer in RCX -> retail SysV arguments; original blocks use
        # the wrapper's frame, just as their containing retail functions do.
        code = bytearray.fromhex('5357554883ec60488d6c2460')
        def call(address):
            code.extend(b'\xe8'+struct.pack('<i', address-(0x100+len(code)+5)))
        if native_task:
            code.extend(bytes.fromhex('4889cb'))  # RBX = SprjFlipper
            call(0x2018e36)
        else:
            code.extend(bytes.fromhex('8b41088945c8'))  # supplied step-info +8
        code.extend(bytes.fromhex('488d7dc0'))  # RDI = step-info
        call(0x103f9f0)  # ORIGINAL native current-step writer
        call(PHYSICS_FRAME_STEP_SITE)
        code.extend(bytes.fromhex('8b45b88b55c848c1e2204809d04883c4605d5f5bc3'))
        self.apply([(0x100, bytes(code))])
        return ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_void_p)(self.base+0x100)

    def pair(self, run, buffer):
        packed = run(ctypes.addressof(buffer))
        return struct.unpack('<ff', struct.pack('<Q', packed))  # physics, task

    def test_all_presets_use_the_actual_native_task_step(self):
        for fps in ('60', '90', '120', '144', 'uncap'):
            names = [SCALED_BASE] if fps in SCALED_FPS else FPS_PRESETS[fps]
            with redirect_stdout(io.StringIO()):
                fixed = preset_writes(ROOT/'patches/Bloodborne.xml', names, fps, '01.09',
                                      eboot_segments(self.elf), self.elf, {})
            # The final write belongs to the production correction; remove it
            # for a negative control with exactly the old preset's instructions.
            self.assertEqual(fixed[-1][0], PHYSICS_FRAME_STEP_SITE)
            old = fixed[:-1]
            target = 1/(120 if fps == 'uncap' else int(fps))
            flipper = ctypes.create_string_buffer(0x2c8)
            self.apply([(0x55404f8, struct.pack('<Q', ctypes.addressof(flipper)))])
            run = self.runner()
            for elapsed in (target, target*1.2, target*1.8, .070, 0, -.1):
                with self.subTest(fps=fps, elapsed=elapsed):
                    struct.pack_into('<f', flipper, 0x18, target)
                    struct.pack_into('<f', flipper, 0x264, elapsed)
                    # Restore the original fragment before applying an old
                    # preset (which writes only its immediate or jump).
                    self.apply([(PHYSICS_FRAME_STEP_SITE,
                                 eboot_bytes(self.elf, PHYSICS_FRAME_STEP_SITE, PHYSICS_FRAME_STEP_SITE+15)), *old])
                    before, task = self.pair(run, flipper)
                    self.assertAlmostEqual(task, min(max(elapsed, target), 1/30), places=6)
                    if (fps != 'uncap' and elapsed == target*1.2) or (fps == 'uncap' and elapsed == .070):
                        self.assertGreater(abs(before-task), .0001)  # old code must reproduce drift
                    self.apply([fixed[-1]])
                    after, task = self.pair(run, flipper)
                    self.assertEqual(after, task)

    def test_native_zero_and_scaled_steps_are_preserved(self):
        with redirect_stdout(io.StringIO()):
            writes = physics_frame_step([], '60', self.elf)
        self.apply(writes)
        run = self.runner(native_task=False)
        for dt in (0, .007, 1/60, .020, 1/30):
            info = ctypes.create_string_buffer(16)
            struct.pack_into('<f', info, 8, dt)
            physics, native = self.pair(run, info)
            self.assertEqual(physics, native)


if __name__ == '__main__':
    unittest.main()
