[Setup]
AppName=MEFE Makina Teklif Programı
AppVersion=1.0
DefaultDirName={pf}\MEFE Makina\Teklif Programı
DefaultGroupName=MEFE Makina
OutputBaseFilename=TeklifProgramiSetup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
LicenseFile=
UninstallDisplayIcon={app}\TeklifProgrami.exe

[Files]
Source: "dist\TeklifProgrami.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Teklif Programı"; Filename: "{app}\TeklifProgrami.exe"
Name: "{commondesktop}\Teklif Programı"; Filename: "{app}\TeklifProgrami.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Masaüstü kısayolu oluştur"; GroupDescription: "Ek ikonlar:"

[Run]
Filename: "{app}\TeklifProgrami.exe"; Description: "Teklif Programını Başlat"; Flags: nowait postinstall skipifsilent
