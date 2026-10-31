# AGENTS.md — standing instructions for this sandbox

## 0. Enforcement block — read this FIRST, non-negotiable

> AGENT RULE — WAJIB, TIDAK DINEGOSIASIKAN: untuk setiap tugas non-trivial yang menghasilkan
> artefak dengan struktur yang bisa diperiksa (laporan, analisis, kode), kamu WAJIB menjalankan
> skill `harness-ppc` — baca `/home/z/my-project/harness-template/PROTOCOL.md` utuh sebelum
> rollout pertama — dan mengikuti urutannya tanpa melompati satu langkah pun: (1) MIGRATE:
> cek `harness-lab/library/<domain>/INDEX.md` dan adopsi harness terbaru verbatim sebagai base;
> kalau domain belum ada di Library, itu temuan untuk dilaporkan — BUKAN izin memilih stack:
> ajukan 2–3 opsi oracle beserta kebutuhan infranya dan TUNGGU pengguna memilih sebelum
> memasang toolchain/database atau menyentuh sudo (sandbox ini tanpa sudo, tanpa rustc/psql;
> Python stdlib sqlite3 dan Node tersedia); (2) pilih tier T0/T1/T2 eksplisit dengan
> justifikasi biaya satu kalimat; (3) jalankan: base rollout → defect scan (kutipan verbatim
> per defect) → propose → probe (smoke-test dulu) → compose (cek self-containment) → blind
> select (ground truth disegel di luar lab sampai `ranking.md` ditulis, kunci strict JSON,
> laporan di-scrub) → audit hanya post-selection; (4) PERSIST via `write_library_entry.py`
> jika pemenang ≠ base. Bukti yang diakui HANYA kontras perilaku antar-harness pada input
> yang sama; setiap edit yang diadopsi wajib menyebut mekanisme + bukti; setiap klaim
> "tercatat di jejak audit" harus menunjuk file yang benar-benar ada; setiap asumsi belum
> dikonfirmasi ditandai "assumption → awaiting confirmation". Menyimpang dari protokol ini —
> memilih stack sendiri, meng-install dependensi tanpa izin, atau menyatakan selesai tanpa
> bukti kontras — berarti tugas GAGAL dan diulang dari MIGRATE.

(The block above is the paste-ready master prompt; items 1–7 below are its reference detail.)

For any agent (human-guided or autonomous) working inside `/home/z/my-project/`:

1. **Workflow.** For any non-trivial task in a repeated domain (reports, analyses, code
   with checkable output), run the `harness-ppc` skill — the Propose–Probe–Compose loop.
   Spec: `harness-template/PROTOCOL.md`; scripts: `harness-template/scripts/` (stdlib only).
   Trigger phrases: "pakai harness loop", "pakai workflow PPC", "apply the harness template".
2. **Library first.** Before proposing new harnesses, check
   `harness-lab/library/<domain>/INDEX.md` and adopt the newest harness verbatim as base.
   A missing domain is a finding to report, not a license to pick a stack: propose 2–3
   oracle options and wait for the user's pick. Never install toolchains/DBs or use sudo
   without explicit approval — this sandbox has no passwordless sudo and no rustc/psql;
   Python stdlib `sqlite3` (real SQLite) and Node are available for real behavioral
   evidence with zero installs.
3. **Evidence discipline.** Ground truth is sealed outside the lab tree until blind
   selection is written; selection keys are strict JSON; audit is post-selection only.
4. **Lab is evidence.** `harness-lab/` is an append-only experiment record — do not rewrite
   past tasks; add new task dirs instead.
5. **Secrets.** Never write tokens/keys to files or commits; they live only in the current
   shell session and must be rotated by the user after use.
6. **Skill stacks.** Installed: the mattpocock set (upstream names) and pstack as
   `cursor-*` (58 skills, internal refs pre-rewritten; `cursor-poteto-mode` orchestrates
   the others). Verify the call graph any time with `python3 scripts/audit_skill_refs.py`
   (report lands in `download/skill-crossref-audit.md`). `cursor-tdd`/`cursor-teach` are
   pstack's variants — prefer them inside pstack flows, the unprefixed ones in MP flows.
7. **Backup.** This project mirrors `github.com/ILoveTahuTek/optimize-zai` (curated:
   excludes third-party clones; skills organized under `skills/{harness-ppc,mattpocock,
   cursor}` with `skills/INDEX.md`). See `RESTORE.md` in that repo.
