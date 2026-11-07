"""Sign the firmware in incoming/ and write the release files (used by .github/workflows/release.yml).

    SIGNING_KEY=<contents of parasha-signing-key.pem> python3 tools/sign_release.py incoming out

Reads the version and model from each .bin ("Parasha Display 0.6.4 model 75"), signs
"PDFW1|<model>|<version>|<sha256 hex>" with ECDSA P-256 / SHA-256 (raw r||s, base64) -- the same format
as the release tool and the check in the firmware (include/ota.h) -- and writes out/manifest.json,
the renamed .bin files and out/VERSION.
"""
import base64, hashlib, json, os, re, shutil, sys
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, utils

src, out = sys.argv[1], sys.argv[2]
key_pem = os.environ.get("SIGNING_KEY", "").strip()
if not key_pem:
    sys.exit("SIGNING_KEY secret is missing (repo Settings -> Secrets and variables -> Actions).")
key = serialization.load_pem_private_key(key_pem.encode() + b"\n", None)
pub = key.public_key().public_bytes(serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint)
expected = base64.b64decode(open(os.path.join(os.path.dirname(__file__), "update_pubkey.txt")).read().strip())
if pub != expected:
    sys.exit("SIGNING_KEY is not the key built into the displays (fingerprint %s, expected %s)."
             % (hashlib.sha256(pub).hexdigest()[:8].upper(), hashlib.sha256(expected).hexdigest()[:8].upper()))

NAMES = {"42": "parasha-4.2in.bin", "75": "parasha-7.5in.bin"}
builds, versions = {}, set()
os.makedirs(out, exist_ok=True)
for f in sorted(os.listdir(src)):
    if not f.endswith(".bin"):
        continue
    data = open(os.path.join(src, f), "rb").read()
    m = re.search(rb"Parasha Display (\d+(?:\.\d+){1,3}) model (42|75)", data)
    if not m:
        sys.exit(f"{f}: not a Parasha Display firmware file")
    ver, model = m.group(1).decode(), m.group(2).decode()
    if model in builds:
        sys.exit(f"two files for model {model}")
    versions.add(ver)
    sha = hashlib.sha256(data).hexdigest()
    der = key.sign(f"PDFW1|{model}|{ver}|{sha}".encode(), ec.ECDSA(hashes.SHA256()))
    r, s = utils.decode_dss_signature(der)
    builds[model] = {"file": NAMES[model], "size": len(data), "sha256": sha,
                     "sig": base64.b64encode(r.to_bytes(32, "big") + s.to_bytes(32, "big")).decode()}
    shutil.copyfile(os.path.join(src, f), os.path.join(out, NAMES[model]))
    print(f"{f}: model {model}, version {ver}, {len(data)} bytes, sha256 {sha[:12]}...")
if not builds:
    sys.exit("no .bin files in " + src)
if len(versions) != 1:
    sys.exit("the files are different versions: " + ", ".join(sorted(versions)))
ver = versions.pop()
json.dump({"product": "parasha-display", "version": ver, "tag": "v" + ver, "builds": builds},
          open(os.path.join(out, "manifest.json"), "w"), indent=2)
open(os.path.join(out, "VERSION"), "w").write(ver)
print("signed version", ver, "with key", hashlib.sha256(pub).hexdigest()[:8].upper())
