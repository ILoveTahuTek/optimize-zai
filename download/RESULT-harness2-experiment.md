# Eksperimen: Menerapkan Metodologi Harness² ke Workflow Agen Saya

Tanggal: 2026-10-31 · Repo: google-research/harness2 (Apache-2.0, arXiv:2610.14224) ·
Lab: `/home/z/my-project/harness-lab/` · Repo klon: `/home/z/my-project/repo-harness2/`

## 1. Pipeline resmi (harness2-demo --k 2)

Berjalan mulus tanpa kredensial model (proposer deterministik + eksekusi Python nyata):
2 task × (4k rollout + 3k tahap) = 28 eksekusi, 32 panggilan editor, 0 gagal.

Bukti kontras perilaku pada `ledger-2` (input 35.50, −10.25, −5.00):

| Rollout | Output | Keterangan |
|---|---|---|
| base1 | `Total: 35.50` | bug laten: skrip base memfilter `amount > 0`, debit dibuang |
| agg1 (komposisi) | `Total: 20.25` | benar — tertangkap murni dari kontras antar-eksekusi, tanpa ground truth |

Library per-domain tersimpan: `runs/demo/library/k2/agg/accounting/` (INDEX.md + pohon harness lengkap + EXPERIENCE.md per task).

## 2. Replikasi loop pada workflow saya sendiri

Pemetaan arsitektur: **solver** = sub-agen (model dikunci, haiku) · **harness yang dapat diedit**
= `INSTRUCTIONS.md` + `skills/` + `scripts/` · **proposer/composer/selector** = agen utama ·
**bukti** = report.md + process.md tiap rollout. Domain uji: analisis data penjualan
(128 baris, jebakan tersembunyi: 8 duplikat, 4 refund, region kosong).

### Siklus task 1 (sales-2025h1)

1. **Base rollout** — laporan baik, tetapi: 3 varian "Total revenue" sekaligus, angka GROSS
   (49.015) salah dilabeli "net sales", tanpa verifikasi.
2. **PROPOSE** dari evidence: `inv1` (lever umum: definisi NET/GROSS/refund + verifikasi ganda)
   dan `dom1` (lever domain: `profile_csv.py` deterministik + skill data-hygiene).
3. **PROBE (paralel)** — inv1 8/8, dom1 7/8. Probe dom1 menyingkap **defect harness nyata**:
   referensi skill dengan path relatif tidak ditemukan solver.
4. **COMPOSE → c1**: profiler + definisi tunggal + tabel verifikasi per-angka + **path absolut**.
5. **SELECT (butuh anonimisasi)**: memilih cand_1; kunci dibuka setelah keputusan → **c1**.

### Audit eksternal vs ground truth (tersegel sampai setelah seleksi)

| Task 1 (maks 8) | base | inv1 | dom1 | c1 |
|---|---|---|---|---|
| Skor | 5/8 | **8/8** | 7/8 | **8/8** |

Seleksi buta tepat memilih tier tertinggi. Gain base → c1 = +3 poin **murni dari harness**
(model sama) — sesuai tesis Harness².

### Rekursi level-harnessing (Library) + uji transfer (task 2, data baru, jebakan berbeda)

Harness c1 diadopsi apa adanya ke task baru `sales-2025h2` (outlier 250.000, baris amount=0,
6 duplikat, refund, 9 region kosong). Ground truth dipindah keluar pohon lab (leak hardening).

| Task 2 (maks 10) | base | c1 (diadopsi) |
|---|---|---|
| Skor | 8/10 | **10/10** |

### Pelajaran yang tersimpan di Library (`library/data-report/`)

- cue: task data tabular untuk solver baru · lesson: profiler deterministik + definisi tertulis
  + verifikasi per-angka di dalam harness; **semua aset harness dirujuk path absolut**
- evidence: skor audit 5/8 → 8/8 (task 1) dan 8/10 → 10/10 (task 2); probe membuktikan
  failure mode path relatif · confidence: high (2 task, kontras konsisten)

## 3. Biaya

6 rollout solver ≈ 180 ribu token sub-agen; 0 kredensial eksternal; semua artefak lokal.

## 4. Kesimpulan

1. Loop Propose–Probe–Compose bekerja tanpa ground truth: kontras perilaku antar-eksekusi
   cukup untuk melokalisasi defect (mislabel, path relatif) dan menyusun harness yang lebih baik.
2. Level rekursi kedua (Library + adopted harness) memindahkan gain ke task tak terlihat:
   8/10 → 10/10 pada data dengan jebakan berbeda.
3. Pola defect yang tertangkap persis kelas yang diklaim paper: mutu konteks/antarmuka di
   sekitar model, bukan kemampuan model, yang membatasi performa agen.

---

## 5. Lanjutan: rekursi paralel penuh k=2 (task 3, `sales-2025h1-dirty`)

Dataset baru dengan kelas jebakan berbeda: 10 duplikat (termasuk refund terduplikasi),
11 baris refund, 1 baris nol, 7 region kosong, 2 tanggal DD/MM/YYYY, harga Monitor
berubah 210→220. Truth tetap disegel sampai audit.

Struktur k=2 (setia ke `run_parallel`): base rollout → **4 kandidat** (inv1, dom1 dibawa
beku; inv2 = ringkasan-eksekutif + katalog asumsi; dom2 = `detect_anomalies.py` census
format & harga) → **2 komposisi** (agg1 = gabungan penuh; agg2 = ramping self-contained).

| Task 3 (maks 10) | base | inv2 | inv1 | dom1 | dom2 | agg2 | **agg1** |
|---|---|---|---|---|---|---|---|
| Skor audit | 8/10 | 9/10 | 10/10 | 10/10 | 10/10 | 10/10 | **10/10** |

Seleksi buta (cand_5) → **agg1**, tier tertinggi. Seluruh pool konvergen ke angka yang
benar vs truth — yang membedakan adalah jaminan proses: verifikasi per-angka, definisi,
inventaris anomali, katalog asumsi.

### Temuan baru dari k=2

1. **Defect path-relatif bereproduksi**: file skill yang ADA di disk gagal ditemukan solver
   3 dari 4 kali saat direferensikan relatif (dom1 ronde 1; dom1 & dom2 ronde 2) — tapi
   selalu ditemukan via path absolut (c1, agg1). Perbaikan dimasukkan ke kedua komposisi.
2. **Korektivitas saturasi**: angka headline sudah benar bahkan di base; gain harness
   bersifat struktural (menjamin verifikasi/disclosure, bukan berharap solver melakukannya).
3. **Biaya nyata**: rollout agg1 ≈ 45,6k token vs base ≈ 29,6k (+54%) — harness penuh
   membeli jaminan proses, bukan kebenaran tambahan, pada data yang angkanya mudah.
4. **Anomali lintas-kolom tertangkap**: agg2 menemukan refund −220.00 (harga Monitor baru)
   pada 2025-05-07, 5 hari sebelum penjualan 220.00 pertama — insigt yang tidak muncul di
   base maupun probe ronde 1.
5. **Cacat prosedur saya**: satu kandidat (inv2) membocorkan labelnya sendiri via path
   run-dir di dalam teks laporan — pada harness2 sungguhan, anonimisasi ditangani sistem.

### Ledger kumulatif (3 task)

13 rollout solver ≈ 480 ribu token sub-agen · 0 kredensial eksternal · Library kini berisi
2 harness teradopsi dengan EXPERIENCE.md per task.
