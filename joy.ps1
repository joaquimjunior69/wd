# Definir URL do instalador e caminho local temporário
$joyToKeyUrl = "https://joytokey.net/download/JoyToKeySetup_beta_en.exe"
$installerPath = "$env:TEMP\JoyToKeySetup.exe"

# Baixar o instalador
Write-Host "Baixando o instalador do JoyToKey..." -ForegroundColor Green
Invoke-WebRequest -Uri $joyToKeyUrl -OutFile $installerPath

# Verificar se o download foi bem-sucedido
if (-Not (Test-Path $installerPath)) {
    Write-Host "Erro: O instalador não foi baixado corretamente." -ForegroundColor Red
    exit
}

# Executar o instalador
Write-Host "Iniciando a instalação do JoyToKey..." -ForegroundColor Green
Start-Process -FilePath $installerPath -ArgumentList "/SILENT" -Wait

# Verificar se a instalação foi concluída
if (Test-Path "C:\Program Files (x86)\JoyToKey" -or Test-Path "C:\Program Files\JoyToKey") {
    Write-Host "JoyToKey foi instalado com sucesso!" -ForegroundColor Cyan
} else {
    Write-Host "Erro durante a instalação do JoyToKey." -ForegroundColor Red
}

# Limpar instalador temporário
Write-Host "Limpando instalador temporário..." -ForegroundColor Green
Remove-Item $installerPath -Force
