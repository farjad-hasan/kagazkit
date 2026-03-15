## Highlights

- Windows releases include `KagazKit.exe` and `KagazKit.exe.sha256`.
- KagazKit is currently unsigned, so Microsoft Defender SmartScreen may warn before launching the `.exe`.
- Download the Windows binary only from this official GitHub release page.

## Verify The Windows Download

In PowerShell:

```powershell
Get-FileHash .\KagazKit.exe -Algorithm SHA256
```

Compare the SHA256 output to the value in `KagazKit.exe.sha256`.
