# Keep the core provider-neutral and ship Codex first

The Blueprint contract is provider-neutral, while version 1 implements only Codex, dependency-free Python reference, and documentation targets. This preserves future portability without advertising untested adapters or multiplying the initial maintenance surface.

