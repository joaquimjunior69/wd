# Define URLs e paths
$downloadUrl = "https://www.generalarcade.com/gamepadtool/GamepadTool.win.latest.zip"
$destinationZip = "GamepadTool.win.latest.zip"
$extractPath = ".\gamepad-tool"

# Baixar o arquivo
Write-Host "Baixando o arquivo..." -ForegroundColor Green
Invoke-WebRequest -Uri $downloadUrl -OutFile $destinationZip

# Verifica se o 7-Zip está instalado
$sevenZipPath = "C:\Program Files\7-Zip\7z.exe"
if (-Not (Test-Path $sevenZipPath)) {
    Write-Host "Erro: 7-Zip não encontrado em 'C:\Program Files\7-Zip\7z.exe'. Instale o 7-Zip antes de continuar." -ForegroundColor Red
    exit
}

# Criar a pasta de extração, se não existir
if (-Not (Test-Path $extractPath)) {
    New-Item -ItemType Directory -Path $extractPath | Out-Null
}

# Extrair o arquivo usando o 7-Zip
Write-Host "Extraindo os arquivos para a pasta correta..." -ForegroundColor Green
& $sevenZipPath x $destinationZip -o"$extractPath" -y

# Confirmação de extração
if (Test-Path $extractPath) {
    Write-Host "Arquivos extraídos com sucesso para '$extractPath'." -ForegroundColor Cyan
} else {
    Write-Host "Erro ao extrair os arquivos." -ForegroundColor Red
}

# Limpar o arquivo ZIP baixado (opcional)
Remove-Item $destinationZip -Force
Write-Host "Download concluído e arquivo ZIP removido." -ForegroundColor Green
