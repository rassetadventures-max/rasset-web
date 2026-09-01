from pathlib import Path
import shutil

root = Path('.').resolve()
log_path = root / 'scripts' / 'restore_baks_log.txt'
if log_path.exists():
    log_path.unlink()

restored = 0
skipped = 0
with log_path.open('w', encoding='utf-8') as log:
    for bak in root.rglob('*.bak'):
        try:
            orig = bak.with_suffix('')
            # create a safety copy of current orig if it exists and differs from bak
            if orig.exists():
                safety = orig.with_suffix(orig.suffix + '.postapply.bak')
                shutil.copy2(orig, safety)
                log.write(f"Created safety backup: {safety}\n")
            # copy bak -> orig
            shutil.copy2(bak, orig)
            log.write(f"Restored: {orig} from {bak}\n")
            restored += 1
        except Exception as e:
            log.write(f"ERROR restoring {bak}: {e}\n")
            skipped += 1

with log_path.open('a', encoding='utf-8') as log:
    log.write(f"\nSummary: restored={restored}, skipped={skipped}\n")

print(f"Done. Restored {restored} files. Log: {log_path}")
