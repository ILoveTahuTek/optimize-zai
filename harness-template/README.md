# harness-template — Loop PPC (Propose · Probe · Compose), harness-agnostic

Template workflow hasil distillasi eksperimen Harness² (2026-10-31, laporan lengkap:
`download/RESULT-harness2-experiment.md`). Intinya: naikkan mutu kerja agen dengan
memperbaiki **harness** — instruksi, skill, skrip, dan kontrak output yang mengelilingi
model — melalui siklus *Propose → Probe → Compose* yang dinilai dari **kontras
perilaku**, bukan opini; hasil terbaik dipromosikan ke **Library per-domain** agar
terakumulasi lintas tugas.

Bukti dari eksperimen validasi (model tidak pernah diubah):

| Uji | Base | Dengan harness hasil loop |
|---|---|---|
| Task 1 (audit 8 poin) | 5/8 | **8/8** |
| Task 2 — data baru, jebakan berbeda (transfer Library) | 8/10 | **10/10** |
| Task 3 — rekursi paralel k=2 (10 poin) | 8/10 | **10/10** (5 dari 7 harness) |

## Arti "harness-agnostic"

Runtime agen apa pun yang bisa (a) memunculkan sub-eksekutor tanpa memori dan (b)
membaca/menulis file dapat menjalankan protokol ini. Tidak ada SDK vendor, tidak ada
API key — semua tooling Python stdlib. Pemetaan peran di lingkungan GLM/Z.ai:
SOLVER = sub-agen (model dikunci); PROPOSER/COMPOSER/SELECTOR/AUDITOR = agen utama;
harness = `INSTRUCTIONS.md` + `skills/` + `scripts/` milik solver.

## Kapan loop dijalankan

- T0 (sekali jalan): tugas trivial atau sekali pakai — tanpa loop.
- T1 (k=1): domain berulang tapi murah — base → 1 kandidat → compose → select.
- T2 (k≥2 paralel): data kotor / taruhan tinggi — base → 2k kandidat → 2 komposisi → seleksi buta.

Lewati loop untuk percakapan murni, edit sekali-jalan, atau output yang tak bisa dibandingkan.

## Quick start

```bash
cd /home/z/my-project

# 1) Instantiate kontrak file untuk satu task (opsional: adopsi harness dari Library)
python3 harness-template/scripts/new_lab.py \
  --domain data-report --task sales-2025h4 \
  --input path/ke/data.csv \
  --adopt-from harness-lab/library/data-report/harnesses/sales-2025h1-dirty/harness

# 2) Base rollout: jalankan SOLVER (sub-agen) hanya dengan base/ + input/
# 3) DEFECT SCAN → PROPOSE kandidat (masing-masing pohon harness utuh)
# 4) PROBE di sandbox segar; smoke-test skrip dengan data sintetis dulu
# 5) COMPOSE + uji self-containment (path absolut, tanpa referensi keluar pohon)

# 6) Seleksi buta — stdout tidak pernah menampilkan pemetaan; kunci strict JSON
python3 harness-template/scripts/blind_reports.py \
  --runs harness-lab/data-report/tasks/sales-2025h4/runs \
  --out   harness-lab/data-report/tasks/sales-2025h4/selection --scrub
#    tulis selection/ranking.md DULU, baru buka key.json

# 7) Audit vs ground truth tersegel (hanya setelah seleksi)
python3 harness-template/scripts/score_audit.py \
  --checklist .../audit/checklist.json --answers .../audit/answers.json \
  --out .../audit/scores.md

# 8) Promosikan pemenang ke Library
python3 harness-template/scripts/write_library_entry.py \
  --lab harness-lab --domain data-report \
  --harness .../harnesses/agg1 --task sales-2025h4 --name agg1 \
  --cue "..." --lesson "..." --evidence "..." --confidence high
```

## Isi template

| Path | Isi |
|---|---|
| `PROTOCOL.md` | Spesifikasi lengkap: peran, kontrak file, 9 langkah loop, 10 aturan, skema experience |
| `scripts/new_lab.py` | Buat struktur lab satu task (opsional adopsi dari Library) |
| `scripts/blind_reports.py` | Anonimisasi laporan + scrub label + `key.json` strict JSON |
| `scripts/score_audit.py` | Skor checklist berbobot → `scores.md` |
| `scripts/write_library_entry.py` | Promosi pemenang → Library + INDEX.md + EXPERIENCE.md |
| `scaffold/examples/` | Contoh `checklist.json`, `answers.json`, `PROPOSAL.template.md` |

## Integrasi ke workflow agen

- Skill: `skills/harness-ppc/SKILL.md` — dipicu otomatis untuk tugas non-trivial yang
  domainnya berulang, atau manual dengan frasa "pakai harness loop" / "pakai workflow PPC".
- `AGENTS.md` di root sandbox ber instruksi berdiri (standing instructions) untuk agen mana pun.
- Backup: repo GitHub `ILoveTahuTek/optimize-zai` (lihat `RESTORE.md` di repo).

## Provenance

Metode: [google-research/harness2](https://github.com/google-research/harness2)
(Apache-2.0, arXiv:2610.14224) — rekursi tingkat task (Propose–Probe–Compose atas bukti
kontras perilaku) dan tingkat harnessing (Library + experience per domain). Template ini
adalah reimplementasi ringan yang bebas vendor; bukan bagian dari proyek tersebut.
